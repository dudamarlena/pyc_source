# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmitry.kovalenko/MyOwnMess/my_own_messenger/my_own_client/handlers.py
# Compiled at: 2018-01-18 12:51:49
# Size of source mod 2**32: 2814 bytes
from my_own_jim.config import MESSAGE
from PyQt5.QtCore import QObject, pyqtSignal
from my_own_jim.utils import get_message
from my_own_jim.core import Jim, JimResponse, JimMessage
from my_own_jim.exceptions import WrongParamsError, ToLongError, WrongActionError, WrongDictError, ResponseCodeError
from my_own_jim.config import *

class Receiver:
    __doc__ = 'Класс-получатель информации из сокета'

    def __init__(self, sock, request_queue):
        self.request_queue = request_queue
        self.sock = sock
        self.is_alive = False

    def process_message(self, message):
        """метод для обработки принятого сообщения, будет переопределен в наследниках"""
        pass

    def poll(self):
        self.is_alive = True
        while True:
            if not self.is_alive:
                break
            data = get_message(self.sock)
            try:
                jm = Jim.from_dict(data)
                if isinstance(jm, JimMessage):
                    self.process_message(jm)
                else:
                    self.request_queue.put(jm)
            except Exception as e:
                print(e)

    def stop(self):
        self.is_alive = False


class GuiReciever(Receiver, QObject):
    __doc__ = 'GUI обработчик входящих сообщений'
    gotData = pyqtSignal(str)
    finished = pyqtSignal(int)

    def __init__(self, sock, request_queue):
        Receiver.__init__(self, sock, request_queue)
        QObject.__init__(self)

    def process_message(self, message):
        """Обработка сообщения"""
        text = '{} >>> {}'.format(message.from_, message.message)
        self.gotData.emit(text)

    def poll(self):
        super().poll()
        self.finished.emit(0)