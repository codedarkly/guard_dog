from mongoframes import *
from datetime import datetime, date, timedelta


class Account(SubFrame):
    _fields = {
        'id',
        'name',
        'category',
        'email',
        'password',
        'account_note',
        'date_added',
        'due_date',
        'amount',
        'priority',
        'autopay',
        'notifications'
    }

    def save_due_date(self, bill_date):
        #add 30 to the date given: bill_date + timedelta(days=30)
        pass
