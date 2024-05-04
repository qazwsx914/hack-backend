
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
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


def RemindAtMind(line = "", futureTime = 0):
    pass

'''
from dateutil import parser
import re
def normalize_time(time_str):
    # Регулярные выражения для различных форматов времени
    patterns = [
        r'(\d+)\s*(?:мин|минут[ыа]?)',
        r'(\d+)\s*(?:час|час[оа]в)',
        r'(\d+)\s*(?:ден[ья]?|дн[ея]?)',
        r'(\d+)\s*(?:недел[ия]?|нед[ей]?)',
        r'(\d+)\s*(?:месяц[аев]?|мес\.?)',
        r'(\d+)\s*(?:го[дау]?|л[ет]?)',
        r'(\d+)\s*([яа]нвар[ья]?|феврал[ья]?|март[а]?|апрел[ья]?|ма[ия]?|июн[ья]?|июл[ья]?|август[а]?|сентябр[ья]?|октябр[ья]?|ноябр[ья]?|декабр[ья]?)\s*(\d+)?'
    ]

    # Попытка совпадения с каждым регулярным выражением
    for pattern in patterns:
        match = re.search(pattern, time_str, re.IGNORECASE)
        if match:
            value = int(match.group(1))
            unit = match.lastgroup
            try:
                if unit.startswith('мин'):
                    return parser.relativedelta(minutes=value)
                elif unit.startswith('час'):
                    return parser.relativedelta(hours=value)
                elif unit.startswith('ден') or unit.startswith('дн'):
                    return parser.relativedelta(days=value)
                elif unit.startswith('недел'):
                    return parser.relativedelta(weeks=value)
                elif unit.startswith('месяц'):
                    return parser.relativedelta(months=value)
                elif unit.startswith('го'):
                    year = match.group(3) if match.group(3) else None
                    return parser.relativedelta(years=value, month=parser.parse(match.group(2), yearfirst=True).month, day=year)
            except ValueError:
                pass

    # Если не удалось совпасть ни с одним регулярным выражением, возвращаем None
    return None
'''

# Определение моделей


class Note(db.Model):
    NoteID = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.Text, nullable=False)
    Description = db.Column(db.Text)
    CreationDate = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    Status = db.Column(db.Text, default='active')



with app.app_context():
    db.create_all()


def RememberNote(line = "", username=""):
    try:
        nt = Note(NoteID=1, Description=line)
        db.session.add(nt)
        db.session.commit()
        return True
    except:
        return False

def ShowNote(username=''):
    return Note.query.filter_by(username=username).all()


@app.route('/', methods=['POST'])
def main():
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

                try:
                    nt = Note(NoteID=1, Description=message, Title='Empty')
                    db.session.add(nt)
                    db.session.commit()
                    res_text = "Я запомнила"
                except Exception as e:
                    res_text = e;

                '''if RememberNote(message, 'username'):
                    res_text = "Я запомнила"
                else:
                    res_text = "Извините, у меня ошибка"'''

        elif req_parts[0] == 'измени' and (req_parts[1] == 'задачу' or req_parts[1] == 'заметку'):
            pass

        elif req_parts[0] == 'задача' or req_parts[0] == 'заметка':
            res_text = ShowNote('username')


    response["response"]["text"] = res_text

    return json.dumps(response)


