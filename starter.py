import os
import smtplib
import time
import imaplib
import email



ORG_EMAIL   = "@gmail.com"
FROM_EMAIL  = "test" + ORG_EMAIL
FROM_PWD    = os.environ['gmail_pass']
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 993

# -------------------------------------------------
#
# Utility to read email from Gmail Using Python
#
# ------------------------------------------------

def read_email_from_gmail():
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')

        type, data = mail.search(None, 'FROM', 'VENMO')
        mail_ids = data[0].split()
        
        for i in mail_ids[-1:]:            
            typ, data = mail.fetch(i, '(RFC822)' )
            print(data)
            # print(typ, data)
#             for response_part in data:
#                 if isinstance(response_part, tuple):
#                     msg = email.message_from_string(response_part[1])
#                     email_subject = msg['subject']
#                     email_from = msg['from']
#                     print('From : ' + email_from + '\n')
#                     print('Subject : ' + email_subject + '\n')
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    read_email_from_gmail()
