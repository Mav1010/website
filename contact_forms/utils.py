import sendgrid
from sendgrid.helpers.mail import *

from django.conf import settings


def send_email_sendgrid(from_email, to_email, subject, content_type, content):
    sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
    mail = Mail(Email(from_email), subject, Email(to_email), Content(content_type, content))
    response = sg.client.mail.send.post(request_body=mail.get())