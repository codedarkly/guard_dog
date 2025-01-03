from mongoframes import *
from flask_apscheduler import APScheduler
import smtplib
from email.message import EmailMessage

class Notification(SubFrame):
    _fields = {
        'type',
        'notification_date',
        'frequency'
    }


    def send_reminder(reminder_message, username, password, server, port):
        with smtplib.SMTP_SSL(server, port) as smtp:
            smtp.login(username, password)
            smtp.send_message(reminder_message)
        return 'Reminder sent', 200

    def reminder_email(**data):
        #send as reminder email to user
        reminder_message = EmailMessage()
        reminder_message['to'] = data['recipient']
        reminder_message['from'] = data['sender']
        reminder_message['subject'] = 'Reminder to pay Netflix'
        reminder_message.set_content(data['template'], subtype='html')
        return [reminder_message, data['username'], data['password'], data['server'], data['port']]


    @staticmethod
    def schedule_notification(scheduler, notification_date, **data):
        #set notification date and frequency
        reminder_msg = Notification.reminder_email(**data)
        scheduler.add_job(
            func=Notification.send_reminder,
            trigger='interval',
            days=notification_date,
            id='set_reminder',
            args=[
                reminder_msg[0],
                reminder_msg[1],
                reminder_msg[2],
                reminder_msg[3],
                reminder_msg[4]
            ]
        )
        return 'Notification set', 200

    def add_notification(user, notification):
        user.accounts.notifications.append(notification)
        user.update()
        return 'Notification saved', 200

    @staticmethod
    def update_notification(user, account_id, notification):
        result = [account for account in user['accounts'] if account_id in account['id']][0]
        result['notifications'].append(notification)
        user.update()
        return 'Notification updated', 200
