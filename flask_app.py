
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request
from flask_cors import CORS

import logging
import json

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG)

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
    if req["session"]["new"]:
        response["response"]["text"] = "Привет, как дела?"
    else:
        if req["request"]["original_utterance"].lower() in ["хорошо"]:
            response["response"]["text"] = "Супер!"
        elif req["request"]["original_utterance"].lower() in ["плохо"]:
            response["response"]["text"] = "Ну и ладно"
        elif req["request"]["original_utterance"].lower() in ["кто у нас рома"]:
            response["response"]["text"] = "Он у нас красавчик"
        elif req["request"]["original_utterance"].lower() in ["кто у нас руслан"]:
            response["response"]["text"] = "Он у нас программист"
        elif req["request"]["original_utterance"].lower() in ["кто у нас дима"]:
            response["response"]["text"] = "Он у нас обезьянка"
        elif req["request"]["original_utterance"].lower() in ["кто у нас руслан"]:
            response["response"]["text"] = "Просто молодец"
        else:
            response["response"]["text"] = "Пиши по сценарию!!!"

    return json.dumps(response)

