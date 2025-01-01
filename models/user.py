from mongoframes import *
from datetime import datetime
import random
import string


class User(Frame):
    _fields = {
        'name',
        'email',
        'password'
        'date_added',
        'accounts',
        'notes'
    }

    def validate_email():
        pass

    def validate_name():
        pass

    def check_user_account():
        pass

    def hash_password():
        pass

    def verify_password():
        pass

    def generate_verification_code():
        pass

    def store_verification_code():
        pass

    def verify_verification_code():
        pass

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
