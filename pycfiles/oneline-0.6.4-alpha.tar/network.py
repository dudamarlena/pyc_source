# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: bson/network.py
# Compiled at: 2011-07-10 20:51:08
import socket
try:
    from cStringIO import StringIO
except ImportError as e:
    from StringIO import StringIO

from struct import unpack
from __init__ import dumps, loads

def _bintoint(data):
    return unpack('<i', data)[0]


def _sendobj(self, obj):
    """
        Atomically send a BSON message.
        """
    data = dumps(obj)
    self.sendall(data)


def _recvobj(self):
    """
        Atomic read of a BSON message.

        This function either returns a dict, None, or raises a socket error.

        If the return value is None, it means the socket is closed by the other side.
        """
    sock_buf = self.recvbytes(4)
    if sock_buf is None:
        return
    else:
        message_length = _bintoint(sock_buf.getvalue())
        sock_buf = self.recvbytes(message_length - 4, sock_buf)
        if sock_buf is None:
            return
        retval = loads(sock_buf.getvalue())
        return retval


def _recvbytes(self, bytes_needed, sock_buf=None):
    """
        Atomic read of bytes_needed bytes.

        This function either returns exactly the nmber of bytes requested in a
        StringIO buffer, None, or raises a socket error.

        If the return value is None, it means the socket is closed by the other side.
        """
    if sock_buf is None:
        sock_buf = StringIO()
    bytes_count = 0
    while bytes_count < bytes_needed:
        chunk = self.recv(min(bytes_needed - bytes_count, 32768))
        part_count = len(chunk)
        if part_count < 1:
            return
        bytes_count += part_count
        sock_buf.write(chunk)

    return sock_buf