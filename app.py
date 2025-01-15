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
from threading import Thread
from flask_wtf import CSRFProtect

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
csrf = CSRFProtect(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = User.validate_name(request.form.get('name'))
        username = User.validate_username(request.form.get('username'))
        email = User.validate_email(request.form.get('email'))
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')
        password_result = User.compare_passwords(password, confirm_password)
        user = {
            'name' : name[0],
            'username' : username[0],
            'email' : email[0],
            'password' : password_result[0],
            'status' : 'active'
        }
        account_status = User.check_for_account(**user)
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
        elif user_response.status_code == 404:
             user_id = session.sid
             redis_result = User.store_verification_code(redis_client, user_id)
             user['password'] = User.hash_password(password_result[0])
             User.register_account(
                 User(
                     name=name[0],
                     username=username[0],
                     email=email[0],
                     password=user['password'],
                     date_added=datetime.datetime.utcnow(),
                     status=user['status'],
                     accounts=[],
                     notes=[]
                ))
             email = {
                 'email' :  email[0],
                 'sender' : app.config['MAIL_USERNAME'],
                 'password' : app.config['MAIL_PASSWORD'],
                 'subject' : 'Guard Dog - E-mail verification',
                 'server' : app.config['MAIL_SERVER'],
                 'port' : app.config['MAIL_PORT'],
                 'template' : render_template('email_verification.html', name=User.format_name(name[0]), code=redis_result[0]['verification_code'])
             }
             Thread(name='email_verification', target=User.send_verification_code, args=(email,)).start()
             return redirect(url_for('verify_account'))
        elif user_response.status_code == 200:
            flash(account_status[0], 'error')
            return redirect(url_for('signin'))
    return render_template('home.html', title='Online Password Manager')

@app.route('/account-verification', methods=['GET', 'POST'])
def verify_account():
    verification_code = request.form.get('verification_code')
    if request.method == 'POST' and verification_code != '':
        verify_user = User.verify_verification_code(redis_client, f'user:{session.sid}')
        verify_user_response =  make_response(verify_user)
        if verify_user_response.status_code == 200:
           if verification_code == verify_user[0]:
               return redirect(url_for('account_manager'))
        else:
            flash(verify_user[0],'error')
    return render_template('account_verification.html')

@app.route('/sign-up', methods=['GET', 'POST'])
def signup():
    return render_template('home.html', title='Sign up')

@app.route('/sign-in', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = User.validate_email(request.form.get('email'))
        email_response = make_response(email)
        if email_response.status_code == 200:
            user = User()
            result = User.retrieve_user_account(email[0])
            password_result = user.verify_password(request.form.get('password'), result['password'])
            password_response = make_response(password_result)
            if password_response.status_code == 200:
                user_id = session.sid
                redis_result = User.store_verification_code(redis_client, user_id)
                email = {
                    'email' :  email[0],
                    'sender' : app.config['MAIL_USERNAME'],
                    'password' : app.config['MAIL_PASSWORD'],
                    'subject' : 'Guard Dog - E-mail verification',
                    'server' : app.config['MAIL_SERVER'],
                    'port' : app.config['MAIL_PORT'],
                    'template' : render_template('email_verification.html', name=User.format_name(result.name), code=redis_result[0]['verification_code'])
                }
                Thread(name='email_verification', target=User.send_verification_code, args=(email,)).start()
                return redirect(url_for('verify_account'))
            else:
                flash(password_result[0], 'error')
        else:
           flash(email[0], 'error')
    return render_template('signin.html', title='Sign in')

@app.route('/sign-out')
def signout():
    session.clear()
    return render_template('signout.html')

@app.route('/timed-out')
def timeout():
    return 'You\'ve been timed out', 200


@app.route('/account-manager', methods=['GET'])
def account_manager():
    #check session id to see if they are logged in on every route
    session_result = User.check_session_status(redis_client, session.sid)
    if session_result and request.method == 'GET':
        return render_template('accounts.html'), 200
    else:
        return redirect(url_for('timeout')), 301


@app.route('/account-manager/item/<id>')
def get_item():
    pass

@app.route('/account-manager/add-item')
def add_item():
    return render_template('account.html')

@app.route('/account-manager/edit-item/<id>')
def edit_item(id):
    pass

@app.route('/account-manager/remove-item/<id>')
def delete_item(id):
    pass

@app.route('/settings')
def settings():
    pass

@app.route('/password-generator', methods=['GET', 'POST'])
def password_generator():
    #make sure number is not negative
    password_length = request.form.get('password-length')
    character_type = request.form.get('character-type')
    if request.method == 'POST' and password_length != '' and  character_type != '':
        if password_length.isnumeric() and int(password_length) < 48:
            password = User.generate_password(int(password_length), character_type.upper())
            return render_template('password_generator.html', user_password=password)
        else:
           flash('Password length must be numbers and no longer than 48 characters', 'error')
    return render_template('password_generator.html')

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






if __name__ == '__main__':
    scheduler.init_app(app)
    scheduler.start()
    app.run()
