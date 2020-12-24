# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bacpypes/pdu.py
# Compiled at: 2020-04-20 14:21:19
"""
PDU
"""
import re, socket, struct
try:
    import netifaces
except ImportError:
    netifaces = None

from .settings import settings
from .debugging import ModuleLogger, bacpypes_debugging, btox, xtob
from .comm import PCI as _PCI, PDUData
_short_mask = 65535
_long_mask = 4294967295
_debug = 0
_log = ModuleLogger(globals())
_field_address = '((?:\\d+)|(?:0x(?:[0-9A-Fa-f][0-9A-Fa-f])+))'
_ip_address_port = '(\\d+\\.\\d+\\.\\d+\\.\\d+)(?::(\\d+))?'
_ip_address_mask_port = '(\\d+\\.\\d+\\.\\d+\\.\\d+)(?:/(\\d+))?(?::(\\d+))?'
_net_ip_address_port = '(\\d+):' + _ip_address_port
_at_route = '(?:[@](?:' + _field_address + '|' + _ip_address_port + '))?'
field_address_re = re.compile('^' + _field_address + '$')
ip_address_port_re = re.compile('^' + _ip_address_port + '$')
ip_address_mask_port_re = re.compile('^' + _ip_address_mask_port + '$')
net_ip_address_port_re = re.compile('^' + _net_ip_address_port + '$')
net_ip_address_mask_port_re = re.compile('^' + _net_ip_address_port + '$')
ethernet_re = re.compile('^([0-9A-Fa-f][0-9A-Fa-f][:]){5}([0-9A-Fa-f][0-9A-Fa-f])$')
interface_re = re.compile('^(?:([\\w]+))(?::(\\d+))?$')
net_broadcast_route_re = re.compile('^([0-9])+:[*]' + _at_route + '$')
net_station_route_re = re.compile('^([0-9])+:' + _field_address + _at_route + '$')
net_ip_address_route_re = re.compile('^([0-9])+:' + _ip_address_port + _at_route + '$')
combined_pattern = re.compile('^(?:(?:([0-9]+)|([*])):)?(?:([*])|' + _field_address + '|' + _ip_address_mask_port + ')' + _at_route + '$')

