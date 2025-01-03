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

    def update_account(data):
        data.update()
        return 'Account updated', 200

    def retrieve_account(user, id):
        try:
           return [account for account in user.accounts if id in account['id']]
        except AttributeError:
           return 'Account does not exist',404

    def retrieve_accounts(user):
        try:
            return user.accounts
        except AttributeError:
            return 'No accounts', 404
