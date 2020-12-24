# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Toolserver/timeoutsocket.py
# Compiled at: 2010-03-01 05:51:22
"""Timeout Socket

This module enables a timeout mechanism on all TCP connections.  It
does this by inserting a shim into the socket module.  After this module
has been imported, all socket creation goes through this shim.  As a
result, every TCP connection will support a timeout.

The beauty of this method is that it immediately and transparently
enables the entire python library to support timeouts on TCP sockets.
As an example, if you wanted to SMTP connections to have a 20 second
timeout:

    import timeoutsocket
    import smtplib
    timeoutsocket.setDefaultSocketTimeout(20)

The timeout applies to the socket functions that normally block on
execution:  read, write, connect, and accept.  If any of these 
operations exceeds the specified timeout, the exception Timeout
will be raised.

The default timeout value is set to None.  As a result, importing
this module does not change the default behavior of a socket.  The
timeout mechanism only activates when the timeout has been set to
a numeric value.  (This behavior mimics the behavior of the
select.select() function.)

This module implements two classes: TimeoutSocket and TimeoutFile.

The TimeoutSocket class defines a socket-like object that attempts to
avoid the condition where a socket may block indefinitely.  The
TimeoutSocket class raises a Timeout exception whenever the
current operation delays too long. 

The TimeoutFile class defines a file-like object that uses the TimeoutSocket
class.  When the makefile() method of TimeoutSocket is called, it returns
an instance of a TimeoutFile.

Each of these objects adds two methods to manage the timeout value:

    get_timeout()   -->  returns the timeout of the socket or file
    set_timeout()   -->  sets the timeout of the socket or file

As an example, one might use the timeout feature to create httplib
connections that will timeout after 30 seconds:

    import timeoutsocket
    import httplib
    H = httplib.HTTP("www.python.org")
    H.sock.set_timeout(30)

Note:  When used in this manner, the connect() routine may still
block because it happens before the timeout is set.  To avoid
this, use the 'timeoutsocket.setDefaultSocketTimeout()' function.

Good Luck!

"""
__version__ = '$Revision: 2 $'
__author__ = "Timothy O'Malley <timo@alum.mit.edu>"
import select, string, socket
if not hasattr(socket, '_no_timeoutsocket'):
    _socket = socket.socket
else:
    _socket = socket._no_timeoutsocket
import os
if os.name == 'nt':
    _IsConnected = (10022, 10056)
    _ConnectBusy = (10035, )
    _AcceptBusy = (10035, )
else:
    import errno
    _IsConnected = (
     errno.EISCONN,)
    _ConnectBusy = (errno.EINPROGRESS, errno.EALREADY, errno.EWOULDBLOCK)
    _AcceptBusy = (errno.EAGAIN, errno.EWOULDBLOCK)
    del errno
del os
_DefaultTimeout = None

def setDefaultSocketTimeout(timeout):
    global _DefaultTimeout
    _DefaultTimeout = timeout


def getDefaultSocketTimeout():
    return _DefaultTimeout


Error = socket.error

class Timeout(Exception):
    pass


from socket import AF_INET, SOCK_STREAM

def timeoutsocket(family=AF_INET, type=SOCK_STREAM, proto=None):
    if family != AF_INET or type != SOCK_STREAM:
        if proto:
            return _socket(family, type, proto)
        else:
            return _socket(family, type)
    return TimeoutSocket(_socket(family, type), _DefaultTimeout)


