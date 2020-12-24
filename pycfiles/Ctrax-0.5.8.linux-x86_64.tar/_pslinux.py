# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/psutil/_pslinux.py
# Compiled at: 2016-09-17 16:22:08
"""Linux platform implementation."""
from __future__ import division
import base64, errno, functools, os, re, socket, struct, sys, traceback, warnings
from collections import defaultdict
from collections import namedtuple
from . import _common
from . import _psposix
from . import _psutil_linux as cext
from . import _psutil_posix as cext_posix
from ._common import isfile_strict
from ._common import memoize
from ._common import parse_environ_block
from ._common import NIC_DUPLEX_FULL
from ._common import NIC_DUPLEX_HALF
from ._common import NIC_DUPLEX_UNKNOWN
from ._common import path_exists_strict
from ._common import supports_ipv6
from ._common import usage_percent
from ._compat import b
from ._compat import basestring
from ._compat import long
from ._compat import PY3
if sys.version_info >= (3, 4):
    import enum
else:
    enum = None
__extra__all__ = [
 'PROCFS_PATH',
 'IOPRIO_CLASS_NONE', 'IOPRIO_CLASS_RT', 'IOPRIO_CLASS_BE',
 'IOPRIO_CLASS_IDLE',
 'CONN_ESTABLISHED', 'CONN_SYN_SENT', 'CONN_SYN_RECV', 'CONN_FIN_WAIT1',
 'CONN_FIN_WAIT2', 'CONN_TIME_WAIT', 'CONN_CLOSE', 'CONN_CLOSE_WAIT',
 'CONN_LAST_ACK', 'CONN_LISTEN', 'CONN_CLOSING']
HAS_SMAPS = os.path.exists('/proc/%s/smaps' % os.getpid())
HAS_PRLIMIT = hasattr(cext, 'linux_prlimit')
if HAS_PRLIMIT:
    for name in dir(cext):
        if name.startswith('RLIM'):
            __extra__all__.append(name)

CLOCK_TICKS = os.sysconf('SC_CLK_TCK')
PAGESIZE = os.sysconf('SC_PAGE_SIZE')
BOOT_TIME = None
BIGGER_FILE_BUFFERING = -1 if PY3 else 8192
LITTLE_ENDIAN = sys.byteorder == 'little'
if PY3:
    FS_ENCODING = sys.getfilesystemencoding()
    ENCODING_ERRORS_HANDLER = 'surrogateescape'
if enum is None:
    AF_LINK = socket.AF_PACKET
else:
    AddressFamily = enum.IntEnum('AddressFamily', {'AF_LINK': int(socket.AF_PACKET)})
    AF_LINK = AddressFamily.AF_LINK
if enum is None:
    IOPRIO_CLASS_NONE = 0
    IOPRIO_CLASS_RT = 1
    IOPRIO_CLASS_BE = 2
    IOPRIO_CLASS_IDLE = 3
else:

    class IOPriority(enum.IntEnum):
        IOPRIO_CLASS_NONE = 0
        IOPRIO_CLASS_RT = 1
        IOPRIO_CLASS_BE = 2
        IOPRIO_CLASS_IDLE = 3


    globals().update(IOPriority.__members__)
PROC_STATUSES = {'R': _common.STATUS_RUNNING, 
   'S': _common.STATUS_SLEEPING, 
   'D': _common.STATUS_DISK_SLEEP, 
   'T': _common.STATUS_STOPPED, 
   't': _common.STATUS_TRACING_STOP, 
   'Z': _common.STATUS_ZOMBIE, 
   'X': _common.STATUS_DEAD, 
   'x': _common.STATUS_DEAD, 
   'K': _common.STATUS_WAKE_KILL, 
   'W': _common.STATUS_WAKING}
TCP_STATUSES = {'01': _common.CONN_ESTABLISHED, 
   '02': _common.CONN_SYN_SENT, 
   '03': _common.CONN_SYN_RECV, 
   '04': _common.CONN_FIN_WAIT1, 
   '05': _common.CONN_FIN_WAIT2, 
   '06': _common.CONN_TIME_WAIT, 
   '07': _common.CONN_CLOSE, 
   '08': _common.CONN_CLOSE_WAIT, 
   '09': _common.CONN_LAST_ACK, 
   '0A': _common.CONN_LISTEN, 
   '0B': _common.CONN_CLOSING}
NoSuchProcess = None
ZombieProcess = None
AccessDenied = None
TimeoutExpired = None
svmem = namedtuple('svmem', ['total', 'available', 'percent', 'used', 'free',
 'active', 'inactive', 'buffers', 'cached', 'shared'])
sdiskio = namedtuple('sdiskio', ['read_count', 'write_count',
 'read_bytes', 'write_bytes',
 'read_time', 'write_time',
 'read_merged_count', 'write_merged_count',
 'busy_time'])
popenfile = namedtuple('popenfile', ['path', 'fd', 'position', 'mode', 'flags'])
pmem = namedtuple('pmem', 'rss vms shared text lib data dirty')
pfullmem = namedtuple('pfullmem', pmem._fields + ('uss', 'pss', 'swap'))
pmmap_grouped = namedtuple('pmmap_grouped', [
 'path', 'rss', 'size', 'pss', 'shared_clean', 'shared_dirty',
 'private_clean', 'private_dirty', 'referenced', 'anonymous', 'swap'])
