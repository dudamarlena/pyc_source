# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/drench/listener.py
# Compiled at: 2013-12-07 21:54:49
import socket
from abc import abstractmethod, ABCMeta

class Listener(object):
    __metaclass__ = ABCMeta

    def __init__(self, address='127.0.0.1', port=7000):
        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((address, port))
        self.sock.listen(5)
        print ('listening on {}:{}').format(address, port)

    @abstractmethod
    def read(self):
        pass

    def fileno(self):
        return self.sock.fileno()

    def write(self):
        pass