@bacpypes_debugging
class Address():
    nullAddr = 0
    localBroadcastAddr = 1
    localStationAddr = 2
    remoteBroadcastAddr = 3
    remoteStationAddr = 4
    globalBroadcastAddr = 5

    def __init__(self, *args):
        if _debug:
            Address._debug('__init__ %r', args)
        self.addrType = Address.nullAddr
        self.addrNet = None
        self.addrAddr = None
        self.addrLen = None
        self.addrRoute = None
        if len(args) == 1:
            self.decode_address(args[0])
        elif len(args) == 2:
            self.decode_address(args[1])
            if self.addrType == Address.localStationAddr:
                self.addrType = Address.remoteStationAddr
                self.addrNet = args[0]
            elif self.addrType == Address.localBroadcastAddr:
                self.addrType = Address.remoteBroadcastAddr
                self.addrNet = args[0]
            else:
                raise ValueError('unrecognized address ctor form')
        return

    def decode_address(self, addr):
        """Initialize the address from a string.  Lots of different forms are supported."""
        if _debug:
            Address._debug('decode_address %r (%s)', addr, type(addr))
        self.addrType = Address.localStationAddr
        self.addrNet = None
        self.addrAddr = None
        self.addrLen = None
        self.addrRoute = None
        if addr == '*':
            if _debug:
                Address._debug('    - localBroadcast')
            self.addrType = Address.localBroadcastAddr
        elif addr == '*:*':
            if _debug:
                Address._debug('   - globalBroadcast')
            self.addrType = Address.globalBroadcastAddr
        elif isinstance(addr, int):
            if _debug:
                Address._debug('    - int')
            if addr < 0 or addr >= 256:
                raise ValueError('address out of range')
            self.addrAddr = struct.pack('B', addr)
            self.addrLen = 1
        elif isinstance(addr, basestring):
            if _debug:
                Address._debug('    - str')
            m = combined_pattern.match(addr)
            if m:
                if _debug:
                    Address._debug('    - combined pattern')
                net, global_broadcast, local_broadcast, local_addr, local_ip_addr, local_ip_net, local_ip_port, route_addr, route_ip_addr, route_ip_port = m.groups()
                if global_broadcast and local_broadcast:
                    if _debug:
                        Address._debug('    - global broadcast')
                    self.addrType = Address.globalBroadcastAddr
                elif net and local_broadcast:
                    if _debug:
                        Address._debug('    - remote broadcast')
                    net_addr = int(net)
                    if net_addr >= 65535:
                        raise ValueError('network out of range')
                    self.addrType = Address.remoteBroadcastAddr
                    self.addrNet = net_addr
                elif local_broadcast:
                    if _debug:
                        Address._debug('    - local broadcast')
                    self.addrType = Address.localBroadcastAddr
                elif net:
                    if _debug:
                        Address._debug('    - remote station')
                    net_addr = int(net)
                    if net_addr >= 65535:
                        raise ValueError('network out of range')
                    self.addrType = Address.remoteStationAddr
                    self.addrNet = net_addr
                if local_addr:
                    if _debug:
                        Address._debug('    - simple address')
                    if local_addr.startswith('0x'):
                        self.addrAddr = xtob(local_addr[2:])
                        self.addrLen = len(self.addrAddr)
                    else:
                        local_addr = int(local_addr)
                        if local_addr >= 256:
                            raise ValueError('address out of range')
                        self.addrAddr = struct.pack('B', local_addr)
                        self.addrLen = 1
                if local_ip_addr:
                    if _debug:
                        Address._debug('    - ip address')
                    if not local_ip_port:
                        local_ip_port = '47808'
                    local_ip_net = local_ip_net or '32'
                self.addrPort = int(local_ip_port)
                self.addrTuple = (local_ip_addr, self.addrPort)
                if _debug:
                    Address._debug('    - addrTuple: %r', self.addrTuple)
                addrstr = socket.inet_aton(local_ip_addr)
                self.addrIP = struct.unpack('!L', addrstr)[0]
                self.addrMask = _long_mask << 32 - int(local_ip_net) & _long_mask
                self.addrHost = self.addrIP & ~self.addrMask
                self.addrSubnet = self.addrIP & self.addrMask
                bcast = self.addrSubnet | ~self.addrMask
                self.addrBroadcastTuple = (socket.inet_ntoa(struct.pack('!L', bcast & _long_mask)), self.addrPort)
                if _debug:
                    Address._debug('    - addrBroadcastTuple: %r', self.addrBroadcastTuple)
                self.addrAddr = addrstr + struct.pack('!H', self.addrPort & _short_mask)
                self.addrLen = 6
            if not settings.route_aware and (route_addr or route_ip_addr):
                Address._warning('route provided but not route aware: %r', addr)
            if route_addr:
                self.addrRoute = Address(int(route_addr))
                if _debug:
                    Address._debug('    - addrRoute: %r', self.addrRoute)
            else:
                if route_ip_addr:
                    if not route_ip_port:
                        route_ip_port = '47808'
                    self.addrRoute = Address((route_ip_addr, int(route_ip_port)))
                    if _debug:
                        Address._debug('    - addrRoute: %r', self.addrRoute)
                return
            if ethernet_re.match(addr):
                if _debug:
                    Address._debug('    - ethernet')
                self.addrAddr = xtob(addr, ':')
                self.addrLen = len(self.addrAddr)
                return
            if re.match('^\\d+$', addr):
                if _debug:
                    Address._debug('    - int')
                addr = int(addr)
                if addr > 255:
                    raise ValueError('address out of range')
                self.addrAddr = struct.pack('B', addr)
                self.addrLen = 1
                return
            if re.match('^\\d+:[*]$', addr):
                if _debug:
                    Address._debug('    - remote broadcast')
                addr = int(addr[:-2])
                if addr >= 65535:
                    raise ValueError('network out of range')
                self.addrType = Address.remoteBroadcastAddr
                self.addrNet = addr
                self.addrAddr = None
                self.addrLen = None
                return
            if re.match('^\\d+:\\d+$', addr):
                if _debug:
                    Address._debug('    - remote station')
                net, addr = addr.split(':')
                net = int(net)
                addr = int(addr)
                if net >= 65535:
                    raise ValueError('network out of range')
                if addr > 255:
                    raise ValueError('address out of range')
                self.addrType = Address.remoteStationAddr
                self.addrNet = net
                self.addrAddr = struct.pack('B', addr)
                self.addrLen = 1
                return
            if re.match('^0x([0-9A-Fa-f][0-9A-Fa-f])+$', addr):
                if _debug:
                    Address._debug('    - modern hex string')
                self.addrAddr = xtob(addr[2:])
                self.addrLen = len(self.addrAddr)
                return
            if re.match("^X'([0-9A-Fa-f][0-9A-Fa-f])+'$", addr):
                if _debug:
                    Address._debug('    - old school hex string')
                self.addrAddr = xtob(addr[2:-1])
                self.addrLen = len(self.addrAddr)
                return
            if re.match('^\\d+:0x([0-9A-Fa-f][0-9A-Fa-f])+$', addr):
                if _debug:
                    Address._debug('    - remote station with modern hex string')
                net, addr = addr.split(':')
                net = int(net)
                if net >= 65535:
                    raise ValueError('network out of range')
                self.addrType = Address.remoteStationAddr
                self.addrNet = net
                self.addrAddr = xtob(addr[2:])
                self.addrLen = len(self.addrAddr)
                return
            if re.match("^\\d+:X'([0-9A-Fa-f][0-9A-Fa-f])+'$", addr):
                if _debug:
                    Address._debug('    - remote station with old school hex string')
                net, addr = addr.split(':')
                net = int(net)
                if net >= 65535:
                    raise ValueError('network out of range')
                self.addrType = Address.remoteStationAddr
                self.addrNet = net
                self.addrAddr = xtob(addr[2:-1])
                self.addrLen = len(self.addrAddr)
                return
            if netifaces and interface_re.match(addr):
                if _debug:
                    Address._debug('    - interface name with optional port')
                interface, port = interface_re.match(addr).groups()
                if port is not None:
                    self.addrPort = int(port)
                else:
                    self.addrPort = 47808
                interfaces = netifaces.interfaces()
                if interface not in interfaces:
                    raise ValueError('not an interface: %s' % (interface,))
                if _debug:
                    Address._debug('    - interfaces: %r', interfaces)
                ifaddresses = netifaces.ifaddresses(interface)
                if netifaces.AF_INET not in ifaddresses:
                    raise ValueError('interface does not support IPv4: %s' % (interface,))
                ipv4addresses = ifaddresses[netifaces.AF_INET]
                if len(ipv4addresses) > 1:
                    raise ValueError('interface supports multiple IPv4 addresses: %s' % (interface,))
                ifaddress = ipv4addresses[0]
                if _debug:
                    Address._debug('    - ifaddress: %r', ifaddress)
                addr = ifaddress['addr']
                self.addrTuple = (addr, self.addrPort)
                if _debug:
                    Address._debug('    - addrTuple: %r', self.addrTuple)
                addrstr = socket.inet_aton(addr)
                self.addrIP = struct.unpack('!L', addrstr)[0]
                if 'netmask' in ifaddress:
                    maskstr = socket.inet_aton(ifaddress['netmask'])
                    self.addrMask = struct.unpack('!L', maskstr)[0]
                else:
                    self.addrMask = _long_mask
                self.addrHost = self.addrIP & ~self.addrMask
                self.addrSubnet = self.addrIP & self.addrMask
                if 'broadcast' in ifaddress:
                    self.addrBroadcastTuple = (
                     ifaddress['broadcast'], self.addrPort)
                else:
                    self.addrBroadcastTuple = None
                if _debug:
                    Address._debug('    - addrBroadcastTuple: %r', self.addrBroadcastTuple)
                self.addrAddr = addrstr + struct.pack('!H', self.addrPort & _short_mask)
                self.addrLen = 6
                return
            raise ValueError('unrecognized format')
        elif isinstance(addr, tuple):
            addr, port = addr
            self.addrPort = int(port)
            if isinstance(addr, basestring):
                if not addr:
                    addrstr = '\x00\x00\x00\x00'
                else:
                    addrstr = socket.inet_aton(addr)
                self.addrTuple = (
                 addr, self.addrPort)
            elif isinstance(addr, (int, long)):
                addrstr = struct.pack('!L', addr & _long_mask)
                self.addrTuple = (socket.inet_ntoa(addrstr), self.addrPort)
            else:
                raise TypeError('tuple must be (string, port) or (long, port)')
            if _debug:
                Address._debug('    - addrstr: %r', addrstr)
            self.addrIP = struct.unpack('!L', addrstr)[0]
            self.addrMask = _long_mask
            self.addrHost = None
            self.addrSubnet = None
            self.addrBroadcastTuple = self.addrTuple
            self.addrAddr = addrstr + struct.pack('!H', self.addrPort & _short_mask)
            self.addrLen = 6
        else:
            raise TypeError('integer, string or tuple required')
        return

    def __str__(self):
        if self.addrType == Address.nullAddr:
            rslt = 'Null'
        elif self.addrType == Address.localBroadcastAddr:
            rslt = '*'
        elif self.addrType == Address.localStationAddr:
            rslt = ''
            if self.addrLen == 1:
                rslt += str(ord(self.addrAddr))
            else:
                port = struct.unpack('!H', self.addrAddr[-2:])[0]
                if len(self.addrAddr) == 6 and port >= 47808 and port <= 47823:
                    rslt += ('.').join([ '%d' % ord(x) for x in self.addrAddr[0:4] ])
                    if port != 47808:
                        rslt += ':' + str(port)
                else:
                    rslt += '0x' + btox(self.addrAddr)
        elif self.addrType == Address.remoteBroadcastAddr:
            rslt = '%d:*' % (self.addrNet,)
        elif self.addrType == Address.remoteStationAddr:
            rslt = '%d:' % (self.addrNet,)
            if self.addrLen == 1:
                rslt += str(ord(self.addrAddr[0]))
            else:
                port = struct.unpack('!H', self.addrAddr[-2:])[0]
                if len(self.addrAddr) == 6 and port >= 47808 and port <= 47823:
                    rslt += ('.').join([ '%d' % ord(x) for x in self.addrAddr[0:4] ])
                    if port != 47808:
                        rslt += ':' + str(port)
                else:
                    rslt += '0x' + btox(self.addrAddr)
        elif self.addrType == Address.globalBroadcastAddr:
            rslt = '*:*'
        else:
            raise TypeError('unknown address type %d' % self.addrType)
        if self.addrRoute:
            rslt += '@' + str(self.addrRoute)
        return rslt

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.__str__())

    def _tuple(self):
        if not settings.route_aware or self.addrRoute is None:
            return (self.addrType, self.addrNet, self.addrAddr, None)
        else:
            return (
             self.addrType, self.addrNet, self.addrAddr, self.addrRoute._tuple())
            return

    def __hash__(self):
        return hash(self._tuple())

    def __eq__(self, arg):
        if not isinstance(arg, Address):
            arg = Address(arg)
        rslt = self.addrType == arg.addrType
        rslt = rslt and self.addrNet == arg.addrNet
        rslt = rslt and self.addrAddr == arg.addrAddr
        if rslt and self.addrRoute and arg.addrRoute:
            rslt = rslt and self.addrRoute == arg.addrRoute
        return rslt

    def __ne__(self, arg):
        return not self.__eq__(arg)

    def __lt__(self, arg):
        return self._tuple() < arg._tuple()

    def dict_contents(self, use_dict=None, as_class=None):
        """Return the contents of an object as a dict."""
        if _debug:
            _log.debug('dict_contents use_dict=%r as_class=%r', use_dict, as_class)
        return str(self)


