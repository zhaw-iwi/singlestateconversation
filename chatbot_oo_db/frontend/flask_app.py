
# A very simple Flask Hello World app for you to get started with...

from flask import Flask,jsonify,request,render_template
from chatbot_db import Chatbot

app = Flask(__name__)

@app.route('/')
def index():
    return "URL is missing type_id and user_id"

@app.route('/<type_id>/<user_id>/chat')
def chatbot(type_id, user_id):
    return render_template('index.html')

@app.route('/<type_id>/<user_id>/info')
def info_retrieve(type_id, user_id):
    bot = Chatbot(
        database_file="/home/aldespin/chatbot/data/chatbot.db",
        type_id=type_id,
        user_id=user_id
    )
    response = bot.info_retrieve()
    return jsonify(response)

@app.route('/<type_id>/<user_id>/conversation')
def conversation_retrieve(type_id, user_id):
    bot = Chatbot(
        database_file="/home/aldespin/chatbot/data/chatbot.db",
        type_id=type_id,
        user_id=user_id
    )
    response = bot.conversation_retrieve()
    return jsonify(response)

@app.route('/<type_id>/<user_id>/response_for', methods=["POST"])
def response_for(type_id, user_id):

    user_says = None
    #content_type = request.headers.get('Content-Type')
    #if (content_type == 'application/json; charset=utf-8'):
    user_says = request.json
    #else:
    #    return jsonify('/response_for request must have content_type == application/json')

    bot = Chatbot(
        database_file="/home/aldespin/chatbot/data/chatbot.db",
        type_id=type_id,
        user_id=user_id
    )
    assistant_says = bot.response_for(user_says)
    response = {
        "user_says": user_says,
        "assistant_says": assistant_says
    }
    return jsonify(response)

@app.route('/<type_id>/<user_id>/reset', methods=["DELETE"])
def reset(type_id, user_id):
    bot = Chatbot(
        database_file="/home/aldespin/chatbot/data/chatbot.db",
        type_id=type_id,
        user_id=user_id
    )
    bot.reset()
    response = bot.starter()
    return jsonify(response)