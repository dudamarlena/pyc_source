# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.4/site-packages/PyIRC/io/socket.py
# Compiled at: 2015-10-08 05:15:52
# Size of source mod 2**32: 4324 bytes
""" A basic socket/ssl/sched-based module implementation for IRC.

If you just want a simple bot for one network, this is what you want.

Note all socket stuff is blocking, if you want non-blocking operation, you
may want to subclass this and modify things for your application.

This also serves as a useful example.
"""
import socket, ssl
from sched import scheduler
from logging import getLogger
from PyIRC.base import IRCBase
from PyIRC.line import Line
_logger = getLogger(__name__)

class IRCSocket(IRCBase):
    __doc__ = 'The socket implementation of the IRC protocol. No asynchronous I/O is\n    done. All scheduling is done with socket timeouts and the python ``sched``\n    module.\n\n    The same methods available in\n    :py:class:`~PyIRC.base.IRCBase` are available.\n\n\n    :key socket_timeout:\n        Set the timeout for connecting to the server (defaults to 10)\n\n    :key send_timeout:\n        Set the timeout for sending data (default None)\n\n    :key recv_timeout:\n        Set the timeout for receiving data (default None)\n\n    :key family:\n        The family to use for the socket (default AF_INET, IPv4). Set to\n        socket.AF_INET6 for IPv6 usage.\n\n    '

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        family = kwargs.get('family', socket.AF_INET)
        self._socket = self.socket = socket.socket(family=family)
        self.scheduler = scheduler()
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
        if not self.scheduler.empty():
            timeout_s = self.scheduler.run(False)
            if timeout is None or timeout > timeout_s:
                timeout = timeout_s
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
            super().recv(line)

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
        return self.scheduler.enter(time, 0, callback)

    def unschedule(self, sched):
        self.scheduler.cancel(sched)

    def wrap_ssl(self):
        if self.ssl:
            return False
        self._socket = self.socket
        self.socket = ssl.wrap_socket(self.socket)
        self.socket.do_handshake()
        self.ssl = True
        return True