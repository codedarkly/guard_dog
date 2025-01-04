from mongoframes import Frame, Q
from datetime import datetime
import random
import re
import smtplib
from email.message import EmailMessage
from passlib.hash import pbkdf2_sha256


class User(Frame):
    _fields = {
        'name',
        'username',
        'email',
        'password',
        'date_added',
        'status',
        'accounts',
        'notes'
    }

    def is_user_signed_in(user_status):
        #check to see if user still has a session(make this a decorator)
        #def wrapper():
        #    if user_status
        #return wrapper
        pass

    @staticmethod
    def validate_name(name):
        return (name, 200) if re.match('^[a-zA-Z\s]+$', name) else ('Name is invalid', 401)

    @staticmethod
    def validate_username(username):
        return (username, 200) if re.match('^[a-zA-Z0-9]+$', username) else ('Name is invalid', 401)

    @staticmethod
    def validate_email(email):
        email_pattern = re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email)
        return (email, 200) if email_pattern else ('E-mail address is not valid', 401)

    @staticmethod
    def register_account(user):
        result =  User.one(Q.email == user.email)
        if result is not None:
           return 'User exists', 409
        else:
           user.insert()
           return 'User registered', 200

    @staticmethod
    def compare_passwords(password, confirm_password):
        return (password, 200) if password == confirm_password else ('Passwords do not match', 401)

    @staticmethod
    def hash_password(password):
        return pbkdf2_sha256.hash(password)

    def verify_password(self,password,hashed_password):
        #get user from database and compare it against their enter password(use check_user_account())
        return pbkdf2_sha256.verify(password, hashed_password)

    @staticmethod
    def generate_password(length):
        characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-&'
        return ''.join(random.choice(characters) for _ in range(length))

    @classmethod
    def generate_verification_code(cls):
        return User.generate_password(8)

    @classmethod
    def store_verification_code(cls, rc, user_id):
        #store the generated verification code in the cache(temporarily)
        user  = {'verification_code' : User.generate_verification_code()}
        user_data = f'user:{user_id}'
        rc.hset(user_data, mapping=user)
        rc.expire(user_data, 900)
        result = rc.hgetall(user_data)
        return {k.decode():v.decode() for k,v in result.items()}, 200

    @classmethod
    def verify_verification_code(cls, rc, user_id):
        try:
            result = rc.hgetall(user_id)
            data = {k.decode():v.decode() for k,v in result.items()}
            return (data['verification_code'], 200)
        except KeyError:
            return 'Verification code or username is incorrect or your passcode has expired', 401

    @staticmethod
    def send_verification_code(mail_settings):
        message = EmailMessage()
        message['to'] = mail_settings['email']
        message['from'] = mail_settings['sender']
        message['subject'] = mail_settings['subject']
        message.set_content(mail_settings['template'], subtype='html')
        with smtplib.SMTP_SSL(mail_settings['server'], mail_settings['port']) as smtp:
            smtp.login(mail_settings['sender'], mail_settings['password'])
            smtp.send_message(message)
        return 'message sent', 200

    @staticmethod
    def update_user_account(user):
        user.update()
        return 'User account updated',204

    @classmethod
    def retrieve_user_account(cls, **user):
        if u := User.one(Q.email == user['email']) is not None:
            return ('User exists', 200)
        else:
            return ('User does not exist', 404)

    def deactivate_account(user):
        try:
           u = User.one({'email' : user.email, 'password' : user.password})
           u.status = 'inactive'
           u.update()
           return 'User account deactivated', 404
        except AttributeError:
           return 'User does not exist', 404
