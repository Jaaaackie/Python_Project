import smtplib
from account import *
from imap_tools import MailBox
from email.message import EmailMessage

max_val = 3 # Anzahl an maximalen Ausgewählten
applicant_list = [] # Bewerberliste

print("[1. Suche nach E-Mails von Bewerbern]")
with MailBox("imap.googlemail.com", 993).login(EMAIL_ADDRESS, EMAIL_PASSWORD, initial_folder = "INBOX") as mailbox:
    idx = 1 # E-Mail Ankunftsreihenfolge
    # Das Datum wird basierend auf GMT eingesetzt.
    for msg in mailbox.fetch('(SENTSINCE 03-Aug-2023)'): # Suche nach E-Mails nach dem 22. April 2024
        if "Pythonkurs" in msg.subject: # Überprüfung, ob E-Mails mit dem Betreff "Anmeldung zum Pythonkurs" vorhanden sind
            name, phone = msg.text.strip().split("/") # Verwendung von strip() zur Entfernung unnötiger Leerzeichen
            # print("Reihenfolge : {}, Name : {}, Kontaktnr. : {}".format(idx, name, phone))
            applicant_list.append((msg, idx, name, phone))
            idx += 1


print("[2. Auswahl / Absagenbenachrichtigungs-E-Mail schicken]")
with smtplib.SMTP("smtp.googlemail.com", 587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    for applicant in applicant_list:
        to_addr = applicant[0].from_ # E-Mail-Adresse von Empfängern
        # idx = applicant[1]
        # name = applicant[2]
        # phone = applicant[3]
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