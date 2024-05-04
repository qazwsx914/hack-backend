
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from datetime import datetime

import logging
import json

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG)

app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="Kortep",
    password="mysql1716",
    hostname="Kortep.mysql.pythonanywhere-services.com",
    databasename="Kortep$Notes",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


association_table = db.Table('association', db.Model.metadata,
    db.Column('left_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('right_id', db.Integer, db.ForeignKey('note.id'))
)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.Text, nullable=False)
    notes = db.relationship("Note",
                    secondary=association_table)

class Note(db.Model):
    __tablename__ = 'note'
    id = db.Column(db.Integer, primary_key=True)
    Description = db.Column(db.Text, nullable=False)
    Status = db.Column(db.Text, default='active')
    CreateDate = db.Column(db.TIMESTAMP, default=datetime.utcnow)


with app.app_context():
    db.create_all()


def RememberNote(line = "", username=""):
    try:
        us = User(Name=username) # req["session"]["user"]["user_id"]
        nt = Note(Description=line)
        us.notes.append(nt)
        db.session.add(us)
        db.session.commit()
        return True
    except:
        return False

def ShowNote(username=''):
    return Note.query.filter_by(username=username).all()

def SetNoteStatus(desk, status):
    nt = Note.query.filter_by(Description=desk).first()
    nt.Status = status
    db.session.commit()

@app.route('/', methods=['POST'])
def main():
    print("start")

    response = {
        "version": request.json["version"],
        "session": request.json["session"],
        "response": {
            "end_session": False
        }
    }
    req = request.json
    res_text = ""

    if req["session"]["new"]: # Если сессия новая
        res_text = "Привет, я запомню всё, что вы мне скажете"
    else:
        req_text = req["request"]["original_utterance"].lower()
        req_parts = req_text.split() # Делим на отдельные слова

        if req_parts[0] == 'запомни' or req_parts[0] == 'создай':
            if len(req_parts) < 2:
                res_text = "Что я должна запомнить?"
            else:
                if req_parts[1] == 'задачу' or req_parts[1] == 'заметку':
                    message = ' '.join(req_parts[2:]) # Оставляем оставшиеся слова
                else:
                    message = ' '.join(req_parts[1:])
                '''
                try:
                    us = User(Name=req["session"]["user_id"]) # req["session"]["user"]["user_id"]
                    nt = Note(Description=message)
                    us.notes.append(nt)
                    db.session.add(us)
                    db.session.commit()
                    res_text = "Я запомнила"
                except Exception as e:
                    res_text = e
                '''
                if RememberNote(message, req["session"]["user_id"]):
                    res_text = "Я запомнила"
                else:
                    res_text = "Извините, у меня ошибка"


        elif len(req_parts) > 3:
            if req_parts[0] == 'измени' or req_parts[1] == 'статус' or req_parts[2] == 'задачи':
                ln = len(req_parts)
                if req_parts[ln-1] == 'выполнена':
                    if req_parts[ln-2] == 'не':
                        message = ' '.join(req_parts[3:-2])
                        status = False
                    else:
                        message = ' '.join(req_parts[3:-1])
                        status = True
                    SetNoteStatus(message, status)

                else:
                    res_text = "Ошибка"

        #elif req_parts[0] == 'задача' or req_parts[0] == 'заметка':
        #    res_text = ShowNote('username')


    response["response"]["text"] = res_text

    return json.dumps(response)


