# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\despres\Desktop\reaper\scripts\reapy\reapy\tools\network\socket.py
# Compiled at: 2020-04-18 10:49:27
# Size of source mod 2**32: 2067 bytes
import socket

class Socket:
    __doc__ = '\n    Wrapped `socket` that can send and receive data of any length.\n    '

    def __init__(self, s=None):
        self._socket = socket.socket() if s is None else s
        self._socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    @staticmethod
    def _non_blocking(f):
        """
        Modify a socket method so that it returns `None` when time
        out is reached.
        """

        def g(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except socket.timeout:
                pass

        return g

    def accept(self, *args, **kwargs):
        connection, address = (self._socket.accept)(*args, **kwargs)
        connection = Socket(connection)
        return (connection, address)

    def bind(self, *args, **kwargs):
        return (self._socket.bind)(*args, **kwargs)

    def close(self, *args, **kwargs):
        return (self._socket.close)(*args, **kwargs)

    def connect(self, *args, **kwargs):
        return (self._socket.connect)(*args, **kwargs)

    def listen(self, *args, **kwargs):
        return (self._socket.listen)(*args, **kwargs)

    def recv(self, timeout=0.0001):
        """Receive data of arbitrary length."""
        self.settimeout(timeout)
        length = self._socket.recv(8)
        length = int.from_bytes(length, 'little')
        if length == 0:
            raise ConnectionAbortedError
        self.settimeout(None)
        return self._socket.recv(length, socket.MSG_WAITALL)

    def send(self, data):
        """Send data."""
        length = len(data).to_bytes(8, 'little')
        self._socket.sendall(length)
        self._socket.sendall(data)

    def settimeout(self, *args, **kwargs):
        return (self._socket.settimeout)(*args, **kwargs)

    def shutdown(self, *args, **kwargs):
        return (self._socket.shutdown)(*args, **kwargs)