pmmap_ext = namedtuple('pmmap_ext', 'addr perms ' + (' ').join(pmmap_grouped._fields))

def open_binary(fname, **kwargs):
    return open(fname, 'rb', **kwargs)


def open_text(fname, **kwargs):
    """On Python 3 opens a file in text mode by using fs encoding and
    a proper en/decoding errors handler.
    On Python 2 this is just an alias for open(name, 'rt').
    """
    if PY3:
        kwargs.setdefault('encoding', FS_ENCODING)
        kwargs.setdefault('errors', ENCODING_ERRORS_HANDLER)
    return open(fname, 'rt', **kwargs)


if PY3:

    def decode(s):
        return s.decode(encoding=FS_ENCODING, errors=ENCODING_ERRORS_HANDLER)


else:

    def decode(s):
        return s


def get_procfs_path():
    return sys.modules['psutil'].PROCFS_PATH


def readlink(path):
    """Wrapper around os.readlink()."""
    assert isinstance(path, basestring), path
    path = os.readlink(path)
    path = path.split('\x00')[0]
    if path.endswith(' (deleted)') and not path_exists_strict(path):
        path = path[:-10]
    return path


def file_flags_to_mode(flags):
    modes_map = {os.O_RDONLY: 'r', os.O_WRONLY: 'w', os.O_RDWR: 'w+'}
    mode = modes_map[(flags & (os.O_RDONLY | os.O_WRONLY | os.O_RDWR))]
    if flags & os.O_APPEND:
        mode = mode.replace('w', 'a', 1)
    mode = mode.replace('w+', 'r+')
    return mode


def get_sector_size():
    try:
        with open('/sys/block/sda/queue/hw_sector_size') as (f):
            return int(f.read())
    except (IOError, ValueError):
        return 512


SECTOR_SIZE = get_sector_size()

@memoize
def set_scputimes_ntuple(procfs_path):
    """Return a namedtuple of variable fields depending on the
    CPU times available on this Linux kernel version which may be:
    (user, nice, system, idle, iowait, irq, softirq, [steal, [guest,
     [guest_nice]]])
    """
    global scputimes
    with open_binary('%s/stat' % procfs_path) as (f):
        values = f.readline().split()[1:]
    fields = [
     'user', 'nice', 'system', 'idle', 'iowait', 'irq', 'softirq']
    vlen = len(values)
    if vlen >= 8:
        fields.append('steal')
    if vlen >= 9:
        fields.append('guest')
    if vlen >= 10:
        fields.append('guest_nice')
    scputimes = namedtuple('scputimes', fields)
    return scputimes


try:
    scputimes = set_scputimes_ntuple('/proc')
except Exception:
    traceback.print_exc()
    scputimes = namedtuple('scputimes', 'user system idle')(0.0, 0.0, 0.0)

def virtual_memory():
    total, free, buffers, shared, _, _, unit_multiplier = cext.linux_sysinfo()
    total *= unit_multiplier
    free *= unit_multiplier
    buffers *= unit_multiplier
    shared *= unit_multiplier or None
    if shared == 0:
        shared = None
    cached = active = inactive = None
    with open_binary('%s/meminfo' % get_procfs_path()) as (f):
        for line in f:
            if cached is None and line.startswith('Cached:'):
                cached = int(line.split()[1]) * 1024
            elif active is None and line.startswith('Active:'):
                active = int(line.split()[1]) * 1024
            elif inactive is None and line.startswith('Inactive:'):
                inactive = int(line.split()[1]) * 1024
            elif shared is None and line.startswith('MemShared:') or line.startswith('Shmem:'):
                shared = int(line.split()[1]) * 1024

    missing = []
    if cached is None:
        missing.append('cached')
        cached = 0
    if active is None:
        missing.append('active')
        active = 0
    if inactive is None:
        missing.append('inactive')
        inactive = 0
    if shared is None:
        missing.append('shared')
        shared = 0
    if missing:
        msg = "%s memory stats couldn't be determined and %s set to 0" % (
         (', ').join(missing),
         'was' if len(missing) == 1 else 'were')
        warnings.warn(msg, RuntimeWarning)
    avail = free + buffers + cached
    used = total - free
    percent = usage_percent(total - avail, total, _round=1)
    return svmem(total, avail, percent, used, free, active, inactive, buffers, cached, shared)


def swap_memory():
    _, _, _, _, total, free, unit_multiplier = cext.linux_sysinfo()
    total *= unit_multiplier
    free *= unit_multiplier
    used = total - free
    percent = usage_percent(used, total, _round=1)
    try:
        f = open_binary('%s/vmstat' % get_procfs_path())
    except IOError as err:
        msg = "'sin' and 'sout' swap memory stats couldn't be determined and were set to 0 (%s)" % str(err)
        warnings.warn(msg, RuntimeWarning)
        sin = sout = 0
    else:
        with f:
            sin = sout = None
            for line in f:
                if line.startswith('pswpin'):
                    sin = int(line.split(' ')[1]) * 4 * 1024
                elif line.startswith('pswpout'):
                    sout = int(line.split(' ')[1]) * 4 * 1024
                if sin is not None and sout is not None:
                    break
            else:
                msg = "'sin' and 'sout' swap memory stats couldn't be determined and were set to 0"
                warnings.warn(msg, RuntimeWarning)
                sin = sout = 0

    return _common.sswap(total, used, free, percent, sin, sout)


