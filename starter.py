import os
import smtplib, imaplib
import time, datetime
import email, email.parser, email.utils

from bs4 import BeautifulSoup
from bs4 import Comment

# Main Settings
FROM_EMAIL  = os.environ['email_ramen']
FROM_PWD    = os.environ['gmail_pass']
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 993

# Extra Stuff
def setUpConnection():
    """ Connect to Server through Imap """
    mail = imaplib.IMAP4_SSL(SMTP_SERVER)
    mail.login(FROM_EMAIL,FROM_PWD)

    return mail


def gather_venmo_ids(mail):
    """ Return Emails with Venmo Subject in your Inbox"""
    mail.select('inbox')
    typ, data = mail.search(None, 'FROM', 'VENMO')

    mail_ids = data[0].split()
    
    return mail_ids

def parse_venmo_msgs(mail, mail_ids):
    """ Parse Through Emails """
    
    for i in mail_ids[-10:]:            
        typ, msg_data = mail.fetch(i, '(RFC822)' )
        

        for response_part in msg_data:
            if isinstance(response_part, tuple):
                email_parser = email.parser.BytesFeedParser()
                email_parser.feed(response_part[1])
                msg = email_parser.close()

                # print(msg)
                # Check if we have a standard Venmo Subject line
                message_subject = msg['SUBJECT']
                if "paid you" in message_subject:
                    
                    typ, msg_data = mail.fetch(i, '(BODY.PEEK[TEXT])')
                    for response_part in msg_data:
                        if isinstance(response_part, tuple):
                            full_msg = response_part[1]
                            soup=BeautifulSoup(full_msg,'html.parser')
                            note= soup.find("p")
                            print(note.text)
                            # print(note.text[0:2])

                    # get the timestamp
                    # timestamp = msg["Received"].split(";")[1].strip()
                    # # print(timestamp)
                    # parsedate = email.utils.parsedate(timestamp)
                    # # Time logic 
                    # current_time = time.mktime(time.localtime())
                    # email_time = time.mktime(parsedate)

                    # if email_time < current_time:
                    doSomething(msg, message_subject)

def main():
    try:
        mail = setUpConnection()
        mail_ids = gather_venmo_ids(mail)
        parse_venmo_msgs(mail, mail_ids)

    except Exception as e:
        print(str(e))



def doSomething(msg, message):
    string = message.split(" ")
    index = string.index("paid")
    person = " ".join(string[:index])

    # print(msg)
    

if __name__ == "__main__":
    main()
