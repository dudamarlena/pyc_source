# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sslmanage/mail.py
# Compiled at: 2019-07-05 06:11:56
# Size of source mod 2**32: 865 bytes
import smtplib
from email.mime.text import MIMEText
from email.header import Header

class Mail:

    def __init__(self, smtp_host, smtp_prot, smtp_user, smtp_pass, receiver_mail):
        self.smtp = None
        self.smtp_user = smtp_user
        self.receiver_mail = receiver_mail
        self.smtp = smtplib.SMTP_SSL(smtp_host, smtp_prot)
        self.smtp.login(smtp_user, smtp_pass)

    def send_mail(self, msg):
        message = MIMEText(msg, 'html', 'utf-8')
        message['From'] = Header('ssl更新', 'utf-8')
        message['To'] = Header('管理员', 'utf-8')
        subject = 'ssl更新'
        message['Subject'] = Header(subject, 'utf-8')
        if isinstance(self.receiver_mail, str):
            self.receiver_mail = [
             self.receiver_mail]
        self.smtp.sendmail(self.smtp_user, self.receiver_mail, message.as_string())