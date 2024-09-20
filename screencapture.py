

import pyautogui
myScreenshot = pyautogui.screenshot()
myScreenshot.save("1.png")
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = 'dotnetdeveloper2022new@gmail.com'
smtp_password = 'mckokwceynfejezo'

from_email = 'dotnetdeveloper2022new@gmail.com'
to_email = 'parameshprogrammer@gmail.com'
subject = 'Email with attachment'
body = 'Intrusion Detected Alert.'

msg = MIMEMultipart()
msg['From'] = from_email
msg['To'] = to_email
msg['Subject'] = subject
msg.attach(MIMEText(body))

image_path = "1.png"
with open(image_path, "rb") as image_file:
    image = MIMEImage(image_file.read(), name="intrusion.png")
    msg.attach(image)


with smtplib.SMTP(smtp_server, smtp_port) as smtp:
    smtp.starttls()
    smtp.login(smtp_username, smtp_password)
    smtp.send_message(msg)
