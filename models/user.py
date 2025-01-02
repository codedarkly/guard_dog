from mongoframes import *
from datetime import datetime
import random
import string
import re
from passlib.hash import pbkdf2_sha256

class User(Frame):
    _fields = {
        'name',
        'email',
        'password'
        'date_added',
        'accounts',
        'notes'
    }

    @staticmethod
    def validate_email(email):
        email_pattern = re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email)
        return email if email_pattern else 'E-mail address is not valid', 401

    @staticmethod
    def validate_name(name):
        return name if re.match('^[a-zA-Z\s]+$', name) else 'Name is invalid', 401


    def check_user_account():
        pass

    def hash_password(self, password):
        return pbkdf2_sha256.hash(password)

    def verify_password(self,password,hashed_password):
        #get user from database and compare it against their enter password(use check_user_account())
        return pbkdf2_sha256.verify(password, hashed_password)

    @staticmethod
    def generate_verification_code():
        return generate_password(8)

    def store_verification_code(self, rc, user):
        user['verification_code'] = generate_verification_code()
        user_data = f'username:{user["username"]}'
        rc.hset(user_data, mapping=user)
        rc.expire(user_data, 900)
        result = rc.hgetall(user_data)
        return {k.decode():v.decode() for k,v in result.items()}, 200

    def verify_verification_code(self, rc, **user):
        try:
            result = rc.hgetall(user['username'])
            data = {k.decode():v.decode() for k,v in result.items()}
            return data['verification_code']
        except KeyError:
            return 'Verification code or username is incorrect or your passcode has expired', 401

    def email_verification_code():
        pass

    def register_user():
        pass

    def update_user_account():
       pass

    def retrieve_user_account():
       pass

    def deactivate_account():
        pass

    @staticmethod
    def generate_password(length):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
