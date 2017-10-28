import os
import smtplib, imaplib
import time, datetime
import email, email.parser, email.utils
import dateutil.parser, datetime, pytz
import re

from bs4 import BeautifulSoup
from bs4 import Comment
from subprocess import call

# Main Settings
FROM_EMAIL  = os.environ['email_ramen']
FROM_PWD    = os.environ['gmail_pass']
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 993
DEBUG = True

# Extra Stuff
def setUpConnection():
    """ Connect to Server through Imap """
    mail = imaplib.IMAP4_SSL(SMTP_SERVER)
    mail.login(FROM_EMAIL,FROM_PWD)

    print("Mail Connection Complete")
    return mail


def gather_venmo_ids(mail):
    """ Return Emails with Venmo Subject in your Inbox"""
    mail.select('inbox')
    # Gather any email with "paid you" subject line
    typ, data = mail.search(None, '(SUBJECT "paid you")', 'FROM', 'VENMO')
    mail_ids = data[0].split()
    
    print("Venmo Ids Gathered")
    return mail_ids

def parse_venmo_msgs(mail, mail_ids, ramen_bank):
    """ Parse Through Emails """
    
    for i in mail_ids[-10:]:            
        typ, msg_data = mail.fetch(i, '(BODY.PEEK[TEXT])')
        typ2, msg_data_2 = mail.fetch(i, '(BODY[HEADER])')

        # Get the Subject Line
        for response_part in msg_data_2:
            if isinstance(response_part, tuple):
                email_parser2 = email.parser.BytesFeedParser()
                email_parser2.feed(response_part[1])
                msg2 = email_parser2.close()
                subject = msg2["SUBJECT"]
                timestamp = msg2["Received"].split(";")[1].strip()
                timestamp = dateutil.parser.parse(timestamp)
                #print(msg2["SUBJECT"])

        # Get the note
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                full_msg = response_part[1]
                soup=BeautifulSoup(full_msg,'html.parser')
                note= soup.find("p").text
                #print(note.text)

        print("Starting to parse name, amount, and more")
        parseGoods(subject, note, timestamp, ramen_bank) 


def parseGoods(subject, note, timestamp, ramen_bank):
    """ Gather the Name, Amount, and Note """
   
    email_time=timestamp + datetime.timedelta(hours=1) 
    current_time=datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)-datetime.timedelta(hours=8)
    if email_time >= current_time or DEBUG:
        print("Time is current at {}".format(email_time))
        subject_list = subject.split(" ")
        
        # Name Parsing
        index_paid = subject_list.index("paid")
        name = " ".join(subject_list[:index_paid])

        # Amount Parsing
        index_you = subject_list.index("you") +1
        amount = " ".join(subject_list[index_you:])
        amount = float(amount[1:])

        print("{} {:.2f} ".format(name, amount))
        
        # Note Parsing
        total_paid = amount
        orders = [order for order in note.split() if len(order)==2]
        for order in orders:
            if order in ramen_bank:
                if total_paid - cost  >= 0:
                    cost = ramen_bank[order]
                    total_paid -= cost
                    # call(["./ramen_swag", "-k", order])
                    print('Order filled {} '.format(order))
                else: 
                    print("Insufficient Funds Bro, Chill")
        print("Motor Logic Completed")
    else:
        print("Time too old {}".format(email_time))
    
def mainLoop():
    ramen_bank = {}
    try:
        mail = setUpConnection()
        mail_ids = gather_venmo_ids(mail)
        parse_venmo_msgs(mail, mail_ids, ramen_bank)

    except Exception as e:
        print(str(e))

def main():
    mainLoop()
    time.sleep(1)

if __name__ == "__main__":
    main()
