# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: socket.pyc
# Compiled at: 2010-01-10 12:45:52
"""This module provides socket operations and some related functions.
On Unix, it supports IP (Internet Protocol) and Unix domain sockets.
On other systems, it only supports IP. Functions specific for a
socket are available as methods of the socket object.

Functions:

socket() -- create a new socket object
socketpair() -- create a pair of new socket objects [*]
fromfd() -- create a socket object from an open file descriptor [*]
gethostname() -- return the current hostname
gethostbyname() -- map a hostname to its IP number
gethostbyaddr() -- map an IP number or hostname to DNS info
getservbyname() -- map a service name and a protocol name to a port number
getprotobyname() -- map a protocol name (e.g. 'tcp') to a number
ntohs(), ntohl() -- convert 16, 32 bit int from network to host byte order
htons(), htonl() -- convert 16, 32 bit int from host to network byte order
inet_aton() -- convert IP addr string (123.45.67.89) to 32-bit packed format
inet_ntoa() -- convert 32-bit packed format IP to string (123.45.67.89)
ssl() -- secure socket layer support (only available if configured)
socket.getdefaulttimeout() -- get the default timeout value
socket.setdefaulttimeout() -- set the default timeout value
create_connection() -- connects to an address, with an optional timeout and
                       optional source address.

 [*] not available on all platforms!

Special objects:

SocketType -- type object for socket objects
error -- exception raised for I/O errors
has_ipv6 -- boolean value indicating if IPv6 is supported

Integer constants:

AF_INET, AF_UNIX -- socket domains (first argument to socket() call)
SOCK_STREAM, SOCK_DGRAM, SOCK_RAW -- socket types (second argument)

Many other constants may be defined; these may be used in calls to
the setsockopt() and getsockopt() methods.
"""
import _socket
from _socket import *
from functools import partial
from types import MethodType
try:
    import _ssl
except ImportError:
    pass
else:

    def ssl(sock, keyfile=None, certfile=None):
        import ssl as _realssl
        warnings.warn('socket.ssl() is deprecated.  Use ssl.wrap_socket() instead.', DeprecationWarning, stacklevel=2)
        return _realssl.sslwrap_simple(sock, keyfile, certfile)


    from _ssl import SSLError as sslerror
    from _ssl import RAND_add, RAND_egd, RAND_status, SSL_ERROR_ZERO_RETURN, SSL_ERROR_WANT_READ, SSL_ERROR_WANT_WRITE, SSL_ERROR_WANT_X509_LOOKUP, SSL_ERROR_SYSCALL, SSL_ERROR_SSL, SSL_ERROR_WANT_CONNECT, SSL_ERROR_EOF, SSL_ERROR_INVALID_ERROR_CODE

import os, sys, warnings
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

try:
    import errno
except ImportError:
    errno = None

EBADF = getattr(errno, 'EBADF', 9)
EINTR = getattr(errno, 'EINTR', 4)
__all__ = [
 'getfqdn', 'create_connection']
__all__.extend(os._get_exports_list(_socket))
_realsocket = socket
if sys.platform.lower().startswith('win'):
    errorTab = {}
    errorTab[10004] = 'The operation was interrupted.'
    errorTab[10009] = 'A bad file handle was passed.'
    errorTab[10013] = 'Permission denied.'
    errorTab[10014] = 'A fault occurred on the network??'
    errorTab[10022] = 'An invalid operation was attempted.'
    errorTab[10035] = 'The socket operation would block'
    errorTab[10036] = 'A blocking operation is already in progress.'
    errorTab[10048] = 'The network address is in use.'
    errorTab[10054] = 'The connection has been reset.'
    errorTab[10058] = 'The network has been shut down.'
    errorTab[10060] = 'The operation timed out.'
    errorTab[10061] = 'Connection refused.'
    errorTab[10063] = 'The name is too long.'
    errorTab[10064] = 'The host is down.'
    errorTab[10065] = 'The host is unreachable.'
    __all__.append('errorTab')

