import os
import requests
from flask import Flask,request

app = Flask(__name__)

@app.route('/',methods = ['POST'])

def webhook():

    msg = request.get_json()

    if '@bills' in msg['text'].lower():
        reply('No bills right now!!')

    return "ok", 200


botid = os.getenv('GROUPME_BOT_ID')


def reply(msg):
    requests.post('https://api.groupme.com/v3/bots/post?bot_id='+botid+'&text='+msg)
