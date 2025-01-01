from mongoframes import *
from datetime import datetime

class User(Frame):
    _fields = {
        'name',
        'email',
        'password'
        'date_added',
        'accounts',
        'notes'
    }
