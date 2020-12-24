# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kiddiepool/connection.py
# Compiled at: 2018-03-12 18:12:15
import time, socket
from kiddiepool.exceptions import KiddieConnectionRecvFailure, KiddieConnectionSendFailure
DEFAULT_MAX_IDLE = 60
DEFAULT_LIFETIME = 300
DEFAULT_TIMEOUT = 3

class _ConnectionContext(object):
    """Context Manager to handle Connections"""

    def __init__(self, pool):
        self.conn = None
        self.pool = pool
        return

    def __enter__(self):
        self.conn = self.pool.get()
        return self.conn

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.pool.put(self.conn)
        if exc_type is not None:
            return bool(self.conn.handle_exception(exc_type, exc_value, exc_tb))
        else:
            return


class KiddieConnection(object):
    """
    TCP Base Connection Class

    Features:
     * TCP Keepalives on by default
     * Configurable timeout for socket operations
     * Tracks age and idle time for pools to refresh/cull idle/old connections
    """
    SendException = KiddieConnectionSendFailure
    RecvException = KiddieConnectionRecvFailure

    def __init__(self, lifetime=DEFAULT_LIFETIME, max_idle=DEFAULT_MAX_IDLE, tcp_keepalives=True, timeout=DEFAULT_TIMEOUT):
        self.host = None
        self.port = None
        self.socket = None
        self.max_idle = max_idle
        self.tcp_keepalives = tcp_keepalives
        self.timeout = timeout
        self.last_touch = 0
        self.lifetime = lifetime
        self.endoflife = 0
        return

    @property
    def closed(self):
        return self.socket is None

    def connect(self, host, port):
        self.host = host
        self.port = port
        if self.socket is not None:
            self.close()
        try:
            self._open()
        except socket.error:
            return False

        return True
        return

    def _open(self):
        self.socket = socket.create_connection((
         self.host, self.port), timeout=self.timeout)
        if self.tcp_keepalives:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.touch()
        if self.lifetime is not None:
            self.endoflife = time.time() + self.lifetime
        return

    def touch(self):
        self.last_touch = time.time()

    def close(self):
        self.socket.close()
        self.socket = None
        return

    def sendall(self, payload):
        try:
            self.socket.sendall(payload)
        except socket.error as e:
            raise self.SendException(e)

        self.touch()

    def recv(self, size, flags=0):
        try:
            data = self.socket.recv(size, flags)
        except socket.error as e:
            raise self.RecvException(e)

        self.touch()
        return data

    def recvall(self, size):
        """Receive `size` data and return it or raise a socket.error"""
        data = []
        received = 0
        try:
            while received < size:
                chunk = self.recv(size - received)
                if not chunk:
                    raise self.RecvException('Received %d bytes out of %d.' % (received, size))
                data.append(chunk)
                received += len(chunk)

        except socket.error as e:
            raise self.RecvException(e)

        return ('').join(data)

    def handle_exception(self, exc_type, exc_value, exc_tb):
        """Close connection on socket errors"""
        if issubclass(exc_type, socket.error):
            self.close()

    def validate(self):
        """
        Returns True if connection is still valid, otherwise False

        Takes into account socket status, idle time, and lifetime
        """
        if self.closed:
            return False
        else:
            now = time.time()
            if now - self.last_touch > self.max_idle:
                return False
            if self.lifetime is not None and self.endoflife < now:
                return False
            return True