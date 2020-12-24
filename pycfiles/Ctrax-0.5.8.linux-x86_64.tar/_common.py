# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/psutil/_common.py
# Compiled at: 2016-09-17 16:22:08
"""Common objects shared by __init__.py and _ps*.py modules."""
from __future__ import division
import contextlib, errno, functools, os, socket, stat, sys, warnings
from collections import namedtuple
from socket import AF_INET
from socket import SOCK_DGRAM
from socket import SOCK_STREAM
try:
    from socket import AF_INET6
except ImportError:
    AF_INET6 = None

try:
    from socket import AF_UNIX
except ImportError:
    AF_UNIX = None

if sys.version_info >= (3, 4):
    import enum
else:
    enum = None
__all__ = [
 'FREEBSD', 'BSD', 'LINUX', 'NETBSD', 'OPENBSD', 'OSX', 'POSIX', 'SUNOS',
 'WINDOWS',
 'CONN_CLOSE', 'CONN_CLOSE_WAIT', 'CONN_CLOSING', 'CONN_ESTABLISHED',
 'CONN_FIN_WAIT1', 'CONN_FIN_WAIT2', 'CONN_LAST_ACK', 'CONN_LISTEN',
 'CONN_NONE', 'CONN_SYN_RECV', 'CONN_SYN_SENT', 'CONN_TIME_WAIT',
 'NIC_DUPLEX_FULL', 'NIC_DUPLEX_HALF', 'NIC_DUPLEX_UNKNOWN',
 'STATUS_DEAD', 'STATUS_DISK_SLEEP', 'STATUS_IDLE', 'STATUS_LOCKED',
 'STATUS_RUNNING', 'STATUS_SLEEPING', 'STATUS_STOPPED', 'STATUS_SUSPENDED',
 'STATUS_TRACING_STOP', 'STATUS_WAITING', 'STATUS_WAKE_KILL',
 'STATUS_WAKING', 'STATUS_ZOMBIE',
 'pconn', 'pcputimes', 'pctxsw', 'pgids', 'pio', 'pionice', 'popenfile',
 'pthread', 'puids', 'sconn', 'scpustats', 'sdiskio', 'sdiskpart',
 'sdiskusage', 'snetio', 'snic', 'snicstats', 'sswap', 'suser',
 'conn_tmap', 'deprecated_method', 'isfile_strict', 'memoize',
 'parse_environ_block', 'path_exists_strict', 'usage_percent',
 'supports_ipv6', 'sockfam_to_enum', 'socktype_to_enum']
POSIX = os.name == 'posix'
WINDOWS = os.name == 'nt'
LINUX = sys.platform.startswith('linux')
OSX = sys.platform.startswith('darwin')
FREEBSD = sys.platform.startswith('freebsd')
OPENBSD = sys.platform.startswith('openbsd')
NETBSD = sys.platform.startswith('netbsd')
BSD = FREEBSD or OPENBSD or NETBSD
SUNOS = sys.platform.startswith('sunos') or sys.platform.startswith('solaris')
STATUS_RUNNING = 'running'
STATUS_SLEEPING = 'sleeping'
STATUS_DISK_SLEEP = 'disk-sleep'
STATUS_STOPPED = 'stopped'
STATUS_TRACING_STOP = 'tracing-stop'
STATUS_ZOMBIE = 'zombie'
STATUS_DEAD = 'dead'
STATUS_WAKE_KILL = 'wake-kill'
STATUS_WAKING = 'waking'
STATUS_IDLE = 'idle'
STATUS_LOCKED = 'locked'
STATUS_WAITING = 'waiting'
STATUS_SUSPENDED = 'suspended'
CONN_ESTABLISHED = 'ESTABLISHED'
CONN_SYN_SENT = 'SYN_SENT'
CONN_SYN_RECV = 'SYN_RECV'
CONN_FIN_WAIT1 = 'FIN_WAIT1'
CONN_FIN_WAIT2 = 'FIN_WAIT2'
CONN_TIME_WAIT = 'TIME_WAIT'
CONN_CLOSE = 'CLOSE'
CONN_CLOSE_WAIT = 'CLOSE_WAIT'
CONN_LAST_ACK = 'LAST_ACK'
CONN_LISTEN = 'LISTEN'
CONN_CLOSING = 'CLOSING'
CONN_NONE = 'NONE'
if enum is None:
    NIC_DUPLEX_FULL = 2
    NIC_DUPLEX_HALF = 1
    NIC_DUPLEX_UNKNOWN = 0
