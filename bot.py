import requests
from flask import Flask,request
from pymongo import MongoClient
import os

app = Flask(__name__)

@app.route('/',methods = ['POST'])

def webhook():

    msg = request.get_json()

    if '/list' in msg['text'].lower():
        #lists out db list
        db = db_connect()
        reply(show_list(db))
    
    elif '/add' in msg['text'].lower():
        #collect info into list and add to db
    
        ls = parse_text("/add ",msg['text'].lower())
        db = db_connect()
    
        for food in ls:
            add_list(db,food)
    
        reply('ok')
    
    elif '/remove' in msg['text'].lower():
        #collect info into list and remove from db
        ls = parse_text("/remove ", msg['text'].lower())
        db = db_connect()
        for food in ls:
            del_list(db,food)
    
        reply('ok')
    
    return "ok", 200

def reply(msg):
    requests.post('https://api.groupme.com/v3/bots/post?bot_id='+os.getenv('GROUPME_BOT_ID')+'&text='+msg)

def parse_text(method,text):
    text = text.replace(method, "")
    parsed_list = text.split(',')
    fl = []
    for things in parsed_list:
        things = things.strip(' ')
        fl.append(things)

    return fl

def db_connect():
    client = MongoClient(os.getenv('CLIENT_ID'))
    db = client[os.getenv('LIST_NAME')]
    return db

def add_list(db,food):
    db.grocerylist.insert_one({'item' : food})

def del_list(db,food):
    db.grocerylist.delete_one({'item' : food})

def show_list(db):
    result = db.grocerylist.find()
    txt = ''
    for docs in result:
        txt += docs['item'] + '\n'
    return txt