def getfqdn(name=''):
    """Get fully qualified domain name from name.

    An empty argument is interpreted as meaning the local host.

    First the hostname returned by gethostbyaddr() is checked, then
    possibly existing aliases. In case no FQDN is available, hostname
    from gethostname() is returned.
    """
    name = name.strip()
    if not name or name == '0.0.0.0':
        name = gethostname()
    try:
        hostname, aliases, ipaddrs = gethostbyaddr(name)
    except error:
        pass

    aliases.insert(0, hostname)
    for name in aliases:
        if '.' in name:
            break
    else:
        name = hostname

    return name


_socketmethods = (
 'bind', 'connect', 'connect_ex', 'fileno', 'listen',
 'getpeername', 'getsockname', 'getsockopt', 'setsockopt',
 'sendall', 'setblocking',
 'settimeout', 'gettimeout', 'shutdown')
if os.name == 'nt':
    _socketmethods = _socketmethods + ('ioctl',)
if sys.platform == 'riscos':
    _socketmethods = _socketmethods + ('sleeptaskw',)
_delegate_methods = (
 'recv', 'recvfrom', 'recv_into', 'recvfrom_into',
 'send', 'sendto')

class _closedsocket(object):
    __slots__ = []

    def _dummy(*args):
        raise error(EBADF, 'Bad file descriptor')

    send = recv = recv_into = sendto = recvfrom = recvfrom_into = _dummy
    __getattr__ = _dummy


class _socketobject(object):
    __doc__ = _realsocket.__doc__
    __slots__ = [
     '_sock', '__weakref__'] + list(_delegate_methods)

    def __init__(self, family=AF_INET, type=SOCK_STREAM, proto=0, _sock=None):
        if _sock is None:
            _sock = _realsocket(family, type, proto)
        self._sock = _sock
        for method in _delegate_methods:
            setattr(self, method, getattr(_sock, method))

        return

    def close(self):
        self._sock = _closedsocket()
        dummy = self._sock._dummy
        for method in _delegate_methods:
            setattr(self, method, dummy)

    close.__doc__ = _realsocket.close.__doc__

    def accept(self):
        sock, addr = self._sock.accept()
        return (_socketobject(_sock=sock), addr)

    accept.__doc__ = _realsocket.accept.__doc__

    def dup(self):
        """dup() -> socket object

        Return a new socket object connected to the same system resource."""
        return _socketobject(_sock=self._sock)

    def makefile(self, mode='r', bufsize=-1):
        """makefile([mode[, bufsize]]) -> file object

        Return a regular file object corresponding to the socket.  The mode
        and bufsize arguments are as for the built-in open() function."""
        return _fileobject(self._sock, mode, bufsize)

    family = property(lambda self: self._sock.family, doc='the socket family')
    type = property(lambda self: self._sock.type, doc='the socket type')
    proto = property(lambda self: self._sock.proto, doc='the socket protocol')


def meth(name, self, *args):
    return getattr(self._sock, name)(*args)


for _m in _socketmethods:
    p = partial(meth, _m)
    p.__name__ = _m
    p.__doc__ = getattr(_realsocket, _m).__doc__
    m = MethodType(p, None, _socketobject)
    setattr(_socketobject, _m, m)

socket = SocketType = _socketobject

