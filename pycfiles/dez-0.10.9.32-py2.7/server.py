# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dez/stomp/server/server.py
# Compiled at: 2020-04-19 19:55:58
from dez.network.server import SocketDaemon
from dez.stomp.server.connection import STOMPConnection
from dez.stomp.server.validator import STOMPValidator

class STOMPServer(object):

    def __init__(self, addr, port):
        self.__val = STOMPValidator()
        self.__server = SocketDaemon(addr, port, self.__connect_cb)
        self.__app_connect_cb = None
        return

    def start(self):
        self.__server.start()

    def set_connect_cb(self, cb):
        self.__app_connect_cb = cb

    def __connect_cb(self, c):
        if self.__app_connect_cb:
            return self.__app_connect_cb(STOMPConnection(c, self.__val))
        print 'Application server not available'