def cpu_times():
    """Return a named tuple representing the following system-wide
    CPU times:
    (user, nice, system, idle, iowait, irq, softirq [steal, [guest,
     [guest_nice]]])
    Last 3 fields may not be available on all Linux kernel versions.
    """
    procfs_path = get_procfs_path()
    set_scputimes_ntuple(procfs_path)
    with open_binary('%s/stat' % procfs_path) as (f):
        values = f.readline().split()
    fields = values[1:len(scputimes._fields) + 1]
    fields = [ float(x) / CLOCK_TICKS for x in fields ]
    return scputimes(*fields)


def per_cpu_times():
    """Return a list of namedtuple representing the CPU times
    for every CPU available on the system.
    """
    procfs_path = get_procfs_path()
    set_scputimes_ntuple(procfs_path)
    cpus = []
    with open_binary('%s/stat' % procfs_path) as (f):
        f.readline()
        for line in f:
            if line.startswith('cpu'):
                values = line.split()
                fields = values[1:len(scputimes._fields) + 1]
                fields = [ float(x) / CLOCK_TICKS for x in fields ]
                entry = scputimes(*fields)
                cpus.append(entry)

        return cpus


def cpu_count_logical():
    """Return the number of logical CPUs in the system."""
    try:
        return os.sysconf('SC_NPROCESSORS_ONLN')
    except ValueError:
        num = 0
        with open_binary('%s/cpuinfo' % get_procfs_path()) as (f):
            for line in f:
                if line.lower().startswith('processor'):
                    num += 1

        if num == 0:
            search = re.compile('cpu\\d')
            with open_text('%s/stat' % get_procfs_path()) as (f):
                for line in f:
                    line = line.split(' ')[0]
                    if search.match(line):
                        num += 1

        if num == 0:
            return
        return num

    return


def cpu_count_physical():
    """Return the number of physical cores in the system."""
    mapping = {}
    current_info = {}
    with open_binary('%s/cpuinfo' % get_procfs_path()) as (f):
        for line in f:
            line = line.strip().lower()
            if not line:
                if 'physical id' in current_info and 'cpu cores' in current_info:
                    mapping[current_info['physical id']] = current_info['cpu cores']
                current_info = {}
            elif line.startswith('physical id') or line.startswith('cpu cores'):
                key, value = line.split('\t:', 1)
                current_info[key] = int(value)

    return sum(mapping.values()) or None


def cpu_stats():
    with open_binary('%s/stat' % get_procfs_path()) as (f):
        ctx_switches = None
        interrupts = None
        soft_interrupts = None
        for line in f:
            if line.startswith('ctxt'):
                ctx_switches = int(line.split()[1])
            elif line.startswith('intr'):
                interrupts = int(line.split()[1])
            elif line.startswith('softirq'):
                soft_interrupts = int(line.split()[1])
            if ctx_switches is not None and soft_interrupts is not None and interrupts is not None:
                break

    syscalls = 0
    return _common.scpustats(ctx_switches, interrupts, soft_interrupts, syscalls)


net_if_addrs = cext_posix.net_if_addrs

class _Ipv6UnsupportedError(Exception):
    pass


