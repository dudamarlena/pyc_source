# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kalimaha/Development/git-repositories/Geobricks/pgeo/pgeo/utils/email_utils.py
# Compiled at: 2014-08-28 10:11:21
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(user, to, pwd, header, body, smtp='smtp.gmail.com', smtp_port=587):
    to = to
    gmail_user = user
    gmail_pwd = pwd
    smtpserver = smtplib.SMTP(smtp, smtp_port)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(gmail_user, gmail_pwd)
    msg = MIMEMultipart('alternative')
    msg['Subject'] = header
    msg['From'] = gmail_user
    msg['To'] = to
    part = MIMEText(body, 'html')
    msg.attach(part)
    smtpserver.sendmail(gmail_user, to, msg.as_string())
    smtpserver.close()