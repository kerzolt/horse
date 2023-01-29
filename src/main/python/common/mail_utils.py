import logging
import sys
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Logging
logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger('mail_service')

def send_mail(subject, text):
    sender = ''
    recipient = ''
    password = ''

    # Recup username et password
    for arg in sys.argv:
        if (arg.startswith("-s") or arg.startswith("--mail.sender")) and arg.find("=") >= 0:
            sender = arg[arg.find("=") + 1:]
        elif (arg.startswith("-p") or arg.startswith("--mail.password")) and arg.find("=") >= 0:
            password = arg[arg.find("=") + 1:]
        elif (arg.startswith("-r") or arg.startswith("--report.recipient")) and arg.find("=") >= 0:
            recipient = arg[arg.find("=") + 1:]
    if sender == '' or password == '':
        LOGGER.error("Envoi du mail impossible : sender ou password vide")
        return
    if recipient == '':
        recipient = sender

    message = MIMEMultipart("alternative")
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message.attach(MIMEText(text, "html"))

    # Send mail
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, recipient, message.as_string())