else:

    class NicDuplex(enum.IntEnum):
        NIC_DUPLEX_FULL = 2
        NIC_DUPLEX_HALF = 1
        NIC_DUPLEX_UNKNOWN = 0


    globals().update(NicDuplex.__members__)
sswap = namedtuple('sswap', ['total', 'used', 'free', 'percent', 'sin',
 'sout'])
sdiskusage = namedtuple('sdiskusage', ['total', 'used', 'free', 'percent'])
sdiskio = namedtuple('sdiskio', ['read_count', 'write_count',
 'read_bytes', 'write_bytes',
 'read_time', 'write_time'])
sdiskpart = namedtuple('sdiskpart', ['device', 'mountpoint', 'fstype', 'opts'])
snetio = namedtuple('snetio', ['bytes_sent', 'bytes_recv',
 'packets_sent', 'packets_recv',
 'errin', 'errout',
 'dropin', 'dropout'])
suser = namedtuple('suser', ['name', 'terminal', 'host', 'started'])
sconn = namedtuple('sconn', ['fd', 'family', 'type', 'laddr', 'raddr',
 'status', 'pid'])
snic = namedtuple('snic', ['family', 'address', 'netmask', 'broadcast', 'ptp'])
snicstats = namedtuple('snicstats', ['isup', 'duplex', 'speed', 'mtu'])
scpustats = namedtuple('scpustats', ['ctx_switches', 'interrupts', 'soft_interrupts', 'syscalls'])
pcputimes = namedtuple('pcputimes', [
 'user', 'system', 'children_user', 'children_system'])
popenfile = namedtuple('popenfile', ['path', 'fd'])
pthread = namedtuple('pthread', ['id', 'user_time', 'system_time'])
puids = namedtuple('puids', ['real', 'effective', 'saved'])
pgids = namedtuple('pgids', ['real', 'effective', 'saved'])
pio = namedtuple('pio', ['read_count', 'write_count',
 'read_bytes', 'write_bytes'])
pionice = namedtuple('pionice', ['ioclass', 'value'])
pctxsw = namedtuple('pctxsw', ['voluntary', 'involuntary'])
pconn = namedtuple('pconn', ['fd', 'family', 'type', 'laddr', 'raddr',
 'status'])
conn_tmap = {'all': (
         [
          AF_INET, AF_INET6, AF_UNIX], [SOCK_STREAM, SOCK_DGRAM]), 
   'tcp': (
         [
          AF_INET, AF_INET6], [SOCK_STREAM]), 
   'tcp4': (
          [
           AF_INET], [SOCK_STREAM]), 
   'udp': (
         [
          AF_INET, AF_INET6], [SOCK_DGRAM]), 
   'udp4': (
          [
           AF_INET], [SOCK_DGRAM]), 
   'inet': (
          [
           AF_INET, AF_INET6], [SOCK_STREAM, SOCK_DGRAM]), 
   'inet4': (
           [
            AF_INET], [SOCK_STREAM, SOCK_DGRAM]), 
   'inet6': (
           [
            AF_INET6], [SOCK_STREAM, SOCK_DGRAM])}
if AF_INET6 is not None:
    conn_tmap.update({'tcp6': (
              [
               AF_INET6], [SOCK_STREAM]), 
       'udp6': (
              [
               AF_INET6], [SOCK_DGRAM])})
if AF_UNIX is not None:
    conn_tmap.update({'unix': (
              [
               AF_UNIX], [SOCK_STREAM, SOCK_DGRAM])})
