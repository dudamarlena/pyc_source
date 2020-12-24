# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/SimpleChat/scconfig.py
# Compiled at: 2011-06-02 04:49:39
admin_emails = [
 'morten@nidelven-it.no']
import smtplib

def send_email(email):
    smtp = smtplib.SMTP('localhost')
    smtp.sendmail(admin_emails[0], admin_emails, email)