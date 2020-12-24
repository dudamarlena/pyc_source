# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil_http_parser/_socketio.py
# Compiled at: 2020-04-09 00:11:53
# Size of source mod 2**32: 4130 bytes
"""
socketio taken from the python3 stdlib
"""
import io, sys
from socket import timeout, error, socket
from errno import EINTR, EAGAIN, EWOULDBLOCK
_blocking_errnos = (
 EAGAIN, EWOULDBLOCK)

def _recv_into_sock_py26(sock, buf):
    data = sock.recv(len(buf))
    l = len(data)
    buf[:l] = data
    return l


if sys.version_info < (2, 7, 0, 'final'):
    _recv_into_sock = _recv_into_sock_py26
else:
    _recv_into_sock = lambda sock, buf: sock.recv_into(buf)

class SocketIO(io.RawIOBase):
    __doc__ = 'Raw I/O implementation for stream sockets.\n\n    This class supports the makefile() method on sockets.  It provides\n    the raw I/O interface on top of a socket object.\n    '

    def __init__(self, sock, mode):
        if mode not in ('r', 'w', 'rw', 'rb', 'wb', 'rwb'):
            raise ValueError('invalid mode: %r' % mode)
        io.RawIOBase.__init__(self)
        self._sock = sock
        if 'b' not in mode:
            mode += 'b'
        self._mode = mode
        self._reading = 'r' in mode
        self._writing = 'w' in mode
        self._timeout_occurred = False

    def readinto(self, b):
        """Read up to len(b) bytes into the writable buffer *b* and return
        the number of bytes read.  If the socket is non-blocking and no bytes
        are available, None is returned.

        If *b* is non-empty, a 0 return value indicates that the connection
        was shutdown at the other end.
        """
        self._checkClosed()
        self._checkReadable()
        if self._timeout_occurred:
            raise IOError('cannot read from timed out object')
        while True:
            try:
                return _recv_into_sock(self._sock, b)
            except timeout:
                self._timeout_occurred = True
                raise
            except error as e:
                n = e.args[0]
                if n == EINTR:
                    continue
                if n in _blocking_errnos:
                    return
                raise

    def write(self, b):
        """Write the given bytes or bytearray object *b* to the socket
        and return the number of bytes written.  This can be less than
        len(b) if not all data could be written.  If the socket is
        non-blocking and no bytes could be written None is returned.
        """
        self._checkClosed()
        self._checkWritable()
        try:
            return self._sock.send(b)
        except error as e:
            if e.args[0] in _blocking_errnos:
                return
            raise

    def readable(self):
        """True if the SocketIO is open for reading.
        """
        return self._reading and not self.closed

    def writable(self):
        """True if the SocketIO is open for writing.
        """
        return self._writing and not self.closed

    def fileno(self):
        """Return the file descriptor of the underlying socket.
        """
        self._checkClosed()
        return self._sock.fileno()

    @property
    def name(self):
        if not self.closed:
            return self.fileno()
        else:
            return -1

    @property
    def mode(self):
        return self._mode

    def close(self):
        """Close the SocketIO object.  This doesn't close the underlying
        socket, except if all references to it have disappeared.
        """
        if self.closed:
            return
        io.RawIOBase.close(self)
        self._sock = None

    def _checkClosed(self, msg=None):
        """Internal: raise an ValueError if file is closed
        """
        if self.closed:
            raise ValueError('I/O operation on closed file.' if msg is None else msg)