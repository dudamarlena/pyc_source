# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kyzima-spb/www/django-projects/mosginfo/adminlte_full/messages.py
# Compiled at: 2016-04-14 15:57:27
# Size of source mod 2**32: 1771 bytes
import django.dispatch
from django.contrib.auth.models import User
from datetime import datetime, date

class Message(object):

    def __init__(self, sender=None, subject='', sent_at=None, recipient=None, uid=None):
        self._Message__sender = None
        self._Message__sent_at = None
        self._Message__recipient = None
        self._Message__uid = uid
        self.sender = sender
        self.subject = subject
        self.sent_at = sent_at or datetime.now()
        self.recipient = recipient

    @property
    def uid(self):
        return self._Message__uid

    @property
    def recipient(self):
        return self._Message__recipient

    @recipient.setter
    def recipient(self, recipient):
        if isinstance(recipient, User):
            self._Message__recipient = recipient

    @property
    def sent_at(self):
        return self._Message__sent_at

    @sent_at.setter
    def sent_at(self, sent_at):
        if not isinstance(sent_at, (date, datetime)):
            sent_at = datetime.strptime(sent_at, '%Y-%m-%d %H:%M:%S')
        self._Message__sent_at = sent_at

    @property
    def sender(self):
        return self._Message__sender

    @sender.setter
    def sender(self, sender):
        if isinstance(sender, User):
            self._Message__sender = sender


class MessagesList(object):
    show_signal = django.dispatch.Signal()

    def __init__(self):
        self._MessagesList__messages = []

    def add_message(self, message):
        if isinstance(message, Message):
            self._MessagesList__messages.append(message)

    @property
    def messages(self):
        return self._MessagesList__messages

    @messages.setter
    def messages(self, messages):
        for msg in messages:
            self.add_message(msg)

    @property
    def total(self):
        return len(self.messages)