def pack_ip_addr(addr):
    """Given an IP address tuple like ('1.2.3.4', 47808) return the six-octet string
    useful for a BACnet address."""
    addr, port = addr
    return socket.inet_aton(addr) + struct.pack('!H', port & _short_mask)


def unpack_ip_addr(addr):
    """Given a six-octet BACnet address, return an IP address tuple."""
    return (
     socket.inet_ntoa(addr[0:4]), struct.unpack('!H', addr[4:6])[0])


class LocalStation(Address):

    def __init__(self, addr, route=None):
        self.addrType = Address.localStationAddr
        self.addrNet = None
        self.addrRoute = route
        if isinstance(addr, int):
            if addr < 0 or addr >= 256:
                raise ValueError('address out of range')
            self.addrAddr = struct.pack('B', addr)
            self.addrLen = 1
        elif isinstance(addr, (bytes, bytearray)):
            if _debug:
                Address._debug('    - bytes or bytearray')
            self.addrAddr = bytes(addr)
            self.addrLen = len(addr)
        else:
            raise TypeError('integer, bytes or bytearray required')
        return


class RemoteStation(Address):

    def __init__(self, net, addr, route=None):
        if not isinstance(net, int):
            raise TypeError('integer network required')
        if net < 0 or net >= 65535:
            raise ValueError('network out of range')
        self.addrType = Address.remoteStationAddr
        self.addrNet = net
        self.addrRoute = route
        if isinstance(addr, int):
            if addr < 0 or addr >= 256:
                raise ValueError('address out of range')
            self.addrAddr = struct.pack('B', addr)
            self.addrLen = 1
        elif isinstance(addr, (bytes, bytearray)):
            if _debug:
                Address._debug('    - bytes or bytearray')
            self.addrAddr = bytes(addr)
            self.addrLen = len(addr)
        else:
            raise TypeError('integer, bytes or bytearray required')