class Connections:
    """A wrapper on top of /proc/net/* files, retrieving per-process
    and system-wide open connections (TCP, UDP, UNIX) similarly to
    "netstat -an".

    Note: in case of UNIX sockets we're only able to determine the
    local endpoint/path, not the one it's connected to.
    According to [1] it would be possible but not easily.

    [1] http://serverfault.com/a/417946
    """

    def __init__(self):
        tcp4 = (
         'tcp', socket.AF_INET, socket.SOCK_STREAM)
        tcp6 = ('tcp6', socket.AF_INET6, socket.SOCK_STREAM)
        udp4 = ('udp', socket.AF_INET, socket.SOCK_DGRAM)
        udp6 = ('udp6', socket.AF_INET6, socket.SOCK_DGRAM)
        unix = ('unix', socket.AF_UNIX, None)
        self.tmap = {'all': (
                 tcp4, tcp6, udp4, udp6, unix), 
           'tcp': (
                 tcp4, tcp6), 
           'tcp4': (
                  tcp4,), 
           'tcp6': (
                  tcp6,), 
           'udp': (
                 udp4, udp6), 
           'udp4': (
                  udp4,), 
           'udp6': (
                  udp6,), 
           'unix': (
                  unix,), 
           'inet': (
                  tcp4, tcp6, udp4, udp6), 
           'inet4': (
                   tcp4, udp4), 
           'inet6': (
                   tcp6, udp6)}
        self._procfs_path = None
        return

    def get_proc_inodes(self, pid):
        inodes = defaultdict(list)
        for fd in os.listdir('%s/%s/fd' % (self._procfs_path, pid)):
            try:
                inode = readlink('%s/%s/fd/%s' % (self._procfs_path, pid, fd))
            except OSError as err:
                if err.errno in (errno.ENOENT, errno.ESRCH):
                    continue
                elif err.errno == errno.EINVAL:
                    continue
                else:
                    raise
            else:
                if inode.startswith('socket:['):
                    inode = inode[8:][:-1]
                    inodes[inode].append((pid, int(fd)))

        return inodes

    def get_all_inodes(self):
        inodes = {}
        for pid in pids():
            try:
                inodes.update(self.get_proc_inodes(pid))
            except OSError as err:
                if err.errno not in (
                 errno.ENOENT, errno.ESRCH, errno.EPERM, errno.EACCES):
                    raise

        return inodes

    def decode_address(self, addr, family):
        """Accept an "ip:port" address as displayed in /proc/net/*
        and convert it into a human readable form, like:

        "0500000A:0016" -> ("10.0.0.5", 22)
        "0000000000000000FFFF00000100007F:9E49" -> ("::ffff:127.0.0.1", 40521)

        The IP address portion is a little or big endian four-byte
        hexadecimal number; that is, the least significant byte is listed
        first, so we need to reverse the order of the bytes to convert it
        to an IP address.
        The port is represented as a two-byte hexadecimal number.

        Reference:
        http://linuxdevcenter.com/pub/a/linux/2000/11/16/LinuxAdmin.html
        """
        ip, port = addr.split(':')
        port = int(port, 16)
        if not port:
            return ()
        if PY3:
            ip = ip.encode('ascii')
        if family == socket.AF_INET:
            if LITTLE_ENDIAN:
                ip = socket.inet_ntop(family, base64.b16decode(ip)[::-1])
            else:
                ip = socket.inet_ntop(family, base64.b16decode(ip))
        else:
            ip = base64.b16decode(ip)
            try:
                if LITTLE_ENDIAN:
                    ip = socket.inet_ntop(socket.AF_INET6, struct.pack('>4I', *struct.unpack('<4I', ip)))
                else:
                    ip = socket.inet_ntop(socket.AF_INET6, struct.pack('<4I', *struct.unpack('<4I', ip)))
            except ValueError:
                if not supports_ipv6():
                    raise _Ipv6UnsupportedError
                else:
                    raise

        return (
         ip, port)

    def process_inet(self, file, family, type_, inodes, filter_pid=None):
        """Parse /proc/net/tcp* and /proc/net/udp* files."""
        if file.endswith('6') and not os.path.exists(file):
            return
        else:
            with open_text(file, buffering=BIGGER_FILE_BUFFERING) as (f):
                f.readline()
                for lineno, line in enumerate(f, 1):
                    try:
                        _, laddr, raddr, status, _, _, _, _, _, inode = line.split()[:10]
                    except ValueError:
                        raise RuntimeError('error while parsing %s; malformed line %s %r' % (
                         file, lineno, line))

                    if inode in inodes:
                        pid, fd = inodes[inode][0]
                    else:
                        pid, fd = (None, -1)
                    if filter_pid is not None and filter_pid != pid:
                        continue
                    else:
                        if type_ == socket.SOCK_STREAM:
                            status = TCP_STATUSES[status]
                        else:
                            status = _common.CONN_NONE
                        try:
                            laddr = self.decode_address(laddr, family)
                            raddr = self.decode_address(raddr, family)
                        except _Ipv6UnsupportedError:
                            continue

                        yield (
                         fd, family, type_, laddr, raddr, status, pid)

            return

    def process_unix(self, file, family, inodes, filter_pid=None):
        """Parse /proc/net/unix files."""
        with open_text(file, buffering=BIGGER_FILE_BUFFERING) as (f):
            f.readline()
            for line in f:
                tokens = line.split()
                try:
                    _, _, _, _, type_, _, inode = tokens[0:7]
                except ValueError:
                    if ' ' not in line:
                        continue
                    raise RuntimeError('error while parsing %s; malformed line %r' % (
                     file, line))

                if inode in inodes:
                    pairs = inodes[inode]
                else:
                    pairs = [
                     (None, -1)]
                for pid, fd in pairs:
                    if filter_pid is not None and filter_pid != pid:
                        continue
                    else:
                        if len(tokens) == 8:
                            path = tokens[(-1)]
                        else:
                            path = ''
                        type_ = int(type_)
                        raddr = None
                        status = _common.CONN_NONE
                        yield (fd, family, type_, path, raddr, status, pid)

        return

    def retrieve(self, kind, pid=None):
        if kind not in self.tmap:
            raise ValueError('invalid %r kind argument; choose between %s' % (
             kind, (', ').join([ repr(x) for x in self.tmap ])))
        self._procfs_path = get_procfs_path()
        if pid is not None:
            inodes = self.get_proc_inodes(pid)
            if not inodes:
                return []
        else:
            inodes = self.get_all_inodes()
        ret = set()
        for f, family, type_ in self.tmap[kind]:
            if family in (socket.AF_INET, socket.AF_INET6):
                ls = self.process_inet('%s/net/%s' % (self._procfs_path, f), family, type_, inodes, filter_pid=pid)
            else:
                ls = self.process_unix('%s/net/%s' % (self._procfs_path, f), family, inodes, filter_pid=pid)
            for fd, family, type_, laddr, raddr, status, bound_pid in ls:
                if pid:
                    conn = _common.pconn(fd, family, type_, laddr, raddr, status)
                else:
                    conn = _common.sconn(fd, family, type_, laddr, raddr, status, bound_pid)
                ret.add(conn)

        return list(ret)


