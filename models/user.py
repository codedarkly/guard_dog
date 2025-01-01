from mongoframes import *
from datetime import datetime

class User(Frame):
    _fields = {
        'name',
        'email',
        'password',
        'accounts',
        'notes'
    }
