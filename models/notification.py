from mongoframes import *


class Notification(SubFrame):
    _fields = {
        'type',
        'notification_date',
        'frequency'
    }

    def schedule_notification(self, notification_date):
        #set notification date and frequency
        pass

    def update_notification():
        pass