_connections = Connections()

def net_connections(kind='inet'):
    """Return system-wide open connections."""
    return _connections.retrieve(kind)


def net_io_counters():
    """Return network I/O statistics for every network interface
    installed on the system as a dict of raw tuples.
    """
    with open_text('%s/net/dev' % get_procfs_path()) as (f):
        lines = f.readlines()
    retdict = {}
    for line in lines[2:]:
        colon = line.rfind(':')
        assert colon > 0, repr(line)
        name = line[:colon].strip()
        fields = line[colon + 1:].strip().split()
        bytes_recv = int(fields[0])
        packets_recv = int(fields[1])
        errin = int(fields[2])
        dropin = int(fields[3])
        bytes_sent = int(fields[8])
        packets_sent = int(fields[9])
        errout = int(fields[10])
        dropout = int(fields[11])
        retdict[name] = (bytes_sent, bytes_recv, packets_sent, packets_recv,
         errin, errout, dropin, dropout)

    return retdict


def net_if_stats():
    """Get NIC stats (isup, duplex, speed, mtu)."""
    duplex_map = {cext.DUPLEX_FULL: NIC_DUPLEX_FULL, cext.DUPLEX_HALF: NIC_DUPLEX_HALF, 
       cext.DUPLEX_UNKNOWN: NIC_DUPLEX_UNKNOWN}
    names = net_io_counters().keys()
    ret = {}
    for name in names:
        isup, duplex, speed, mtu = cext.net_if_stats(name)
        duplex = duplex_map[duplex]
        ret[name] = _common.snicstats(isup, duplex, speed, mtu)

    return ret


disk_usage = _psposix.disk_usage

def disk_io_counters():
    """Return disk I/O statistics for every disk installed on the
    system as a dict of raw tuples.
    """

    def get_partitions():
        partitions = []
        with open_text('%s/partitions' % get_procfs_path()) as (f):
            lines = f.readlines()[2:]
        for line in reversed(lines):
            _, _, _, name = line.split()
            if name[(-1)].isdigit():
                partitions.append(name)
            elif not partitions or not partitions[(-1)].startswith(name):
                partitions.append(name)

        return partitions

    retdict = {}
    partitions = get_partitions()
    with open_text('%s/diskstats' % get_procfs_path()) as (f):
        lines = f.readlines()
    for line in lines:
        fields = line.split()
        fields_len = len(fields)
        if fields_len == 15:
            name = fields[3]
            reads = int(fields[2])
            reads_merged, rbytes, rtime, writes, writes_merged, wbytes, wtime, _, busy_time, _ = map(int, fields[4:14])
        elif fields_len == 14:
            name = fields[2]
            reads, reads_merged, rbytes, rtime, writes, writes_merged, wbytes, wtime, _, busy_time, _ = map(int, fields[3:14])
        elif fields_len == 7:
            name = fields[2]
            reads, rbytes, writes, wbytes = map(int, fields[3:])
            rtime = wtime = reads_merged = writes_merged = busy_time = 0
        else:
            raise ValueError('not sure how to interpret line %r' % line)
        if name in partitions:
            rbytes = rbytes * SECTOR_SIZE
            wbytes = wbytes * SECTOR_SIZE
            retdict[name] = (reads, writes, rbytes, wbytes, rtime, wtime,
             reads_merged, writes_merged, busy_time)

    return retdict


def disk_partitions(all=False):
    """Return mounted disk partitions as a list of namedtuples"""
    fstypes = set()
    with open_text('%s/filesystems' % get_procfs_path()) as (f):
        for line in f:
            line = line.strip()
            if not line.startswith('nodev'):
                fstypes.add(line.strip())
            else:
                fstype = line.split('\t')[1]
                if fstype == 'zfs':
                    fstypes.add('zfs')

    retlist = []
    partitions = cext.disk_partitions()
    for partition in partitions:
        device, mountpoint, fstype, opts = partition
        if device == 'none':
            device = ''
        if not all:
            if device == '' or fstype not in fstypes:
                continue
        ntuple = _common.sdiskpart(device, mountpoint, fstype, opts)
        retlist.append(ntuple)

    return retlist


def users():
    """Return currently connected users as a list of namedtuples."""
    retlist = []
    rawlist = cext.users()
    for item in rawlist:
        user, tty, hostname, tstamp, user_process = item
        if not user_process:
            continue
        if hostname == ':0.0' or hostname == ':0':
            hostname = 'localhost'
        nt = _common.suser(user, tty or None, hostname, tstamp)
        retlist.append(nt)

    return retlist


def boot_time():
    """Return the system boot time expressed in seconds since the epoch."""
    global BOOT_TIME
    with open_binary('%s/stat' % get_procfs_path()) as (f):
        for line in f:
            if line.startswith('btime'):
                ret = float(line.strip().split()[1])
                BOOT_TIME = ret
                return ret

        raise RuntimeError("line 'btime' not found in %s/stat" % get_procfs_path())


