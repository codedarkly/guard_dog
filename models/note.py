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

    def add_note():
        pass

    def remove_note():
        pass

    def retrieve_note():
        pass

    def retrieve_notes():
        pass

    def edit_note():
        pass
