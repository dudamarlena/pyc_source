# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/asyncee/projects/smtpdev/smtpdev/message_observer.py
# Compiled at: 2019-06-17 12:18:47
# Size of source mod 2**32: 661 bytes
import abc, weakref
from mailbox import MaildirMessage
from typing import MutableSet

class MessageObserver(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def on_message(self, local_message_id: str, message: MaildirMessage):
        pass


class MessageObservable:

    def __init__(self) -> None:
        self._observers = weakref.WeakSet()

    def register(self, observer: MessageObserver):
        self._observers.add(observer)

    def notify_observers(self, local_message_id: str, message: MaildirMessage) -> None:
        for observer in self._observers:
            observer.on_message(local_message_id, message)