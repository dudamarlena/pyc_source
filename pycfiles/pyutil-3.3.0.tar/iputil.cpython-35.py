# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/code/pyutil/pyutil/iputil.py
# Compiled at: 2019-06-26 11:58:00
# Size of source mod 2**32: 9825 bytes
import os, re, socket, sys, subprocess
from twisted.internet import defer, threads, reactor
from twisted.internet.protocol import DatagramProtocol
from twisted.python.procutils import which
from twisted.python import log
try:
    import resource

    def increase_rlimits():
        try:
            current = resource.getrlimit(resource.RLIMIT_NOFILE)
        except AttributeError:
            return

        if current[0] >= 1024:
            return
        try:
            if current[1] > 0 and current[1] < 1000000:
                resource.setrlimit(resource.RLIMIT_NOFILE, (
                 current[1], current[1]))
            else:
                resource.setrlimit(resource.RLIMIT_NOFILE, (-1, -1))
                new = resource.getrlimit(resource.RLIMIT_NOFILE)
            if new[0] == current[0]:
                resource.setrlimit(resource.RLIMIT_NOFILE, (3200, -1))
        except ValueError:
            log.msg('unable to set RLIMIT_NOFILE: current value %s' % (
             resource.getrlimit(resource.RLIMIT_NOFILE),))
        except:
            log.err()


except ImportError:

    def _increase_rlimits():
        pass


    increase_rlimits = _increase_rlimits

def get_local_addresses_async(target='198.41.0.4'):
    """
    Return a Deferred that fires with a list of IPv4 addresses (as dotted-quad
    strings) that are currently configured on this host, sorted in descending
    order of how likely we think they are to work.

    @param target: we want to learn an IP address they could try using to
        connect to us; The default value is fine, but it might help if you
        pass the address of a host that you are actually trying to be
        reachable to.
    """
    addresses = []
    local_ip = get_local_ip_for(target)
    if local_ip:
        addresses.append(local_ip)
    if sys.platform == 'cygwin':
        d = _cygwin_hack_find_addresses(target)
    else:
        d = _find_addresses_via_config()

    def _collect(res):
        for addr in res:
            if addr != '0.0.0.0' and addr not in addresses:
                addresses.append(addr)

        return addresses

    d.addCallback(_collect)
    return d


def get_local_ip_for(target):
    """Find out what our IP address is for use by a given target.

    @return: the IP address as a dotted-quad string which could be used by
              to connect to us. It might work for them, it might not. If
              there is no suitable address (perhaps we don't currently have an
              externally-visible interface), this will return None.
    """
    try:
        target_ipaddr = socket.gethostbyname(target)
    except socket.gaierror:
        return

    udpprot = DatagramProtocol()
    port = reactor.listenUDP(0, udpprot)
    try:
        udpprot.transport.connect(target_ipaddr, 7)
        localip = udpprot.transport.getHost().host
    except socket.error:
        localip = None

    port.stopListening()
    return localip


_platform_map = {'linux-i386': 'linux', 
 'linux-ppc': 'linux', 
 'linux2': 'linux', 
 'linux3': 'linux', 
 'win32': 'win32', 
 'irix6-n32': 'irix', 
 'irix6-n64': 'irix', 
 'irix6': 'irix', 
 'openbsd2': 'bsd', 
 'openbsd3': 'bsd', 
 'openbsd4': 'bsd', 
 'openbsd5': 'bsd', 
 'darwin': 'bsd', 
 'freebsd4': 'bsd', 
 'freebsd5': 'bsd', 
 'freebsd6': 'bsd', 
 'freebsd7': 'bsd', 
 'freebsd8': 'bsd', 
 'freebsd9': 'bsd', 
 'netbsd1': 'bsd', 
 'netbsd2': 'bsd', 
 'netbsd3': 'bsd', 
 'netbsd4': 'bsd', 
 'netbsd5': 'bsd', 
 'netbsd6': 'bsd', 
 'dragonfly2': 'bsd', 
 'sunos5': 'sunos', 
 'cygwin': 'cygwin'}

class UnsupportedPlatformError(Exception):
    pass


_win32_path = 'route.exe'
_win32_args = ('print', )
_win32_re = re.compile('^\\s*\\d+\\.\\d+\\.\\d+\\.\\d+\\s.+\\s(?P<address>\\d+\\.\\d+\\.\\d+\\.\\d+)\\s+(?P<metric>\\d+)\\s*$', flags=re.M | re.I | re.S)
_linux_path = '/sbin/ifconfig'
_linux_re = re.compile('^\\s*inet [a-zA-Z]*:?(?P<address>\\d+\\.\\d+\\.\\d+\\.\\d+)\\s.+$', flags=re.M | re.I | re.S)
_netbsd_path = '/sbin/ifconfig'
_netbsd_args = ('-a', )
_netbsd_re = re.compile('^\\s+inet [a-zA-Z]*:?(?P<address>\\d+\\.\\d+\\.\\d+\\.\\d+)\\s.+$', flags=re.M | re.I | re.S)
_irix_path = '/usr/etc/ifconfig'
_sunos_path = '/usr/sbin/ifconfig'
_tool_map = {'linux': (_linux_path, (), _linux_re), 
 'win32': (_win32_path, _win32_args, _win32_re), 
 'cygwin': (_win32_path, _win32_args, _win32_re), 
 'bsd': (_netbsd_path, _netbsd_args, _netbsd_re), 
 'irix': (_irix_path, _netbsd_args, _netbsd_re), 
 'sunos': (_sunos_path, _netbsd_args, _netbsd_re)}

def _find_addresses_via_config():
    return threads.deferToThread(_synchronously_find_addresses_via_config)


def _synchronously_find_addresses_via_config():
    platform = _platform_map.get(sys.platform)
    if not platform:
        raise UnsupportedPlatformError(sys.platform)
    pathtotool, args, regex = _tool_map[platform]
    if os.path.isabs(pathtotool):
        return _query(pathtotool, args, regex)
    else:
        exes_to_try = which(pathtotool)
        for exe in exes_to_try:
            try:
                addresses = _query(exe, args, regex)
            except Exception:
                addresses = []

            if addresses:
                return addresses

        return []


def _query(path, args, regex):
    env = {'LANG': 'en_US.UTF-8'}
    p = subprocess.Popen([path] + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    output, err = p.communicate()
    addresses = []
    outputsplit = output.split('\n')
    for outline in outputsplit:
        m = regex.match(outline)
        if m:
            addr = m.groupdict()['address']
            if addr not in addresses:
                addresses.append(addr)

    return addresses


def _cygwin_hack_find_addresses(target):
    addresses = []
    for h in [target, 'localhost', '127.0.0.1']:
        try:
            addr = get_local_ip_for(h)
            if addr not in addresses:
                addresses.append(addr)
        except socket.gaierror:
            pass

    return defer.succeed(addresses)