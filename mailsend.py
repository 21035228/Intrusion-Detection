import smtplib
import numpy as np
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def emailsend(tomail, message):
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    
    # start TLS for security
    s.starttls()
    
    # Authentication
    s.login("dotnetdeveloper2022new@gmail.com", "mckokwceynfejezo")

    # sending the mail
    s.sendmail("dotnetdeveloper2022new@gmail.com", tomail, message)
    
    # terminating the session
    s.quit()

def emailsendwithattachement(tomail):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'dotnetdeveloper2022new@gmail.com'
    smtp_password = 'mckokwceynfejezo'

    from_email = 'dotnetdeveloper2022new@gmail.com'
    to_email = tomail
    subject = 'Email with attachment'
    body = 'Intrusion Detected Alert.'

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body))

    image_path = "intrusion.png"
    with open(image_path, "rb") as image_file:
        image = MIMEImage(image_file.read(), name="intrusion.png")
        msg.attach(image)

    with smtplib.SMTP(smtp_server, smtp_port) as smtp:
        smtp.starttls()
        smtp.login(smtp_username, smtp_password)
        smtp.send_message(msg)