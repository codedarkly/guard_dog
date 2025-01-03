from flask import Flask, render_template, redirect, url_for, session, request, make_response, flash
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
from flask_apscheduler import APScheduler
from flask_session import Session

load_dotenv('.env')

app = Flask(__name__)
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
app.config['REDIS_URL'] = os.environ.get('REDIS_URL')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_TEST_RECIPIENT'] = os.environ.get('MAIL_TEST_RECIPIENT')
app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL')
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS')
app.config['SCHEDULER_API_ENABLED'] = os.environ.get('SCHEDULER_API_ENABLED')
app.config['SESSION_TYPE'] = os.environ.get('SESSION_TYPE')
app.config['SESSION_PERMANENT'] = os.environ.get('SESSION_PERMANENT')
app.config['SESSION_USE_SIGNER'] = os.environ.get('SESSION_USE_SIGNER')
app.config['SESSION_REDIS'] = os.environ.get('REDIS_URL')
Frame._client = MongoClient(app.config['MONGO_URI'])
redis_client = FlaskRedis(app)
scheduler = APScheduler()
fk_session = Session(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = User.validate_name(request.form.get('name'))
        username = User.validate_username(request.form.get('username'))
        email = User.validate_email(request.form.get('email'))
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')
        password_result = User.compare_passwords(password, confirm_password)
        user = User(name=name, email=email,password=password, status='active')
        account_status = user.retrieve_user_account()
        name_response = make_response(name)
        username_response = make_response(username)
        email_response = make_response(email)
        password_response = make_response(password_result)
        user_response = make_response(account_status)
        if name_response.status_code == 401:
             flash(name[0], 'error')
        elif username_response.status_code == 401:
             flash(username[0], 'error')
        elif email_response.status_code == 401:
             flash(email[0], 'error')
        elif password_response.status_code == 401:
             flash(password_result[0], 'error')
        if user_response.status_code == 404:
             return redirect(url_for('verify_account'))
        else:
             flash(account_status[0], 'error')

    return render_template('home.html', title='Online Password Manager')

@app.route('/account-verification')
def verify_account():
    return 'verify account', 200


@app.route('/sign-up')
def signup():
    return render_template('signup.html', title='Sign up')

@app.route('/sign-in')
def signin():
    return render_template('signin.html', title='Sign in')

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
    scheduler.init_app(app)
    scheduler.start()
    app.run()
