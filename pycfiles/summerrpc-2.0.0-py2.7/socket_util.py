# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summerrpc/helper/socket_util.py
# Compiled at: 2018-07-31 10:42:31
__all__ = [
 'ServerSocketBuilder', 'ClientSocketBuilder',
 'BaseSocket', 'ServerSocket', 'ClientSocket']
__authors__ = ['Tim Chow']
import socket, threading

class SocketBuilder(object):

    def __init__(self):
        self._host = None
        self._port = None
        self._timeout = None
        self._tcp_nodelay = True
        self._blocking = True
        return

    def with_host(self, host):
        self._host = host
        return self

    def with_port(self, port):
        if not isinstance(port, int) or port < 0 or port > 65535:
            raise ValueError('invalid port')
        self._port = port
        return self

    def with_timeout(self, timeout):
        if not isinstance(timeout, (int, float)) or timeout < 0:
            raise ValueError('invalid timeout')
        self._timeout = timeout
        return self

    def with_tcp_nodelay(self):
        self._tcp_nodelay = True
        return self

    def with_tcp_cork(self):
        self._tcp_nodelay = False
        return self

    def with_blocking(self):
        self._blocking = True
        return self

    def with_non_blocking(self):
        self._blocking = False
        return self

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def timeout(self):
        return self._timeout

    @property
    def tcp_nodelay(self):
        return self._tcp_nodelay

    @property
    def blocking(self):
        return self._blocking


class ServerSocketBuilder(SocketBuilder):

    def __init__(self, *a, **kw):
        super(self.__class__, self).__init__(*a, **kw)
        self._backlog = 5

    def with_backlog(self, backlog):
        if not isinstance(backlog, int) or backlog <= 0:
            raise ValueError('invalid backlog')
        self._backlog = backlog
        return self

    @property
    def backlog(self):
        return self._backlog

    def build(self):
        if self._host is None or self._port is None:
            raise RuntimeError('host and port must be provided')
        return ServerSocket(self)


class ClientSocketBuilder(SocketBuilder):

    def __init__(self, *a, **kw):
        super(self.__class__, self).__init__(*a, **kw)

    def build(self):
        return ClientSocket(self)


class BaseSocket(object):

    def __init__(self, builder):
        self._close_lock = threading.RLock()
        self._closed = False
        try:
            self.socket = self.make_socket(builder)
            self.set_socket(self.socket, builder)
        except BaseException:
            self._initialized = False
            raise
        else:
            self._initialized = True

    def make_socket(self, builder):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if builder.tcp_nodelay:
            sock.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
        sock.setblocking(builder.blocking)
        if builder.blocking:
            sock.settimeout(builder.timeout)
        return sock

    def set_socket(self, sock, builder):
        raise NotImplementedError('set_socket should be implemented in subclasses')

    def __getattr__(self, attr_name):
        attr = getattr(self.socket, attr_name, None)
        if attr is None:
            raise AttributeError('Socket instance has no attribute: %s' % attr_name)
        return attr

    def close(self):
        if not self._initialized:
            return
        if self._closed:
            return
        with self._close_lock:
            if self._closed:
                return
            try:
                self.socket.close()
            except BaseException as ex:
                pass

            self._closed = True

    @property
    def closed(self):
        return self._closed

    def __del__(self):
        self.close()


class ServerSocket(BaseSocket):

    def __init__(self, builder):
        if not isinstance(builder, ServerSocketBuilder):
            raise TypeError('invalid builder')
        super(self.__class__, self).__init__(builder)

    def set_socket(self, sock, builder):
        sock.bind((builder.host, builder.port))
        sock.listen(builder.backlog)


class ClientSocket(BaseSocket):

    def __init__(self, builder):
        if not isinstance(builder, ClientSocketBuilder):
            raise TypeError('invalid builder')
        super(self.__class__, self).__init__(builder)

    def set_socket(self, sock, builder):
        if builder.host is not None and builder.port is not None:
            sock.connect((builder.host, builder.port))
        return