del AF_INET
del AF_INET6
del AF_UNIX
del SOCK_STREAM
del SOCK_DGRAM

def usage_percent(used, total, _round=None):
    """Calculate percentage usage of 'used' against 'total'."""
    try:
        ret = used / total * 100
    except ZeroDivisionError:
        ret = 0.0 if isinstance(used, float) or isinstance(total, float) else 0

    if _round is not None:
        return round(ret, _round)
    else:
        return ret
        return


def memoize(fun):
    """A simple memoize decorator for functions supporting (hashable)
    positional arguments.
    It also provides a cache_clear() function for clearing the cache:

    >>> @memoize
    ... def foo()
    ...     return 1
        ...
    >>> foo()
    1
    >>> foo.cache_clear()
    >>>
    """

    @functools.wraps(fun)
    def wrapper(*args, **kwargs):
        key = (args, frozenset(sorted(kwargs.items())))
        try:
            return cache[key]
        except KeyError:
            ret = cache[key] = fun(*args, **kwargs)
            return ret

    def cache_clear():
        """Clear cache."""
        cache.clear()

    cache = {}
    wrapper.cache_clear = cache_clear
    return wrapper


def isfile_strict(path):
    """Same as os.path.isfile() but does not swallow EACCES / EPERM
    exceptions, see:
    http://mail.python.org/pipermail/python-dev/2012-June/120787.html
    """
    try:
        st = os.stat(path)
    except OSError as err:
        if err.errno in (errno.EPERM, errno.EACCES):
            raise
        return False

    return stat.S_ISREG(st.st_mode)


def path_exists_strict(path):
    """Same as os.path.exists() but does not swallow EACCES / EPERM
    exceptions, see:
    http://mail.python.org/pipermail/python-dev/2012-June/120787.html
    """
    try:
        os.stat(path)
    except OSError as err:
        if err.errno in (errno.EPERM, errno.EACCES):
            raise
        return False

    return True


def supports_ipv6():
    """Return True if IPv6 is supported on this platform."""
    if not socket.has_ipv6 or not hasattr(socket, 'AF_INET6'):
        return False
    try:
        sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        with contextlib.closing(sock):
            sock.bind(('::1', 0))
        return True
    except socket.error:
        return False


def parse_environ_block(data):
    """Parse a C environ block of environment variables into a dictionary."""
    ret = {}
    pos = 0
    WINDOWS_ = WINDOWS
    while True:
        next_pos = data.find('\x00', pos)
        if next_pos <= pos:
            break
        equal_pos = data.find('=', pos, next_pos)
        if equal_pos > pos:
            key = data[pos:equal_pos]
            value = data[equal_pos + 1:next_pos]
            if WINDOWS_:
                key = key.upper()
            ret[key] = value
        pos = next_pos + 1

    return ret


def sockfam_to_enum(num):
    """Convert a numeric socket family value to an IntEnum member.
    If it's not a known member, return the numeric value itself.
    """
    if enum is None:
        return num
    else:
        try:
            return socket.AddressFamily(num)
        except (ValueError, AttributeError):
            return num

        return


def socktype_to_enum(num):
    """Convert a numeric socket type value to an IntEnum member.
    If it's not a known member, return the numeric value itself.
    """
    if enum is None:
        return num
    else:
        try:
            return socket.AddressType(num)
        except (ValueError, AttributeError):
            return num

        return


def deprecated_method(replacement):
    """A decorator which can be used to mark a method as deprecated
    'replcement' is the method name which will be called instead.
    """

    def outer(fun):
        msg = '%s() is deprecated; use %s() instead' % (
         fun.__name__, replacement)
        if fun.__doc__ is None:
            fun.__doc__ = msg

        @functools.wraps(fun)
        def inner(self, *args, **kwargs):
            warnings.warn(msg, category=DeprecationWarning, stacklevel=2)
            return getattr(self, replacement)(*args, **kwargs)

        return inner

    return outer