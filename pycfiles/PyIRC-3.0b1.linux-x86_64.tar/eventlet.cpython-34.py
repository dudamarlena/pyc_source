# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.4/site-packages/PyIRC/io/eventlet.py
# Compiled at: 2015-10-08 05:15:52
# Size of source mod 2**32: 3941 bytes
"""An eventlet I/O backend for PyIRC.

This uses green threads to do scheduling of callbacks, and uses eventlet
sockets.

:py:meth:`~PyIRC.io.IRCEventlet.connect` is a green thread, and all
of the scheduling is done with eventlet's `spawn_after`.

"""
from eventlet.green import socket, ssl
from eventlet import spawn_after, spawn_n
from logging import getLogger
from PyIRC.base import IRCBase
from PyIRC.line import Line
_logger = getLogger(__name__)

class IRCEventlet(IRCBase):
    __doc__ = 'The eventlet implementation of the IRC protocol. Everything is done\n    with green threads, as far as possible.\n\n    Virtually everything can be done as a green thread.\n\n    The same methods available in\n    :py:class:`~PyIRC.base.IRCBase` are available.\n\n    :key socket_timeout:\n        Set the timeout for connecting to the server (defaults to 10)\n\n    :key send_timeout:\n        Set the timeout for sending data (default None)\n\n    :key recv_timeout:\n        Set the timeout for receiving data (default None)\n\n    :key family:\n        The family to use for the socket (default AF_INET, IPv4). Set to\n        socket.AF_INET6 for IPv6 usage.\n\n    '

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        family = kwargs.get('family', socket.AF_INET)
        self._socket = self.socket = socket.socket(family=family)
        self.data = b''

    def connect(self):
        if self.ssl is True:
            self.socket = ssl.wrap_socket(self.socket)
        else:
            if isinstance(self.ssl, ssl.SSLContext):
                self.socket = self.ssl.wrap_socket(self.socket)
            elif self.ssl is not (None, False):
                raise TypeError('ssl must be an SSLContext, bool, or None')
        self.socket.settimeout(self.kwargs.get('socket_timeout', 10))
        self.socket.connect((self.server, self.port))
        super().connect()

    def recv(self):
        timeout = self.kwargs.get('recv_timeout', None)
        self.socket.settimeout(timeout)
        try:
            data = self.socket.recv(512)
            if not data:
                raise OSError('Connection reset by peer')
            data = self.data + data
        except socket.timeout:
            return

        lines = data.split(b'\r\n')
        self.data = lines.pop()
        for line in lines:
            line = Line.parse(line.decode('utf-8', 'ignore'))
            _logger.debug('IN: %s', str(line).rstrip())
            spawn_n(super().recv(line))

    def loop(self):
        """Simple loop for bots.

        Does not return, but raises exception when the connection is
        closed.

        """
        self.connect()
        while True:
            try:
                self.recv()
            except OSError:
                self.close()
                raise

    def send(self, command, params):
        line = super().send(command, params)
        if line is None:
            return
        self.socket.settimeout(self.kwargs.get('send_timeout', None))
        if self.socket.send(bytes(line)) == 0:
            raise OSError('Connection reset by peer')
        _logger.debug('OUT: %s', str(line).rstrip())

    def schedule(self, time, callback):
        return spawn_after(time, callback)

    def unschedule(self, sched):
        sched.cancel()

    def wrap_ssl(self):
        if self.ssl:
            return False
        self._socket = self.socket
        self.socket = ssl.wrap_socket(self.socket)
        self.socket.do_handshake()
        self.ssl = True
        return True