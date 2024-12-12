import threading
from django.core.mail import EmailMessage

class EmailThread(threading.Thread):
    def __init__(self, email:EmailMessage):
        self.email = email
        super().__init__()

    def run(self):
        self.email.send()

class Util:
    @staticmethod
    def send_email(email_data:dict):
        email = EmailMessage(
            to=[email_data['to_email']],
            subject = email_data['email_subject'],
            body = email_data['email_body'],
        )
        thread = EmailThread(email)
        thread.start()