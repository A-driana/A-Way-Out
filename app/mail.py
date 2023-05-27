import ssl
import smtplib
from email.message import EmailMessage
from app.config import settings


def send_mail(msg, user_email):
    sender = settings.sender
    pswd = settings.pswd
    rec = user_email

    subject = ' notification'

    body = 'hi'
    em = EmailMessage()
    em['From'] = sender
    em['To'] = rec
    em['Subject'] = subject
    em.set_content(msg)

    c = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com',) as smtp:
        smtp.login(sender, pswd)
        smtp.sendmail(sender, rec, em.as_string())
        print('done')
