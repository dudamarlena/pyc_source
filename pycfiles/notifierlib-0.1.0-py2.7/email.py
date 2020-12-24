# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/notifierlib/channels/email.py
# Compiled at: 2017-09-18 11:03:39
"""Email module file"""
from emaillib import EasySender
from notifierlib.notifierlib import Channel
__author__ = 'Costas Tyfoxylos <costas.tyf@gmail.com>'
__docformat__ = 'plaintext'
__date__ = '18-09-2017'

class Email(Channel):

    def __init__(self, name, sender, recipient, smtp_address, username=None, password=None, tls=False, ssl=True, port=587):
        super(Email, self).__init__()
        self.name = name
        self.recipient = recipient
        self.sender = sender
        self.email = EasySender(smtp_address=smtp_address, username=username, password=password, ssl=ssl, tls=tls, port=port)

    def notify(self, **kwargs):
        result = self.email.send(sender=self.sender, recipients=self.recipient, subject=kwargs.get('subject'), body=kwargs.get('message'))
        if not result:
            self._logger.error('Failed sending email')
        return result