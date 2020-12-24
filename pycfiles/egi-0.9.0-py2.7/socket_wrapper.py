# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/egi/socket_wrapper.py
# Compiled at: 2016-09-08 05:35:24
import socket

class Socket:
    """ wrap the socket() class """

    def connect(self, str_address, port_no):
        """ connect to the given host at the specified port ) """
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((str_address, port_no))
        self._connection = self._socket.makefile('rwb', 0)

    def disconnect(self):
        """ close the connection """
        self._connection.close()
        self._socket.close()
        del self._connection
        del self._socket

    def write(self, data):
        """ write to the socket -- the socket must be opened """
        self._connection.write(data)

    def read(self, size=-1):
        """ read from the socket; warning -- it blocks on reading! """
        if size < 0:
            return self._connection.read()
        else:
            return self._connection.read(size)