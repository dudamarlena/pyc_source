# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/paraproxy/WrapSock.py
# Compiled at: 2011-05-24 05:02:49
import socket

class WrapSock(object):
    """
        Wrap a unix domain socket into a file-like object.
        """
    __module__ = __name__

    def __init__(self, sock):
        self._sock = sock

    def __getattribute__(self, attr):
        try:
            return super(WrapSock, self).__getattribute__(attr)
        except AttributeError:
            return super(WrapSock, self).__getattribute__('_sock').__getattribute__(attr)

    def dup(self):
        return WrapSock(self._sock.dup())

    def read(self, *args):
        return self._sock.recv(*args)

    def write(self, *args):
        return self._sock.send(*args)