class _fileobject(object):
    """Faux file object attached to a socket object."""
    default_bufsize = 8192
    name = '<socket>'
    __slots__ = [
     'mode', 'bufsize', 'softspace',
     '_sock', '_rbufsize', '_wbufsize', '_rbuf', '_wbuf', '_wbuf_len',
     '_close']

    def __init__(self, sock, mode='rb', bufsize=-1, close=False):
        self._sock = sock
        self.mode = mode
        if bufsize < 0:
            bufsize = self.default_bufsize
        self.bufsize = bufsize
        self.softspace = False
        if bufsize == 0:
            self._rbufsize = 1
        elif bufsize == 1:
            self._rbufsize = self.default_bufsize
        else:
            self._rbufsize = bufsize
        self._wbufsize = bufsize
        self._rbuf = StringIO()
        self._wbuf = []
        self._wbuf_len = 0
        self._close = close

    def _getclosed(self):
        return self._sock is None

    closed = property(_getclosed, doc='True if the file is closed')

    def close(self):
        try:
            if self._sock:
                self.flush()
        finally:
            if self._close:
                self._sock.close()
            self._sock = None

        return

    def __del__(self):
        try:
            self.close()
        except:
            pass

    def flush(self):
        if self._wbuf:
            data = ('').join(self._wbuf)
            self._wbuf = []
            self._wbuf_len = 0
            buffer_size = max(self._rbufsize, self.default_bufsize)
            data_size = len(data)
            write_offset = 0
            view = memoryview(data)
            try:
                while write_offset < data_size:
                    self._sock.sendall(view[write_offset:write_offset + buffer_size])
                    write_offset += buffer_size

            finally:
                if write_offset < data_size:
                    remainder = data[write_offset:]
                    del view
                    del data
                    self._wbuf.append(remainder)
                    self._wbuf_len = len(remainder)

    def fileno(self):
        return self._sock.fileno()

    def write(self, data):
        data = str(data)
        if not data:
            return
        self._wbuf.append(data)
        self._wbuf_len += len(data)
        if self._wbufsize == 0 or self._wbufsize == 1 and '\n' in data or self._wbuf_len >= self._wbufsize:
            self.flush()

    def writelines(self, list):
        lines = filter(None, map(str, list))
        self._wbuf_len += sum(map(len, lines))
        self._wbuf.extend(lines)
        if self._wbufsize <= 1 or self._wbuf_len >= self._wbufsize:
            self.flush()
        return

    def read--- This code section failed: ---

 L. 338         0  LOAD_GLOBAL           0  'max'
                3  LOAD_FAST             0  'self'
                6  LOAD_ATTR             1  '_rbufsize'
                9  LOAD_FAST             0  'self'
               12  LOAD_ATTR             2  'default_bufsize'
               15  CALL_FUNCTION_2       2  None
               18  STORE_FAST            2  'rbufsize'

 L. 342        21  LOAD_FAST             0  'self'
               24  LOAD_ATTR             3  '_rbuf'
               27  STORE_FAST            3  'buf'

 L. 343        30  LOAD_FAST             3  'buf'
               33  LOAD_ATTR             4  'seek'
               36  LOAD_CONST               0
               39  LOAD_CONST               2
               42  CALL_FUNCTION_2       2  None
               45  POP_TOP          

 L. 344        46  LOAD_FAST             1  'size'
               49  LOAD_CONST               0
               52  COMPARE_OP            0  <
               55  POP_JUMP_IF_FALSE   188  'to 188'

 L. 346        58  LOAD_GLOBAL           5  'StringIO'
               61  CALL_FUNCTION_0       0  None
               64  LOAD_FAST             0  'self'
               67  STORE_ATTR            3  '_rbuf'

 L. 347        70  SETUP_LOOP          105  'to 178'
               73  LOAD_GLOBAL           6  'True'
               76  POP_JUMP_IF_FALSE   177  'to 177'

 L. 348        79  SETUP_EXCEPT         22  'to 104'

 L. 349        82  LOAD_FAST             0  'self'
               85  LOAD_ATTR             7  '_sock'
               88  LOAD_ATTR             8  'recv'
               91  LOAD_FAST             2  'rbufsize'
               94  CALL_FUNCTION_1       1  None
               97  STORE_FAST            4  'data'
              100  POP_BLOCK        
              101  JUMP_FORWARD         47  'to 151'
            104_0  COME_FROM            79  '79'

 L. 350       104  DUP_TOP          
              105  LOAD_GLOBAL           9  'error'
              108  COMPARE_OP           10  exception-match
              111  POP_JUMP_IF_FALSE   150  'to 150'
              114  POP_TOP          
              115  STORE_FAST            5  'e'
              118  POP_TOP          

 L. 351       119  LOAD_FAST             5  'e'
              122  LOAD_ATTR            10  'args'
              125  LOAD_CONST               0
              128  BINARY_SUBSCR    
              129  LOAD_GLOBAL          11  'EINTR'
              132  COMPARE_OP            2  ==
              135  POP_JUMP_IF_FALSE   144  'to 144'

 L. 352       138  CONTINUE             73  'to 73'
              141  JUMP_FORWARD          0  'to 144'
            144_0  COME_FROM           141  '141'

 L. 353       144  RAISE_VARARGS_0       0  None
              147  JUMP_FORWARD          1  'to 151'
              150  END_FINALLY      
            151_0  COME_FROM           150  '150'
            151_1  COME_FROM           101  '101'

 L. 354       151  LOAD_FAST             4  'data'
              154  POP_JUMP_IF_TRUE    161  'to 161'

 L. 355       157  BREAK_LOOP       
              158  JUMP_FORWARD          0  'to 161'
            161_0  COME_FROM           158  '158'

 L. 356       161  LOAD_FAST             3  'buf'
              164  LOAD_ATTR            12  'write'
              167  LOAD_FAST             4  'data'
              170  CALL_FUNCTION_1       1  None
              173  POP_TOP          
              174  JUMP_BACK            73  'to 73'
              177  POP_BLOCK        
            178_0  COME_FROM            70  '70'

 L. 357       178  LOAD_FAST             3  'buf'
              181  LOAD_ATTR            13  'getvalue'
              184  CALL_FUNCTION_0       0  None
              187  RETURN_END_IF    
            188_0  COME_FROM            55  '55'

 L. 360       188  LOAD_FAST             3  'buf'
              191  LOAD_ATTR            14  'tell'
              194  CALL_FUNCTION_0       0  None
              197  STORE_FAST            6  'buf_len'

 L. 361       200  LOAD_FAST             6  'buf_len'
              203  LOAD_FAST             1  'size'
              206  COMPARE_OP            5  >=
              209  POP_JUMP_IF_FALSE   278  'to 278'

 L. 363       212  LOAD_FAST             3  'buf'
              215  LOAD_ATTR             4  'seek'
              218  LOAD_CONST               0
              221  CALL_FUNCTION_1       1  None
              224  POP_TOP          

 L. 364       225  LOAD_FAST             3  'buf'
              228  LOAD_ATTR            15  'read'
              231  LOAD_FAST             1  'size'
              234  CALL_FUNCTION_1       1  None
              237  STORE_FAST            7  'rv'

 L. 365       240  LOAD_GLOBAL           5  'StringIO'
              243  CALL_FUNCTION_0       0  None
              246  LOAD_FAST             0  'self'
              249  STORE_ATTR            3  '_rbuf'

 L. 366       252  LOAD_FAST             0  'self'
              255  LOAD_ATTR             3  '_rbuf'
              258  LOAD_ATTR            12  'write'
              261  LOAD_FAST             3  'buf'
              264  LOAD_ATTR            15  'read'
              267  CALL_FUNCTION_0       0  None
              270  CALL_FUNCTION_1       1  None
              273  POP_TOP          

 L. 367       274  LOAD_FAST             7  'rv'
              277  RETURN_END_IF    
            278_0  COME_FROM           209  '209'

 L. 369       278  LOAD_GLOBAL           5  'StringIO'
              281  CALL_FUNCTION_0       0  None
              284  LOAD_FAST             0  'self'
              287  STORE_ATTR            3  '_rbuf'

 L. 370       290  SETUP_LOOP          226  'to 519'
              293  LOAD_GLOBAL           6  'True'
              296  POP_JUMP_IF_FALSE   518  'to 518'

 L. 371       299  LOAD_FAST             1  'size'
              302  LOAD_FAST             6  'buf_len'
              305  BINARY_SUBTRACT  
              306  STORE_FAST            8  'left'

 L. 377       309  SETUP_EXCEPT         22  'to 334'

 L. 378       312  LOAD_FAST             0  'self'
              315  LOAD_ATTR             7  '_sock'
              318  LOAD_ATTR             8  'recv'
              321  LOAD_FAST             8  'left'
              324  CALL_FUNCTION_1       1  None
              327  STORE_FAST            4  'data'
              330  POP_BLOCK        
              331  JUMP_FORWARD         47  'to 381'
            334_0  COME_FROM           309  '309'

 L. 379       334  DUP_TOP          
              335  LOAD_GLOBAL           9  'error'
              338  COMPARE_OP           10  exception-match
              341  POP_JUMP_IF_FALSE   380  'to 380'
              344  POP_TOP          
              345  STORE_FAST            5  'e'
              348  POP_TOP          

 L. 380       349  LOAD_FAST             5  'e'
              352  LOAD_ATTR            10  'args'
              355  LOAD_CONST               0
              358  BINARY_SUBSCR    
              359  LOAD_GLOBAL          11  'EINTR'
              362  COMPARE_OP            2  ==
              365  POP_JUMP_IF_FALSE   374  'to 374'

 L. 381       368  CONTINUE            293  'to 293'
              371  JUMP_FORWARD          0  'to 374'
            374_0  COME_FROM           371  '371'

 L. 382       374  RAISE_VARARGS_0       0  None
              377  JUMP_FORWARD          1  'to 381'
              380  END_FINALLY      
            381_0  COME_FROM           380  '380'
            381_1  COME_FROM           331  '331'

 L. 383       381  LOAD_FAST             4  'data'
              384  POP_JUMP_IF_TRUE    391  'to 391'

 L. 384       387  BREAK_LOOP       
              388  JUMP_FORWARD          0  'to 391'
            391_0  COME_FROM           388  '388'

 L. 385       391  LOAD_GLOBAL          16  'len'
              394  LOAD_FAST             4  'data'
              397  CALL_FUNCTION_1       1  None
              400  STORE_FAST            9  'n'

 L. 386       403  LOAD_FAST             9  'n'
              406  LOAD_FAST             1  'size'
              409  COMPARE_OP            2  ==
              412  POP_JUMP_IF_FALSE   426  'to 426'
              415  LOAD_FAST             6  'buf_len'
              418  UNARY_NOT        
            419_0  COME_FROM           412  '412'
              419  POP_JUMP_IF_FALSE   426  'to 426'

 L. 392       422  LOAD_FAST             4  'data'
              425  RETURN_END_IF    
            426_0  COME_FROM           419  '419'

 L. 393       426  LOAD_FAST             9  'n'
              429  LOAD_FAST             8  'left'
              432  COMPARE_OP            2  ==
              435  POP_JUMP_IF_FALSE   458  'to 458'

 L. 394       438  LOAD_FAST             3  'buf'
              441  LOAD_ATTR            12  'write'
              444  LOAD_FAST             4  'data'
              447  CALL_FUNCTION_1       1  None
              450  POP_TOP          

 L. 395       451  DELETE_FAST           4  'data'

 L. 396       454  BREAK_LOOP       
              455  JUMP_FORWARD          0  'to 458'
            458_0  COME_FROM           455  '455'

 L. 397       458  LOAD_FAST             9  'n'
              461  LOAD_FAST             8  'left'
              464  COMPARE_OP            1  <=
              467  POP_JUMP_IF_TRUE    489  'to 489'
              470  LOAD_ASSERT              AssertionError
              473  LOAD_CONST               'recv(%d) returned %d bytes'
              476  LOAD_FAST             8  'left'
              479  LOAD_FAST             9  'n'
              482  BUILD_TUPLE_2         2 
              485  BINARY_MODULO    
              486  RAISE_VARARGS_2       2  None

 L. 398       489  LOAD_FAST             3  'buf'
              492  LOAD_ATTR            12  'write'
              495  LOAD_FAST             4  'data'
              498  CALL_FUNCTION_1       1  None
              501  POP_TOP          

 L. 399       502  LOAD_FAST             6  'buf_len'
              505  LOAD_FAST             9  'n'
              508  INPLACE_ADD      
              509  STORE_FAST            6  'buf_len'

 L. 400       512  DELETE_FAST           4  'data'
              515  JUMP_BACK           293  'to 293'
              518  POP_BLOCK        
            519_0  COME_FROM           290  '290'

 L. 402       519  LOAD_FAST             3  'buf'
              522  LOAD_ATTR            13  'getvalue'
              525  CALL_FUNCTION_0       0  None
              528  RETURN_VALUE     

