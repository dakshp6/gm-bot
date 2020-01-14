from flask import Flask,request
import src

app = Flask(__name__)

@app.route('/',methods = ['POST'])

def webhook():

    msg = request.get_json()

    if '/list' in msg['text'].lower():

        #lists out db list

        db = src.db_connect()

        src.reply(src.show_list(db))
    
    elif '/add' in msg['text'].lower():

        #collect info into list and add to db

        ls = src.parse_text("/add ",msg['text'].lower())

        db = src.db_connect()

        for food in ls:
            src.add_list(db,food)
    
        src.reply('ok, added!')
    
    elif '/remove' in msg['text'].lower():

        #collect info into list and remove from db

        ls = src.parse_text("/remove ", msg['text'].lower())

        db = src.db_connect()

        for food in ls:
            src.del_list(db,food)
    
        src.reply('ok, removed!')
    
    return "ok", 200
