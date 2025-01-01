from mongoframes import *


class Notification(SubFrame):
    _fields = {
        'type',
        'notification_date',
        'frequency'
    }

    def save_notification_date(self, notification_date):
        pass
