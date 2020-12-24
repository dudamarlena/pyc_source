# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: nexmo/utils.py
# Compiled at: 2013-07-01 09:59:48
from .libpynexmo.nexmomessage import NexmoMessage
from django.conf import settings

def send_message(to, message):
    """Shortcut to send a sms using libnexmo api.

    Usage:

    >>> from nexmo import send_message
    >>> send_message('+33612345678', 'My sms message body')
    """
    params = {'username': settings.NEXMO_USERNAME, 
       'password': settings.NEXMO_PASSWORD, 
       'type': 'unicode', 
       'from': settings.NEXMO_FROM, 
       'to': to, 
       'text': message.encode('utf-8')}
    sms = NexmoMessage(params)
    response = sms.send_request()
    return response