# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dnsmon/mailer.py
# Compiled at: 2011-03-21 18:00:36
import smtplib, settings
from email.mime.text import MIMEText

class Mailer:

    def __init__(self, To, From, Subject, Message):
        msg = MIMEText(Message)
        msg['Subject'] = Subject
        msg['From'] = From
        msg['To'] = (', ').join(To)
        s = smtplib.SMTP(settings.mail_host, settings.mail_port)
        if settings.mail_use_TLS is True:
            s.starttls()
        if settings.mail_username is not None and settings.mail_password is not None:
            s.login(settings.mail_username, settings.mail_password)
        s.sendmail(From, To, msg.as_string())
        s.quit()
        return