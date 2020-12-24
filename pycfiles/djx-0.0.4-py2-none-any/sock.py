# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/gunicorn/gunicorn/sock.py
# Compiled at: 2019-02-14 00:35:18
import errno, os, socket, stat, sys, time
from gunicorn import util
from gunicorn.six import string_types

class BaseSocket(object):

    def __init__(self, address, conf, log, fd=None):
        self.log = log
        self.conf = conf
        self.cfg_addr = address
        if fd is None:
            sock = socket.socket(self.FAMILY, socket.SOCK_STREAM)
            bound = False
        else:
            sock = socket.fromfd(fd, self.FAMILY, socket.SOCK_STREAM)
            os.close(fd)
            bound = True
        self.sock = self.set_options(sock, bound=bound)
        return

    def __str__(self):
        return '<socket %d>' % self.sock.fileno()

    def __getattr__(self, name):
        return getattr(self.sock, name)

    def set_options(self, sock, bound=False):
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if self.conf.reuse_port and hasattr(socket, 'SO_REUSEPORT'):
            try:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            except socket.error as err:
                if err.errno not in (errno.ENOPROTOOPT, errno.EINVAL):
                    raise

        if not bound:
            self.bind(sock)
        sock.setblocking(0)
        if hasattr(sock, 'set_inheritable'):
            sock.set_inheritable(True)
        sock.listen(self.conf.backlog)
        return sock

    def bind(self, sock):
        sock.bind(self.cfg_addr)

    def close(self):
        if self.sock is None:
            return
        else:
            try:
                self.sock.close()
            except socket.error as e:
                self.log.info('Error while closing socket %s', str(e))

            self.sock = None
            return


class TCPSocket(BaseSocket):
    FAMILY = socket.AF_INET

    def __str__(self):
        if self.conf.is_ssl:
            scheme = 'https'
        else:
            scheme = 'http'
        addr = self.sock.getsockname()
        return '%s://%s:%d' % (scheme, addr[0], addr[1])

    def set_options(self, sock, bound=False):
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        return super(TCPSocket, self).set_options(sock, bound=bound)


class TCP6Socket(TCPSocket):
    FAMILY = socket.AF_INET6

    def __str__(self):
        host, port, _, _ = self.sock.getsockname()
        return 'http://[%s]:%d' % (host, port)


class UnixSocket(BaseSocket):
    FAMILY = socket.AF_UNIX

    def __init__(self, addr, conf, log, fd=None):
        if fd is None:
            try:
                st = os.stat(addr)
            except OSError as e:
                if e.args[0] != errno.ENOENT:
                    raise
            else:
                if stat.S_ISSOCK(st.st_mode):
                    os.remove(addr)
                else:
                    raise ValueError('%r is not a socket' % addr)
        super(UnixSocket, self).__init__(addr, conf, log, fd=fd)
        return

    def __str__(self):
        return 'unix:%s' % self.cfg_addr

    def bind(self, sock):
        old_umask = os.umask(self.conf.umask)
        sock.bind(self.cfg_addr)
        util.chown(self.cfg_addr, self.conf.uid, self.conf.gid)
        os.umask(old_umask)


def _sock_type(addr):
    if isinstance(addr, tuple):
        if util.is_ipv6(addr[0]):
            sock_type = TCP6Socket
        else:
            sock_type = TCPSocket
    elif isinstance(addr, string_types):
        sock_type = UnixSocket
    else:
        raise TypeError('Unable to create socket from: %r' % addr)
    return sock_type


def create_sockets(conf, log, fds=None):
    """
    Create a new socket for the configured addresses or file descriptors.

    If a configured address is a tuple then a TCP socket is created.
    If it is a string, a Unix socket is created. Otherwise, a TypeError is
    raised.
    """
    listeners = []
    laddr = conf.address
    if conf.certfile and not os.path.exists(conf.certfile):
        raise ValueError('certfile "%s" does not exist' % conf.certfile)
    if conf.keyfile and not os.path.exists(conf.keyfile):
        raise ValueError('keyfile "%s" does not exist' % conf.keyfile)
    if fds is not None:
        for fd in fds:
            sock = socket.fromfd(fd, socket.AF_UNIX, socket.SOCK_STREAM)
            sock_name = sock.getsockname()
            sock_type = _sock_type(sock_name)
            listener = sock_type(sock_name, conf, log, fd=fd)
            listeners.append(listener)

        return listeners
    for addr in laddr:
        sock_type = _sock_type(addr)
        sock = None
        for i in range(5):
            try:
                sock = sock_type(addr, conf, log)
            except socket.error as e:
                if e.args[0] == errno.EADDRINUSE:
                    log.error('Connection in use: %s', str(addr))
                if e.args[0] == errno.EADDRNOTAVAIL:
                    log.error('Invalid address: %s', str(addr))
                if i < 5:
                    msg = 'connection to {addr} failed: {error}'
                    log.debug(msg.format(addr=str(addr), error=str(e)))
                    log.error('Retrying in 1 second.')
                    time.sleep(1)
            else:
                break

        if sock is None:
            log.error("Can't connect to %s", str(addr))
            sys.exit(1)
        listeners.append(sock)

    return listeners


def close_sockets(listeners, unlink=True):
    for sock in listeners:
        sock_name = sock.getsockname()
        sock.close()
        if unlink and _sock_type(sock_name) is UnixSocket:
            os.unlink(sock_name)