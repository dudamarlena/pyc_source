# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cantools/web/dez_server/sms.py
# Compiled at: 2019-08-05 00:35:42
from .mail import send_mail
from cantools import config
carriers = {'at&t': 'mms.att.net', 
   'verizon': 'vtext.com', 
   'tmobile': 'tmomail.net', 
   'sprint': 'page.nextel.com'}

def send_sms(number, subject='hello', body='goodbye', carrier='at&t'):
    send_mail(to='%s@%s' % (number, carriers[carrier]), subject=subject, body=body)