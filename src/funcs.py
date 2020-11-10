import requests
import os
from pymongo import MongoClient
import datetime
import geocoder

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

    if not txt:
        return "List is empty!"
    else:
        return txt

def getToday():

    today = datetime.date.today()

    return today.day
