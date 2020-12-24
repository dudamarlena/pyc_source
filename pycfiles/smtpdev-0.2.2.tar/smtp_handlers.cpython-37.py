# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/asyncee/projects/smtpdev/smtpdev/smtp_handlers.py
# Compiled at: 2019-06-17 12:18:47
# Size of source mod 2**32: 768 bytes
import datetime as dt
from email.utils import format_datetime
from aiosmtpd.handlers import Mailbox
from smtpdev.message_observer import MessageObserver
from .message_observer import MessageObservable

class MailboxHandler(Mailbox):

    def __init__(self, mail_dir, message_class=None):
        super().__init__(mail_dir, message_class)
        self._observable = MessageObservable()

    def register_message_observer(self, observer: MessageObserver):
        self._observable.register(observer)

    def handle_message(self, message):
        if message['Date'] is None:
            message['Date'] = format_datetime(dt.datetime.now())
        local_message_id = self.mailbox.add(message)
        self._observable.notify_observers(local_message_id, message)