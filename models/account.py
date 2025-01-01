from mongoframes import *
from datetime import datetime


class Account(SubFrame):
    _fields = {
        'id',
        'name',
        'category',
        'password',
        'account_note',
        'date_added'
    }
