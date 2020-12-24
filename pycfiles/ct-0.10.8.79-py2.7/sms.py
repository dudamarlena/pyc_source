# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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