Parse error at or near `POP_BLOCK' instruction at offset 518

    def readline(self, size=-1):
        buf = self._rbuf
        buf.seek(0, 2)
        if buf.tell() > 0:
            buf.seek(0)
            bline = buf.readline(size)
            if bline.endswith('\n') or len(bline) == size:
                self._rbuf = StringIO()
                self._rbuf.write(buf.read())
                return bline
            del bline
        if size < 0:
            if self._rbufsize <= 1:
                buf.seek(0)
                buffers = [buf.read()]
                self._rbuf = StringIO()
                data = None
                recv = self._sock.recv
                while True:
                    try:
                        while data != '\n':
                            data = recv(1)
                            if not data:
                                break
                            buffers.append(data)

                    except error as e:
                        if e.args[0] == EINTR:
                            continue
                        raise

                    break

                return ('').join(buffers)
            buf.seek(0, 2)
            self._rbuf = StringIO()
            while True:
                try:
                    data = self._sock.recv(self._rbufsize)
                except error as e:
                    if e.args[0] == EINTR:
                        continue
                    raise

                if not data:
                    break
                nl = data.find('\n')
                if nl >= 0:
                    nl += 1
                    buf.write(data[:nl])
                    self._rbuf.write(data[nl:])
                    del data
                    break
                buf.write(data)

            return buf.getvalue()
        else:
            buf.seek(0, 2)
            buf_len = buf.tell()
            if buf_len >= size:
                buf.seek(0)
                rv = buf.read(size)
                self._rbuf = StringIO()
                self._rbuf.write(buf.read())
                return rv
            self._rbuf = StringIO()
            while True:
                try:
                    data = self._sock.recv(self._rbufsize)
                except error as e:
                    if e.args[0] == EINTR:
                        continue
                    raise

                if not data:
                    break
                left = size - buf_len
                nl = data.find('\n', 0, left)
                if nl >= 0:
                    nl += 1
                    self._rbuf.write(data[nl:])
                    if buf_len:
                        buf.write(data[:nl])
                        break
                    else:
                        return data[:nl]
                n = len(data)
                if n == size and not buf_len:
                    return data
                if n >= left:
                    buf.write(data[:left])
                    self._rbuf.write(data[left:])
                    break
                buf.write(data)
                buf_len += n

            return buf.getvalue()
            return

    def readlines(self, sizehint=0):
        total = 0
        list = []
        while True:
            line = self.readline()
            if not line:
                break
            list.append(line)
            total += len(line)
            if sizehint and total >= sizehint:
                break

        return list

    def __iter__(self):
        return self

    def next(self):
        line = self.readline()
        if not line:
            raise StopIteration
        return line


_GLOBAL_DEFAULT_TIMEOUT = object()

def create_connection(address, timeout=_GLOBAL_DEFAULT_TIMEOUT, source_address=None):
    """Connect to *address* and return the socket object.

    Convenience function.  Connect to *address* (a 2-tuple ``(host,
    port)``) and return the socket object.  Passing the optional
    *timeout* parameter will set the timeout on the socket instance
    before attempting to connect.  If no *timeout* is supplied, the
    global default timeout setting returned by :func:`getdefaulttimeout`
    is used.  If *source_address* is set it must be a tuple of (host, port)
    for the socket to bind as a source address before making the connection.
    An host of '' or port 0 tells the OS to use the default.
    """
    msg = 'getaddrinfo returns an empty list'
    host, port = address
    for res in getaddrinfo(host, port, 0, SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
        sock = None
        try:
            sock = socket(af, socktype, proto)
            if timeout is not _GLOBAL_DEFAULT_TIMEOUT:
                sock.settimeout(timeout)
            if source_address:
                sock.bind(source_address)
            sock.connect(sa)
            return sock
        except error as msg:
            if sock is not None:
                sock.close()

    raise error, msg
    return