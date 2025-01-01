from mongoframes import *
from datetime import datetime

class Note(SubFrame):
    _fields = {
        'id',
        'title',
        'category',
        'note',
        'priority',
        'date_added'
    }
