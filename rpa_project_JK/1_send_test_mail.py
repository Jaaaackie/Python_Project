import smtplib
from random import *
from account import *
from email.message import EmailMessage

names = ["Anton", "Berta", "Caesar", "Dora", "Emil"]

with smtplib.SMTP("smtp.googlemail.com", 587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    for name in names:
        msg = EmailMessage()
        msg['Subject'] = "Anmeldung zum Pythonkurs"
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = "applicant@googlemail.com"

        # content = name + "/" + str(randint(1000, 9999))
        content = "/".join([name, str(randint(1000, 9999))])
        msg.set_content(content)

        smtp.send_message(msg)
        
        print("E-Mail von " + name + " wurde erfolgreich an JK versendet")