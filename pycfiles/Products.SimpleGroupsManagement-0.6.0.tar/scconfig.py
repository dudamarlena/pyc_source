# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/Products/SimpleChat/scconfig.py
# Compiled at: 2011-05-21 08:16:29
admin_emails = [
 'morten@nidelven-it.no']
import smtplib

def send_email(email):
    smtp = smtplib.SMTP('localhost')
    smtp.sendmail(admin_emails[0], admin_emails, email)