class LocalBroadcast(Address):

    def __init__(self, route=None):
        self.addrType = Address.localBroadcastAddr
        self.addrNet = None
        self.addrAddr = None
        self.addrLen = None
        self.addrRoute = route
        return


class RemoteBroadcast(Address):

    def __init__(self, net, route=None):
        if not isinstance(net, int):
            raise TypeError('integer network required')
        if net < 0 or net >= 65535:
            raise ValueError('network out of range')
        self.addrType = Address.remoteBroadcastAddr
        self.addrNet = net
        self.addrAddr = None
        self.addrLen = None
        self.addrRoute = route
        return


class GlobalBroadcast(Address):

    def __init__(self, route=None):
        self.addrType = Address.globalBroadcastAddr
        self.addrNet = None
        self.addrAddr = None
        self.addrLen = None
        self.addrRoute = route
        return


@bacpypes_debugging
class PCI(_PCI):
    _debug_contents = ('pduExpectingReply', 'pduNetworkPriority')

    def __init__(self, *args, **kwargs):
        if _debug:
            PCI._debug('__init__ %r %r', args, kwargs)
        my_kwargs = {}
        other_kwargs = {}
        for element in ('expectingReply', 'networkPriority'):
            if element in kwargs:
                my_kwargs[element] = kwargs[element]

        for kw in kwargs:
            if kw not in my_kwargs:
                other_kwargs[kw] = kwargs[kw]

        if _debug:
            PCI._debug('    - my_kwargs: %r', my_kwargs)
        if _debug:
            PCI._debug('    - other_kwargs: %r', other_kwargs)
        super(PCI, self).__init__(*args, **other_kwargs)
        self.pduExpectingReply = my_kwargs.get('expectingReply', 0)
        self.pduNetworkPriority = my_kwargs.get('networkPriority', 0)

    def update(self, pci):
        """Copy the PCI fields."""
        _PCI.update(self, pci)
        self.pduExpectingReply = pci.pduExpectingReply
        self.pduNetworkPriority = pci.pduNetworkPriority

    def pci_contents(self, use_dict=None, as_class=dict):
        """Return the contents of an object as a dict."""
        if _debug:
            PCI._debug('pci_contents use_dict=%r as_class=%r', use_dict, as_class)
        if use_dict is None:
            use_dict = as_class()
        _PCI.pci_contents(self, use_dict=use_dict, as_class=as_class)
        use_dict.__setitem__('expectingReply', self.pduExpectingReply)
        use_dict.__setitem__('networkPriority', self.pduNetworkPriority)
        return use_dict

    def dict_contents(self, use_dict=None, as_class=dict):
        """Return the contents of an object as a dict."""
        if _debug:
            PCI._debug('dict_contents use_dict=%r as_class=%r', use_dict, as_class)
        return self.pci_contents(use_dict=use_dict, as_class=as_class)


@bacpypes_debugging
class PDU(PCI, PDUData):

    def __init__(self, *args, **kwargs):
        if _debug:
            PDU._debug('__init__ %r %r', args, kwargs)
        super(PDU, self).__init__(*args, **kwargs)

    def __str__(self):
        return '<%s %s -> %s : %s>' % (self.__class__.__name__, self.pduSource, self.pduDestination, btox(self.pduData, '.'))

    def dict_contents(self, use_dict=None, as_class=dict):
        """Return the contents of an object as a dict."""
        if _debug:
            PDUData._debug('dict_contents use_dict=%r as_class=%r', use_dict, as_class)
        if use_dict is None:
            use_dict = as_class()
        self.pci_contents(use_dict=use_dict, as_class=as_class)
        self.pdudata_contents(use_dict=use_dict, as_class=as_class)
        return use_dict