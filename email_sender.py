import os
from email.message import EmailMessage
import ssl
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

email_sender = "sf4sf3sf2@gmail.com"
email_password = 'niqthxwlzyibstna'
email_receiver = "raginghelllfire@gmail.com"


subject = "Enter a Subject"
body = """
I will get the data later.
I was just testing it out.
"""

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)
#em.add_attachment =

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())