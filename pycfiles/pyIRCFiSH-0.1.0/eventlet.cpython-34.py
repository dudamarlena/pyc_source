# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib64/python3.4/site-packages/PyIRC/io/eventlet.py
# Compiled at: 2015-10-08 05:15:52
# Size of source mod 2**32: 3941 bytes
__doc__ = "An eventlet I/O backend for PyIRC.\n\nThis uses green threads to do scheduling of callbacks, and uses eventlet\nsockets.\n\n:py:meth:`~PyIRC.io.IRCEventlet.connect` is a green thread, and all\nof the scheduling is done with eventlet's `spawn_after`.\n\n"
from eventlet.green import socket, ssl
from eventlet import spawn_after, spawn_n
from logging import getLogger
from PyIRC.base import IRCBase
from PyIRC.line import Line
_logger = getLogger(__name__)

class IRCEventlet(IRCBase):
    """IRCEventlet"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        family = kwargs.get('family', socket.AF_INET)
        self._socket = self.socket = socket.socket(family=family)
        self.data = ''

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

        lines = data.split('\r\n')
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