class TimeoutSocket:
    """TimeoutSocket object
    Implements a socket-like object that raises Timeout whenever
    an operation takes too long.
    The definition of 'too long' can be changed using the
    set_timeout() method.
    """
    _copies = 0
    _blocking = 1

    def __init__(self, sock, timeout):
        self._sock = sock
        self._timeout = timeout

    def __getattr__(self, key):
        return getattr(self._sock, key)

    def get_timeout(self):
        return self._timeout

    def set_timeout(self, timeout=None):
        self._timeout = timeout

    def setblocking(self, blocking):
        self._blocking = blocking
        return self._sock.setblocking(blocking)

    def connect_ex(self, addr):
        errcode = 0
        try:
            self.connect(addr)
        except Error, why:
            errcode = why[0]

        return errcode

    def connect(self, addr, port=None, dumbhack=None):
        if port != None:
            addr = (addr, port)
        sock = self._sock
        timeout = self._timeout
        blocking = self._blocking
        try:
            sock.setblocking(0)
            sock.connect(addr)
            sock.setblocking(blocking)
            return
        except Error, why:
            sock.setblocking(blocking)
            if not blocking:
                raise
            errcode = why[0]
            if dumbhack and errcode in _IsConnected:
                return
            if errcode not in _ConnectBusy:
                raise

        if not dumbhack:
            (r, w, e) = select.select([], [sock], [], timeout)
            if w:
                return self.connect(addr, dumbhack=1)
        raise Timeout('Attempted connect to %s timed out.' % str(addr))
        return

    def accept(self, dumbhack=None):
        sock = self._sock
        timeout = self._timeout
        blocking = self._blocking
        try:
            sock.setblocking(0)
            (newsock, addr) = sock.accept()
            sock.setblocking(blocking)
            timeoutnewsock = self.__class__(newsock, timeout)
            timeoutnewsock.setblocking(blocking)
            return (timeoutnewsock, addr)
        except Error, why:
            sock.setblocking(blocking)
            if not blocking:
                raise
            errcode = why[0]
            if errcode not in _AcceptBusy:
                raise

        if not dumbhack:
            (r, w, e) = select.select([sock], [], [], timeout)
            if r:
                return self.accept(dumbhack=1)
        raise Timeout('Attempted accept timed out.')

    def send(self, data, flags=0):
        sock = self._sock
        if self._blocking:
            (r, w, e) = select.select([], [sock], [], self._timeout)
            if not w:
                raise Timeout('Send timed out')
        return sock.send(data, flags)

    def recv(self, bufsize, flags=0):
        sock = self._sock
        if self._blocking:
            (r, w, e) = select.select([sock], [], [], self._timeout)
            if not r:
                raise Timeout('Recv timed out')
        return sock.recv(bufsize, flags)

    def makefile(self, flags='r', bufsize=-1):
        self._copies = self._copies + 1
        return TimeoutFile(self, flags, bufsize)

    def close(self):
        if self._copies <= 0:
            self._sock.close()
        else:
            self._copies = self._copies - 1


class TimeoutFile:
    """TimeoutFile object
    Implements a file-like object on top of TimeoutSocket.
    """

    def __init__(self, sock, mode='r', bufsize=4096):
        self._sock = sock
        self._bufsize = 4096
        if bufsize > 0:
            self._bufsize = bufsize
        if not hasattr(sock, '_inqueue'):
            self._sock._inqueue = ''

    def __getattr__(self, key):
        return getattr(self._sock, key)

    def close(self):
        self._sock.close()
        self._sock = None
        return

    def write(self, data):
        self.send(data)

    def read(self, size=-1):
        _sock = self._sock
        _bufsize = self._bufsize
        while 1:
            datalen = len(_sock._inqueue)
            if datalen >= size >= 0:
                break
            bufsize = _bufsize
            if size > 0:
                bufsize = min(bufsize, size - datalen)
            buf = self.recv(bufsize)
            if not buf:
                break
            _sock._inqueue = _sock._inqueue + buf

        data = _sock._inqueue
        _sock._inqueue = ''
        if size > 0 and datalen > size:
            _sock._inqueue = data[size:]
            data = data[:size]
        return data

    def readline(self, size=-1):
        _sock = self._sock
        _bufsize = self._bufsize
        while 1:
            idx = string.find(_sock._inqueue, '\n')
            if idx >= 0:
                break
            datalen = len(_sock._inqueue)
            if datalen >= size >= 0:
                break
            bufsize = _bufsize
            if size > 0:
                bufsize = min(bufsize, size - datalen)
            buf = self.recv(bufsize)
            if not buf:
                break
            _sock._inqueue = _sock._inqueue + buf

        data = _sock._inqueue
        _sock._inqueue = ''
        if idx >= 0:
            idx = idx + 1
            _sock._inqueue = data[idx:]
            data = data[:idx]
        elif size > 0 and datalen > size:
            _sock._inqueue = data[size:]
            data = data[:size]
        return data

    def readlines(self, sizehint=-1):
        result = []
        data = self.read()
        while data:
            idx = string.find(data, '\n')
            if idx >= 0:
                idx = idx + 1
                result.append(data[:idx])
                data = data[idx:]
            else:
                result.append(data)
                data = ''

        return result

    def flush(self):
        pass


if not hasattr(socket, '_no_timeoutsocket'):
    socket._no_timeoutsocket = socket.socket
    socket.socket = timeoutsocket
del socket
socket = timeoutsocket