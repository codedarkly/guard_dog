from mongoframes import Frame, Q
from datetime import datetime
import random
import re
import smtplib
from email.message import EmailMessage
from passlib.hash import pbkdf2_sha256
from enum import Enum

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
    def format_name(name):
        #split a full name in two parts from the space character and return the first list item capitalized
        return name.split(' ')[0].capitalize()

    @staticmethod
    def validate_name(name):
        pattern = r'^[A-Za-z]+(?:\s+[A-Za-z]+)*$'
        return (name, 200) if re.match(pattern, name) else ('Name is invalid', 401)

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
        password_result = pbkdf2_sha256.verify(password, hashed_password)
        if password_result:
            return ('Password matches', 200)
        else:
            return ('Password is incorrect', 401)

    @staticmethod
    def generate_password(length, character_type):
        for character in (CharacterTypes):
            if character.name in character_type:
                return ''.join(random.choice(character.value) for _ in range(length))

    @classmethod
    def generate_verification_code(cls):
        return User.generate_password(8, 'ALPHANUMERIC')

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
    def check_for_account(cls, **user):
        if _ := User.one(Q.email == user['email']) is not None:
            return ('User exists', 200)
        else:
            return ('User does not exist', 404)

    @classmethod
    def retrieve_user_account(cls, email):
        user = User.one(Q.email == email)
        if user is not None:
            return user
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


class CharacterTypes(Enum):
    ALPHANUMERIC = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    NUMBERS = '0123456789'
    STRONG = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-&@$%*!(+)*'
