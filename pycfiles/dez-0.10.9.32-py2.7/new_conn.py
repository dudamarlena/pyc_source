# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dez/samples/new_conn.py
# Compiled at: 2020-04-19 19:55:58
from dez.network import SocketClient, SocketDaemon, Connection
import sys

def main(**kwargs):
    server = SocketDaemon(kwargs['domain'], kwargs['port'], cb=TestCloseChunked)
    server.start()


class TestCloseChunked(object):

    def __init__(self, conn):
        self.conn = conn
        self.conn.set_rmode_close_chunked(self.data_received)

    def data_received(self, data):
        print data.replace('\r\n', '\\r\\n\n')


class TestClose(object):

    def __init__(self, conn):
        self.conn = conn
        self.conn.set_rmode_close(self.data_received)

    def data_received(self, data):
        print data.replace('\r\n', '\\r\\n\n')


class TestSizeChunked(object):

    def __init__(self, conn):
        self.conn = conn
        self.conn.set_rmode_size_chunked(15, self.data_received)

    def data_received(self, data):
        print data.replace('\r\n', '\\r\\n\n')


class TestSize(object):

    def __init__(self, conn):
        self.conn = conn
        self.conn.set_rmode_size(15, self.data_received)

    def data_received(self, data):
        print data.replace('\r\n', '\\r\\n\n')


class TestDelimiter(object):

    def __init__(self, conn):
        self.conn = conn
        self.conn.set_rmode_delimiter('\r\n', self.data_received)

    def data_received(self, data):
        print data