def pids():
    """Returns a list of PIDs currently running on the system."""
    return [ int(x) for x in os.listdir(b(get_procfs_path())) if x.isdigit() ]


def pid_exists(pid):
    """Check For the existence of a unix pid."""
    return _psposix.pid_exists(pid)


def wrap_exceptions(fun):
    """Decorator which translates bare OSError and IOError exceptions
    into NoSuchProcess and AccessDenied.
    """

    @functools.wraps(fun)
    def wrapper(self, *args, **kwargs):
        try:
            return fun(self, *args, **kwargs)
        except EnvironmentError as err:
            if err.errno in (errno.ENOENT, errno.ESRCH):
                raise NoSuchProcess(self.pid, self._name)
            if err.errno in (errno.EPERM, errno.EACCES):
                raise AccessDenied(self.pid, self._name)
            raise

    return wrapper


class Process(object):
    """Linux process implementation."""
    __slots__ = [
     'pid', '_name', '_ppid', '_procfs_path']

    def __init__(self, pid):
        self.pid = pid
        self._name = None
        self._ppid = None
        self._procfs_path = get_procfs_path()
        return

    def _parse_stat_file(self):
        """Parse /proc/{pid}/stat file. Return a list of fields where
        process name is in position 0.
        Using "man proc" as a reference: where "man proc" refers to
        position N, always subscract 2 (e.g starttime pos 22 in
        'man proc' == pos 20 in the list returned here).
        """
        with open_binary('%s/%s/stat' % (self._procfs_path, self.pid)) as (f):
            data = f.read()
        rpar = data.rfind(')')
        name = data[data.find('(') + 1:rpar]
        fields_after_name = data[rpar + 2:].split()
        return [name] + fields_after_name

    def _read_status_file(self):
        with open_binary('%s/%s/status' % (self._procfs_path, self.pid)) as (f):
            return f.read()

    def _read_smaps_file(self):
        with open_binary('%s/%s/smaps' % (self._procfs_path, self.pid), buffering=BIGGER_FILE_BUFFERING) as (f):
            return f.read().strip()

    @wrap_exceptions
    def name(self):
        name = self._parse_stat_file()[0]
        if PY3:
            name = decode(name)
        return name

    def exe(self):
        try:
            return readlink('%s/%s/exe' % (self._procfs_path, self.pid))
        except OSError as err:
            if err.errno in (errno.ENOENT, errno.ESRCH):
                if os.path.lexists('%s/%s' % (self._procfs_path, self.pid)):
                    return ''
                if not pid_exists(self.pid):
                    raise NoSuchProcess(self.pid, self._name)
                else:
                    raise ZombieProcess(self.pid, self._name, self._ppid)
            if err.errno in (errno.EPERM, errno.EACCES):
                raise AccessDenied(self.pid, self._name)
            raise

    @wrap_exceptions
    def cmdline(self):
        with open_text('%s/%s/cmdline' % (self._procfs_path, self.pid)) as (f):
            data = f.read()
        if not data:
            return []
        if data.endswith('\x00'):
            data = data[:-1]
        return [ x for x in data.split('\x00') ]

    @wrap_exceptions
    def environ(self):
        with open_text('%s/%s/environ' % (self._procfs_path, self.pid)) as (f):
            data = f.read()
        return parse_environ_block(data)

    @wrap_exceptions
    def terminal(self):
        tty_nr = int(self._parse_stat_file()[5])
        tmap = _psposix.get_terminal_map()
        try:
            return tmap[tty_nr]
        except KeyError:
            return

        return

    if os.path.exists('/proc/%s/io' % os.getpid()):

        @wrap_exceptions
        def io_counters(self):
            fname = '%s/%s/io' % (self._procfs_path, self.pid)
            with open_binary(fname) as (f):
                rcount = wcount = rbytes = wbytes = None
                for line in f:
                    if rcount is None and line.startswith('syscr'):
                        rcount = int(line.split()[1])
                    elif wcount is None and line.startswith('syscw'):
                        wcount = int(line.split()[1])
                    elif rbytes is None and line.startswith('read_bytes'):
                        rbytes = int(line.split()[1])
                    elif wbytes is None and line.startswith('write_bytes'):
                        wbytes = int(line.split()[1])

                for x in (rcount, wcount, rbytes, wbytes):
                    if x is None:
                        raise NotImplementedError("couldn't read all necessary info from %r" % fname)

                return _common.pio(rcount, wcount, rbytes, wbytes)
            return

    else:

        def io_counters(self):
            raise NotImplementedError("couldn't find /proc/%s/io (kernel too old?)" % self.pid)

    @wrap_exceptions
    def cpu_times(self):
        values = self._parse_stat_file()
        utime = float(values[12]) / CLOCK_TICKS
        stime = float(values[13]) / CLOCK_TICKS
        children_utime = float(values[14]) / CLOCK_TICKS
        children_stime = float(values[15]) / CLOCK_TICKS
        return _common.pcputimes(utime, stime, children_utime, children_stime)

    @wrap_exceptions
    def wait(self, timeout=None):
        try:
            return _psposix.wait_pid(self.pid, timeout)
        except _psposix.TimeoutExpired:
            raise TimeoutExpired(timeout, self.pid, self._name)

    @wrap_exceptions
    def create_time(self):
        values = self._parse_stat_file()
        bt = BOOT_TIME or boot_time()
        return float(values[20]) / CLOCK_TICKS + bt

    @wrap_exceptions
    def memory_info(self):
        with open_binary('%s/%s/statm' % (self._procfs_path, self.pid)) as (f):
            vms, rss, shared, text, lib, data, dirty = [ int(x) * PAGESIZE for x in f.readline().split()[:7] ]
        return pmem(rss, vms, shared, text, lib, data, dirty)

    if HAS_SMAPS:

        @wrap_exceptions
        def memory_full_info(self, _private_re=re.compile('Private.*:\\s+(\\d+)'), _pss_re=re.compile('Pss.*:\\s+(\\d+)'), _swap_re=re.compile('Swap.*:\\s+(\\d+)')):
            basic_mem = self.memory_info()
            smaps_data = self._read_smaps_file()
            uss = sum(map(int, _private_re.findall(smaps_data))) * 1024
            pss = sum(map(int, _pss_re.findall(smaps_data))) * 1024
            swap = sum(map(int, _swap_re.findall(smaps_data))) * 1024
            return pfullmem(*(basic_mem + (uss, pss, swap)))

    else:
        memory_full_info = memory_info
    if HAS_SMAPS:

        @wrap_exceptions
        def memory_maps(self):
            """Return process's mapped memory regions as a list of named
            tuples. Fields are explained in 'man proc'; here is an updated
            (Apr 2012) version: http://goo.gl/fmebo
            """

            def get_blocks(lines, current_block):
                data = {}
                for line in lines:
                    fields = line.split(None, 5)
                    if not fields[0].endswith(':'):
                        yield (current_block.pop(), data)
                        current_block.append(line)
                    else:
                        try:
                            data[fields[0]] = int(fields[1]) * 1024
                        except ValueError:
                            if fields[0].startswith('VmFlags:'):
                                continue
                            else:
                                raise ValueError("don't know how to interpret line %r" % line)

                yield (
                 current_block.pop(), data)
                return

            data = self._read_smaps_file()
            if not data:
                return []
            else:
                lines = data.split('\n')
                ls = []
                first_line = lines.pop(0)
                current_block = [first_line]
                for header, data in get_blocks(lines, current_block):
                    hfields = header.split(None, 5)
                    try:
                        addr, perms, offset, dev, inode, path = hfields
                    except ValueError:
                        addr, perms, offset, dev, inode, path = hfields + ['']

                    if not path:
                        path = '[anon]'
                    else:
                        if PY3:
                            path = decode(path)
                        path = path.strip()
                        if path.endswith(' (deleted)') and not path_exists_strict(path):
                            path = path[:-10]
                    ls.append((
                     decode(addr), decode(perms), path,
                     data['Rss:'],
                     data.get('Size:', 0),
                     data.get('Pss:', 0),
                     data.get('Shared_Clean:', 0),
                     data.get('Shared_Dirty:', 0),
                     data.get('Private_Clean:', 0),
                     data.get('Private_Dirty:', 0),
                     data.get('Referenced:', 0),
                     data.get('Anonymous:', 0),
                     data.get('Swap:', 0)))

                return ls

    else:

        def memory_maps(self):
            raise NotImplementedError('/proc/%s/smaps does not exist on kernels < 2.6.14 or if CONFIG_MMU kernel configuration option is not enabled.' % self.pid)

    @wrap_exceptions
    def cwd(self):
        return readlink('%s/%s/cwd' % (self._procfs_path, self.pid))

    @wrap_exceptions
    def num_ctx_switches(self, _ctxsw_re=re.compile('ctxt_switches:\t(\\d+)')):
        data = self._read_status_file()
        ctxsw = _ctxsw_re.findall(data)
        if not ctxsw:
            raise NotImplementedError("'voluntary_ctxt_switches' and 'nonvoluntary_ctxt_switches'lines were not found in /proc/%s/status; the kernel is probably older than 2.6.23" % self.pid)
        else:
            return _common.pctxsw(int(ctxsw[0]), int(ctxsw[1]))

    @wrap_exceptions
    def num_threads(self, _num_threads_re=re.compile('Threads:\t(\\d+)')):
        data = self._read_status_file()
        return int(_num_threads_re.findall(data)[0])

    @wrap_exceptions
    def threads(self):
        thread_ids = os.listdir('%s/%s/task' % (self._procfs_path, self.pid))
        thread_ids.sort()
        retlist = []
        hit_enoent = False
        for thread_id in thread_ids:
            fname = '%s/%s/task/%s/stat' % (
             self._procfs_path, self.pid, thread_id)
            try:
                with open_binary(fname) as (f):
                    st = f.read().strip()
            except IOError as err:
                if err.errno == errno.ENOENT:
                    hit_enoent = True
                    continue
                raise

            st = st[st.find(')') + 2:]
            values = st.split(' ')
            utime = float(values[11]) / CLOCK_TICKS
            stime = float(values[12]) / CLOCK_TICKS
            ntuple = _common.pthread(int(thread_id), utime, stime)
            retlist.append(ntuple)

        if hit_enoent:
            os.stat('%s/%s' % (self._procfs_path, self.pid))
        return retlist

    @wrap_exceptions
    def nice_get(self):
        return cext_posix.getpriority(self.pid)

    @wrap_exceptions
    def nice_set(self, value):
        return cext_posix.setpriority(self.pid, value)

    @wrap_exceptions
    def cpu_affinity_get(self):
        return cext.proc_cpu_affinity_get(self.pid)

    @wrap_exceptions
    def cpu_affinity_set(self, cpus):
        try:
            cext.proc_cpu_affinity_set(self.pid, cpus)
        except OSError as err:
            if err.errno == errno.EINVAL:
                allcpus = tuple(range(len(per_cpu_times())))
                for cpu in cpus:
                    if cpu not in allcpus:
                        raise ValueError('invalid CPU #%i (choose between %s)' % (
                         cpu, allcpus))

            raise

    if hasattr(cext, 'proc_ioprio_get'):

        @wrap_exceptions
        def ionice_get(self):
            ioclass, value = cext.proc_ioprio_get(self.pid)
            if enum is not None:
                ioclass = IOPriority(ioclass)
            return _common.pionice(ioclass, value)

        @wrap_exceptions
        def ionice_set(self, ioclass, value):
            if value is not None:
                if not PY3 and not isinstance(value, (int, long)):
                    msg = 'value argument is not an integer (gor %r)' % value
                    raise TypeError(msg)
                if not 0 <= value <= 7:
                    raise ValueError('value argument range expected is between 0 and 7')
            if ioclass in (IOPRIO_CLASS_NONE, None):
                if value:
                    msg = "can't specify value with IOPRIO_CLASS_NONE (got %r)" % value
                    raise ValueError(msg)
                ioclass = IOPRIO_CLASS_NONE
                value = 0
            elif ioclass == IOPRIO_CLASS_IDLE:
                if value:
                    msg = "can't specify value with IOPRIO_CLASS_IDLE (got %r)" % value
                    raise ValueError(msg)
                value = 0
            elif ioclass in (IOPRIO_CLASS_RT, IOPRIO_CLASS_BE):
                if value is None:
                    value = 4
            else:
                raise ValueError('invalid ioclass argument %r' % ioclass)
            return cext.proc_ioprio_set(self.pid, ioclass, value)

    if HAS_PRLIMIT:

        @wrap_exceptions
        def rlimit(self, resource, limits=None):
            if self.pid == 0:
                raise ValueError("can't use prlimit() against PID 0 process")
            try:
                if limits is None:
                    return cext.linux_prlimit(self.pid, resource)
                if len(limits) != 2:
                    raise ValueError('second argument must be a (soft, hard) tuple, got %s' % repr(limits))
                soft, hard = limits
                cext.linux_prlimit(self.pid, resource, soft, hard)
            except OSError as err:
                if err.errno == errno.ENOSYS and pid_exists(self.pid):
                    raise ZombieProcess(self.pid, self._name, self._ppid)
                else:
                    raise

            return

    @wrap_exceptions
    def status(self):
        letter = self._parse_stat_file()[1]
        if PY3:
            letter = letter.decode()
        return PROC_STATUSES.get(letter, '?')

    @wrap_exceptions
    def open_files(self):
        retlist = []
        files = os.listdir('%s/%s/fd' % (self._procfs_path, self.pid))
        hit_enoent = False
        for fd in files:
            file = '%s/%s/fd/%s' % (self._procfs_path, self.pid, fd)
            try:
                path = readlink(file)
            except OSError as err:
                if err.errno in (errno.ENOENT, errno.ESRCH):
                    hit_enoent = True
                    continue
                elif err.errno == errno.EINVAL:
                    continue
                else:
                    raise
            else:
                if path.startswith('/') and isfile_strict(path):
                    file = '%s/%s/fdinfo/%s' % (
                     self._procfs_path, self.pid, fd)
                    with open_binary(file) as (f):
                        pos = int(f.readline().split()[1])
                        flags = int(f.readline().split()[1], 8)
                    mode = file_flags_to_mode(flags)
                    ntuple = popenfile(path, int(fd), int(pos), mode, flags)
                    retlist.append(ntuple)

        if hit_enoent:
            os.stat('%s/%s' % (self._procfs_path, self.pid))
        return retlist

    @wrap_exceptions
    def connections(self, kind='inet'):
        ret = _connections.retrieve(kind, self.pid)
        os.stat('%s/%s' % (self._procfs_path, self.pid))
        return ret

    @wrap_exceptions
    def num_fds(self):
        return len(os.listdir('%s/%s/fd' % (self._procfs_path, self.pid)))

    @wrap_exceptions
    def ppid(self):
        return int(self._parse_stat_file()[2])

    @wrap_exceptions
    def uids(self, _uids_re=re.compile('Uid:\t(\\d+)\t(\\d+)\t(\\d+)')):
        data = self._read_status_file()
        real, effective, saved = _uids_re.findall(data)[0]
        return _common.puids(int(real), int(effective), int(saved))

    @wrap_exceptions
    def gids(self, _gids_re=re.compile('Gid:\t(\\d+)\t(\\d+)\t(\\d+)')):
        data = self._read_status_file()
        real, effective, saved = _gids_re.findall(data)[0]
        return _common.pgids(int(real), int(effective), int(saved))