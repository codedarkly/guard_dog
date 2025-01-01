from flask import Flask, render_template, redirect, url_for
from mongoframes import *
from pymongo import MongoClient
from models.account import Account
from models.note import Note
from models.user import User
from models.notification import Notification
from dotenv import load_dotenv
from datetime import datetime, date, timedelta
import datetime
import os
import uuid
from flask_redis import FlaskRedis
import smtplib
from email.message import EmailMessage


load_dotenv('.env')

app = Flask(__name__)
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
app.config['REDIS_URL'] =os.environ.get('REDIS_URL')
Frame._client = MongoClient(app.config['MONGO_URI'])
redis_client = FlaskRedis(app)


@app.route('/')
def index():
    pass


@app.route('/sign-up')
def signup():
    pass

@app.route('/sign-in')
def signin():
    pass

@app.route('/sign-out')
def signout():
    pass

@app.route('/settings')
def settings():
    pass

@app.route('/password-generator')
def password_generator():
    pass

@app.route('/notes')
def notes():
    pass

@app.route('/notes/item/<id>')
def get_note():
    pass

@app.route('/notes/add-item')
def add_note():
    pass

@app.route('/notes/edit-item/<id>')
def edit_note():
    pass

@app.route('/notes/remove-item/<id>')
def remove_note():
    pass

@app.route('/account-manager')
def account_manager():
    pass

@app.route('/account-manager/item/<id>')
def get_item():
    pass

@app.route('/account-manager/add-item')
def add_item():
    pass

@app.route('/account-manager/edit-item/<id>')
def edit_item(id):
    pass

@app.route('/account-manager/remove-item/<id>')
def delete_item(id):
    pass


if __name__ == '__main__':
    app.run()
