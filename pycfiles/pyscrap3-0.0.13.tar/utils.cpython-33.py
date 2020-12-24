# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jorge/pyscrap3/pyscrap3/utils.py
# Compiled at: 2014-05-16 18:12:19
# Size of source mod 2**32: 1109 bytes
from kombu import Connection
from urllib.parse import quote_plus

class rabbitMsg:
    __doc__ = "Envía mensajes a traves de rabbitmq usando 'kombu'\n    https://pypi.python.org/pypi/kombu"

    def __init__(self, queue, user='guest', passw='guest', host='localhost'):
        self.user = user
        self.passw = quote_plus(passw)
        self.host = host
        self.urlRabbit = 'amqp://' + self.user + ':' + self.passw + '@' + host + '/'
        self.queueName = queue
        self.open()

    def open(self):
        self.conn = Connection(self.urlRabbit)
        self.cola = self.conn.SimpleQueue(self.queueName)

    def send(self, message):
        self.cola.put(message)

    def get(self):
        message = self.cola.get(block=True)
        result = message.payload
        message.ack()
        return result

    def getIfExists(self):
        message = self.cola.queue.get()
        if message:
            result = message.payload
            message.ack()
            return result
        else:
            return
            return

    def close(self):
        self.cola.close()