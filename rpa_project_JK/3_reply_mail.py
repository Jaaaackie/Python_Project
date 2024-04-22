import smtplib
from account import *
from imap_tools import MailBox
from email.message import EmailMessage

max_val = 3
applicant_list = []

print("[1. Suche nach E-Mails von Bewerbern]")
with MailBox("imap.googlemail.com", 993).login(EMAIL_ADDRESS, EMAIL_PASSWORD, initial_folder = "INBOX") as mailbox:
    idx = 1
    for msg in mailbox.fetch('(SENTSINCE 03-Aug-2023)'):
        if "Anmeldung zum Pythonkurs" in msg.subject:
            name, phone = msg.text.strip().split("/")
            
            applicant_list.append((msg, idx, name, phone))
            idx += 1

print("[2. Auswahl / Absagenbenachrichtigungs-E-Mail schicken]")
with smtplib.SMTP("smtp.googlemail.com", 587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    for applicant in applicant_list:
        to_addr = applicant[0].from_
        idx, name, phone = applicant[1:]

        title = None
        content = None

        if idx <= max_val:
            title = "Hinweis zum Pythonkurs [Ausgewählt]"
            content = "Herzlichen Glückwunsch, Herr oder Frau {}. Sie wurden als Teilnehmer für den Kurs ausgewählt. (Auswahlreihenfolge Nr. {})".format(name, idx)
        else: 
            title = "Hinweis zum Pythonkurs [Nicht ausgewählt]"
            content = "Leider wurden Sie, Herr oder Frau {}, nicht ausgewählt. Sollten Absagen eintreffen, werden wir Sie kontaktieren. (Wartelistenreihenfolge Nr. {})".format(name, idx - max_val)

        msg = EmailMessage()
        msg["Subject"] = title
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to_addr
        msg.set_content(content)
        smtp.send_message(msg)

        print("Der Versand der E-Mail an " + name + " ist abgeschlossen")