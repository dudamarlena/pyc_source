# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\supervisor\medusa\text_socket.py
# Compiled at: 2015-07-18 10:13:56
import socket
from supervisor.compat import PY3, as_string, as_bytes
bin_socket = socket.socket
if PY3:

    class text_socket(bin_socket):

        def __init__(self, family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0, fileno=None):
            bin_socket.__init__(self, family, type, proto, fileno)

        def recv(self, *args, **kwargs):
            return as_string(bin_socket.recv(self, *args, **kwargs))

        def recvfrom(self, *args, **kwargs):
            reply, whence = bin_socket.recvfrom(self, *args, **kwargs)
            reply = as_string(reply)
            return (reply, whence)

        def send(self, data, *args, **kwargs):
            b = as_bytes(data)
            return bin_socket.send(self, b, *args, **kwargs)

        def sendall(self, data, *args, **kwargs):
            return bin_socket.sendall(self, as_bytes(data), *args, **kwargs)

        def sendto(self, data, *args, **kwargs):
            return bin_socket.sendto(self, as_bytes(data), *args, **kwargs)

        def accept(self):
            fd, addr = self._accept()
            sock = text_socket(self.family, self.type, self.proto, fileno=fd)
            if socket.getdefaulttimeout() is None and self.gettimeout():
                sock.setblocking(True)
            return (
             sock, addr)


    text_socket.__init__.__doc__ = bin_socket.__init__.__doc__
else:
    text_socket = bin_socket