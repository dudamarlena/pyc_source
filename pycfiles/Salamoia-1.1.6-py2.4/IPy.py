# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/utility/IPy.py
# Compiled at: 2007-12-02 16:26:55
""" IPy - class and tools for handling of IPv4 and IPv6 Addresses and Networks.

$Id: IPy.py,v 1.1 2004/06/05 07:40:33 marko Exp $

(modified slighly to remove python2.3 minor warnings)

The IP class allows a comfortable parsing and handling for most
notations in use for IPv4 and IPv6 Addresses and Networks. It was
greatly inspired bei RIPE's Perl module NET::IP's interface but
doesn't share the Implementation. It doesn't share non-CIDR netmasks,
so funky stuff lixe a netmask 0xffffff0f can't be done here.

    >>> ip = IP('127.0.0.0/30')
    >>> for x in ip:
    ...  print x
    ...
    127.0.0.0
    127.0.0.1
    127.0.0.2
    127.0.0.3
    >>> ip2 = IP('0x7f000000/30')
    >>> ip == ip2
    1
    >>> ip.reverseNames()
    ['0.0.0.127.in-addr.arpa.', '1.0.0.127.in-addr.arpa.', '2.0.0.127.in-addr.arpa.', '3.0.0.127.in-addr.arpa.']
    >>> ip.reverseName()
    '0-3.0.0.127.in-addr.arpa.'
    >>> ip.iptype()
    'PRIVATE'

It can detect about a dozen different ways of expressing IP addresses
and networks, parse them and distinguish between IPv4 and IPv6 addresses.

    >>> IP('10.0.0.0/8').version()
    4
    >>> IP('::1').version()
    6
    >>> print IP(0x7f000001)
    127.0.0.1
    >>> print IP('0x7f000001')
    127.0.0.1
    >>> print IP('127.0.0.1')
    127.0.0.1
    >>> print IP('10')
    10.0.0.0
    >>> print IP('1080:0:0:0:8:800:200C:417A')
    1080:0000:0000:0000:0008:0800:200c:417a
    >>> print IP('1080::8:800:200C:417A')
    1080:0000:0000:0000:0008:0800:200c:417a
    >>> print IP('::1')
    0000:0000:0000:0000:0000:0000:0000:0001
    >>> print IP('::13.1.68.3')
    0000:0000:0000:0000:0000:0000:0d01:4403
    >>> print IP('127.0.0.0/8')
    127.0.0.0/8
    >>> print IP('127.0.0.0/255.0.0.0')
    127.0.0.0/8
    >>> print IP('127.0.0.0-127.255.255.255')
    127.0.0.0/8

Nearly all class methods which return a string have an optional
parameter 'wantprefixlen' which controlles if the prefixlen or netmask
is printed. Per default the prefilen is always shown if the net
contains more than one address.

wantprefixlen == 0 / None        don't return anything    1.2.3.0
wantprefixlen == 1               /prefix                  1.2.3.0/24
wantprefixlen == 2               /netmask                 1.2.3.0/255.255.255.0
wantprefixlen == 3               -lastip                  1.2.3.0-1.2.3.255

You can also change the defaults on an per-object basis by fiddeling with the class members

NoPrefixForSingleIp
WantPrefixLen

    >>> IP('10.0.0.0/32').strNormal()
    '10.0.0.0'
    >>> IP('10.0.0.0/24').strNormal()
    '10.0.0.0/24'
    >>> IP('10.0.0.0/24').strNormal(0)
    '10.0.0.0'
    >>> IP('10.0.0.0/24').strNormal(1)
    '10.0.0.0/24'
    >>> IP('10.0.0.0/24').strNormal(2)
    '10.0.0.0/255.255.255.0'
    >>> IP('10.0.0.0/24').strNormal(3)
    '10.0.0.0-10.0.0.255'
    >>> ip = IP('10.0.0.0')
    >>> print ip
    10.0.0.0
    >>> ip.NoPrefixForSingleIp = None
    >>> print ip
    10.0.0.0/32
    >>> ip.WantPrefixLen = 3
    >>> print ip
    10.0.0.0-10.0.0.0
                

Further Information might be available at http://c0re.jp/c0de/IPy/

Hacked 2001 by drt@un.bewaff.net

TODO:
      * support for base85 encoding
      * support for output of IPv6 encoded IPv4 Addresses
      * update address type tables      
      * first-last notation should be allowed for IPv6
      * add IPv6 docstring examples
      * check better vor negative parameters
      * add addition / aggregation
      * move size in bits into class variables to get rid of some "if self._ipversion ..."
      * move reverse name stuff out of the classes and refactor it
      * support for aggregation of more than two nets at once
      * support for aggregation with "holes"
      * support for finding common prefix
      * '>>' and '<<' for prefix manipulation
      * better comparison (__cmp__ and friends)
      * support for checking if two networks overlap.
      * add our own exceptions instead ValueError all the time
      * always write hex values lowercase
      * interpret 2001:1234:5678:1234/64 as 2001:1234:5678:1234::/64
      * rename checkPrefix to checkPrefixOk
      * add more documentation and doctests
      * refactor
"""
import sys
types = sys.modules['types']
IPv4ranges = {'0': 'PUBLIC', '00000000': 'PRIVATE', '00001010': 'PRIVATE', '01111111': 'PRIVATE', '1': 'PUBLIC', '101011000001': 'PRIVATE', '1100000010101000': 'PRIVATE', '11011111': 'RESERVED', '111': 'RESERVED'}
IPv6ranges = {'00000000': 'RESERVED', '00000001': 'UNASSIGNED', '0000001': 'NSAP', '0000010': 'IPX', '0000011': 'UNASSIGNED', '00001': 'UNASSIGNED', '0001': 'UNASSIGNED', '0010000000000000': 'RESERVED', '0010000000000001': 'ASSIGNABLE', '00100000000000010000000': 'ASSIGNABLE IANA', '00100000000000010000001': 'ASSIGNABLE APNIC', '00100000000000010000010': 'ASSIGNABLE ARIN', '00100000000000010000011': 'ASSIGNABLE RIPE', '0010000000000010': '6TO4', '0011111111111110': '6BONE', '0011111111111111': 'RESERVED', '010': 'GLOBAL-UNICAST', '011': 'UNASSIGNED', '100': 'GEO-UNICAST', '101': 'UNASSIGNED', '110': 'UNASSIGNED', '1110': 'UNASSIGNED', '11110': 'UNASSIGNED', '111110': 'UNASSIGNED', '1111110': 'UNASSIGNED', '111111100': 'UNASSIGNED', '1111111010': 'LINKLOCAL', '1111111011': 'SITELOCAL', '11111111': 'MULTICAST', '0' * 96: 'IPV4COMP', '0' * 80 + '1' * 16: 'IPV4MAP', '0' * 128: 'UNSPECIFIED', '0' * 127 + '1': 'LOOPBACK'}

class IPint:
    """Handling of IP addresses returning integers.

    Use class IP instead because some features are not implemented for
    IPint."""
    __module__ = __name__

    def __init__(self, data, ipversion=0):
        """Create an instance of an IP object.
        
        Data can be a network specification or a single IP. IP
        Addresses can be specified in all forms understood by
        parseAddress.() the size of a network can be specified as

        /prefixlen        a.b.c.0/24               2001:658:22a:cafe::/64
        -lastIP           a.b.c.0-a.b.c.255        2001:658:22a:cafe::-2001:658:22a:cafe:ffff:ffff:ffff:ffff
        /decimal netmask  a.b.c.d/255.255.255.0    not supported for IPv6

        If no size specification is given a size of 1 address (/32 for
        IPv4 and /128 for IPv6) is assumed.

        >>> print IP('127.0.0.0/8')
        127.0.0.0/8
        >>> print IP('127.0.0.0/255.0.0.0')
        127.0.0.0/8
        >>> print IP('127.0.0.0-127.255.255.255')
        127.0.0.0/8

        See module documentation for more examples.
        """
        self.NoPrefixForSingleIp = 1
        self.WantPrefixLen = None
        netbits = 0
        prefixlen = -1
        if type(data) == types.IntType or type(data) == types.LongType:
            self.ip = long(data)
            if ipversion == 0:
                if self.ip < 4294967296:
                    ipversion = 4
                else:
                    ipversion = 6
            if ipversion == 4:
                prefixlen = 32
            elif ipversion == 6:
                prefixlen = 128
            else:
                raise ValueError, 'only IPv4 and IPv6 supported'
            self._ipversion = ipversion
            self._prefixlen = prefixlen
        else:
            x = data.split('-')
            if len(x) == 2:
                (ip, last) = x
                (self.ip, parsedVersion) = parseAddress(ip)
                if parsedVersion != 4:
                    raise ValueError, 'first-last notation only allowed for IPv4'
                (last, lastversion) = parseAddress(last)
                if lastversion != 4:
                    raise ValueError, 'last address should be IPv4, too'
                if last < self.ip:
                    raise ValueError, 'last address should be larger than first'
                size = last - self.ip
                netbits = _count1Bits(size)
            elif len(x) == 1:
                x = data.split('/')
                if len(x) == 1:
                    ip = x[0]
                    prefixlen = -1
                elif len(x) > 2:
                    raise ValueError, "only one '/' allowed in IP Address"
                else:
                    (ip, prefixlen) = x
                    if prefixlen.find('.') != -1:
                        (netmask, vers) = parseAddress(prefixlen)
                        if vers != 4:
                            raise ValueError, 'netmask must be IPv4'
                        prefixlen = _netmaskToPrefixlen(netmask)
            elif len(x) > 2:
                raise ValueError, "only one '-' allowed in IP Address"
            else:
                raise ValueError, "can't parse"
            (self.ip, parsedVersion) = parseAddress(ip)
            if ipversion == 0:
                ipversion = parsedVersion
            if prefixlen == -1:
                if ipversion == 4:
                    prefixlen = 32 - netbits
                elif ipversion == 6:
                    prefixlen = 128 - netbits
                else:
                    raise ValueError, 'only IPv4 and IPv6 supported'
            self._ipversion = ipversion
            self._prefixlen = int(prefixlen)
            if not _checkNetaddrWorksWithPrefixlen(self.ip, self._prefixlen, self._ipversion):
                raise ValueError, '%s goes not well with prefixlen %d' % (hex(self.ip), self._prefixlen)
        return

    def int(self):
        """Return the first / base / network addess as an (long) integer.

        The same as IP[0].

        >>> hex(IP('10.0.0.0/8').int())
        '0xA000000L'
        """
        return self.ip

    def version(self):
        """Return the IP version of this Object.

        >>> IP('10.0.0.0/8').version()
        4
        >>> IP('::1').version()
        6
        """
        return self._ipversion

    def prefixlen(self):
        """Returns Network Prefixlen.

        >>> IP('10.0.0.0/8').prefixlen()
        8
        """
        return self._prefixlen

    def net(self):
        """Return the base (first) address of a network as an (long) integer."""
        return self.int()

    def broadcast(self):
        """Return the broadcast (last) address of a network as an (long) integer.

        The same as IP[-1]."""
        return self.int() + self.len() - 1

    def _printPrefix(self, want):
        """Prints Prefixlen/Netmask.

        Not really. In fact it is our universal Netmask/Prefixlen printer.
        This is considered an internel function.

        want == 0 / None        don't return anything    1.2.3.0
        want == 1               /prefix                  1.2.3.0/24
        want == 2               /netmask                 1.2.3.0/255.255.255.0
        want == 3               -lastip                  1.2.3.0-1.2.3.255
        """
        if self._ipversion == 4 and self._prefixlen == 32 or self._ipversion == 6 and self._prefixlen == 128:
            if self.NoPrefixForSingleIp:
                want = 0
        if want == None:
            want = self.WantPrefixLen
            if want == None:
                want = 1
        if want:
            if want == 2:
                netmask = self.netmask()
                if type(netmask) != types.IntType and type(netmask) != types.LongType:
                    netmask = netmask.int()
                return '/%s' % intToIp(netmask, self._ipversion)
            elif want == 3:
                return '-%s' % intToIp(self.ip + self.len() - 1, self._ipversion)
            else:
                return '/%d' % self._prefixlen
        else:
            return ''
        return

    def strBin(self, wantprefixlen=None):
        """Return a string representation as a binary value.

        >>> print IP('127.0.0.1').strBin()
        01111111000000000000000000000001
        """
        if self._ipversion == 4:
            bits = 32
        elif self._ipversion == 6:
            bits = 128
        else:
            raise ValueError, 'only IPv4 and IPv6 supported'
        if self.WantPrefixLen == None and wantprefixlen == None:
            wantprefixlen = 0
        ret = _intToBin(self.ip)
        return '0' * (bits - len(ret)) + ret + self._printPrefix(wantprefixlen)

    def strCompressed(self, wantprefixlen=None):
        """Return a string representation in compressed format using '::' Notation.

        >>> print IP('127.0.0.1').strCompressed()
        127.0.0.1
        >>> print IP('2001:0658:022a:cafe:0200::1').strCompressed()
        2001:658:22a:cafe:200::1
        """
        if self.WantPrefixLen == None and wantprefixlen == None:
            wantprefixlen = 1
        if self._ipversion == 4:
            return self.strFullsize(wantprefixlen)
        else:
            hextets = [ int(x, 16) for x in self.strFullsize(0).split(':') ]
            followingzeros = [
             0] * 8
            for i in range(len(hextets)):
                followingzeros[i] = _countFollowingZeros(hextets[i:])

            compressionpos = followingzeros.index(max(followingzeros))
            if max(followingzeros) > 1:
                hextets = [ x for x in self.strNormal(0).split(':') ]
                while compressionpos < len(hextets) and hextets[compressionpos] == '0':
                    del hextets[compressionpos]

                hextets.insert(compressionpos, '')
                if compressionpos + 1 >= len(hextets):
                    hextets.append('')
                if compressionpos == 0:
                    hextets = [
                     ''] + hextets
                return (':').join(hextets) + self._printPrefix(wantprefixlen)
            else:
                return self.strNormal() + self._printPrefix(wantprefixlen)
        return

    def strNormal(self, wantprefixlen=None):
        """Return a string representation in the usual format.

        >>> print IP('127.0.0.1').strNormal()
        127.0.0.1
        >>> print IP('2001:0658:022a:cafe:0200::1').strNormal()
        2001:658:22a:cafe:200:0:0:1
        """
        if self.WantPrefixLen == None and wantprefixlen == None:
            wantprefixlen = 1
        if self._ipversion == 4:
            ret = self.strFullsize(0)
        elif self._ipversion == 6:
            ret = (':').join([ hex(x)[2:] for x in [ int(x, 16) for x in self.strFullsize(0).split(':') ] ])
        else:
            raise ValueError, 'only IPv4 and IPv6 supported'
        return ret + self._printPrefix(wantprefixlen)

    def strFullsize(self, wantprefixlen=None):
        """Return a string representation in the non mangled format.

        >>> print IP('127.0.0.1').strFullsize()
        127.0.0.1
        >>> print IP('2001:0658:022a:cafe:0200::1').strFullsize()
        2001:0658:022a:cafe:0200:0000:0000:0001
        """
        if self.WantPrefixLen == None and wantprefixlen == None:
            wantprefixlen = 1
        return intToIp(self.ip, self._ipversion).lower() + self._printPrefix(wantprefixlen)

    def strHex(self, wantprefixlen=None):
        """Return a string representation in hex format.

        >>> print IP('127.0.0.1').strHex()
        0x7F000001
        >>> print IP('2001:0658:022a:cafe:0200::1').strHex()
        0x20010658022ACAFE0200000000000001
        """
        if self.WantPrefixLen == None and wantprefixlen == None:
            wantprefixlen = 0
        x = hex(self.ip)
        if x[(-1)] == 'L':
            x = x[:-1]
        return x + self._printPrefix(wantprefixlen)

    def strDec(self, wantprefixlen=None):
        """Return a string representation in decimal format.

        >>> print IP('127.0.0.1').strDec()
        2130706433
        >>> print IP('2001:0658:022a:cafe:0200::1').strDec()
        42540616829182469433547762482097946625
        """
        if self.WantPrefixLen == None and wantprefixlen == None:
            wantprefixlen = 0
        x = str(self.ip)
        if x[(-1)] == 'L':
            x = x[:-1]
        return x + self._printPrefix(wantprefixlen)

    def iptype(self):
        """Return a description of the IP type ('PRIVATE', 'RESERVERD', etc).

        >>> print IP('127.0.0.1').iptype()
        PRIVATE
        >>> print IP('192.168.1.1').iptype()
        PRIVATE
        >>> print IP('195.185.1.2').iptype()
        PUBLIC
        >>> print IP('::1').iptype()
        LOOPBACK
        >>> print IP('2001:0658:022a:cafe:0200::1').iptype()
        ASSIGNABLE RIPE

        The type information for IPv6 is out of sync with reality.
        """
        if self._ipversion == 4:
            iprange = IPv4ranges
        elif self._ipversion == 6:
            iprange = IPv6ranges
        else:
            raise ValueError, 'only IPv4 and IPv6 supported'
        bits = self.strBin()
        for i in range(len(bits), 0, -1):
            if iprange.has_key(bits[:i]):
                return iprange[bits[:i]]

        return 'unknown'

    def netmask(self):
        """Return netmask as an integer.

        >>> print hex(IP('195.185.0.0/16').netmask().int())
        0xFFFF0000L
        """
        if self._ipversion == 4:
            locallen = 32 - self._prefixlen
        elif self._ipversion == 6:
            locallen = 128 - self._prefixlen
        else:
            raise ValueError, 'only IPv4 and IPv6 supported'
        return 2 ** self._prefixlen - 1 << locallen

    def strNetmask(self):
        """Return netmask as an string. Mostly useful for IPv6.

        >>> print IP('195.185.0.0/16').strNetmask()
        255.255.0.0
        >>> print IP('2001:0658:022a:cafe::0/64').strNetmask()
        /64
        """
        if self._ipversion == 4:
            locallen = 32 - self._prefixlen
            return intToIp(2 ** self._prefixlen - 1 << locallen, 4)
        elif self._ipversion == 6:
            locallen = 128 - self._prefixlen
            return '/%d' % self._prefixlen
        else:
            raise ValueError, 'only IPv4 and IPv6 supported'

    def len(self):
        """Return the length of an subnet.

        >>> print IP('195.185.1.0/28').len()
        16
        >>> print IP('195.185.1.0/24').len()
        256
        """
        if self._ipversion == 4:
            locallen = 32 - self._prefixlen
        elif self._ipversion == 6:
            locallen = 128 - self._prefixlen
        else:
            raise ValueError, 'only IPv4 and IPv6 supported'
        return 2 ** locallen

    def __len__(self):
        """Return the length of an subnet.

        Called to implement the built-in function len().
        It breaks with IPv6 Networks. Anybody knows how to fix this."""
        return int(self.len())

    def __getitem__(self, key):
        """Called to implement evaluation of self[key].
        
        >>> ip=IP('127.0.0.0/30')
        >>> for x in ip:
        ...  print hex(x.int())
        ...
        0x7F000000L
        0x7F000001L
        0x7F000002L
        0x7F000003L
        >>> hex(ip[2].int())
        '0x7F000002L'
        >>> hex(ip[-1].int())
        '0x7F000003L'
        """
        if type(key) != types.IntType and type(key) != types.LongType:
            raise TypeError
        if abs(key) >= self.len():
            raise IndexError
        if key < 0:
            key = self.len() - abs(key)
        return self.ip + long(key)

    def __contains__(self, item):
        """Called to implement membership test operators.

        Should return true if item is in self, false otherwise. Item
        can be other IP-objects, strings or ints.

        >>> print IP('195.185.1.1').strHex()
        0xC3B90101
        >>> 0xC3B90101L in IP('195.185.1.0/24')
        1
        >>> '127.0.0.1' in IP('127.0.0.0/24')
        1
        >>> IP('127.0.0.0/24') in IP('127.0.0.0/25')
        0
        """
        if type(item) == types.StringType:
            item = IP(item)
        if isinstance(item, IP) or isinstance(item, IPint):
            if item.len() == 0:
                item = item.int()
            elif item.ip >= self.ip and item.ip < self.ip + self.len() - item.len() + 1:
                return 1
            else:
                return 0
        if type(item) == types.IntType:
            item = long(item)
        if type(item) == types.LongType:
            if item >= self.ip and item < self.ip + self.len():
                return 1
            else:
                return 0
        raise TypeError, 'Only integers, IP-objects and strings can be tested.'

    def __str__(self):
        """Dispatch to the prefered String Representation.

        Used to implement str(IP)."""
        return self.strFullsize()

    def __repr__(self):
        """Print a representation of the Object.

        Used to implement repr(IP). Returns a string which evaluates
        to an identical Object (without the wnatprefixlen stuff - see
        module docstring.

        >>> print repr(IP('10.0.0.0/24'))
        IP('10.0.0.0/24')
        """
        return "IPint('%s')" % self.strCompressed(1)

    def __cmp__(self, other):
        """Called by comparison operations.

        Should return a negative integer if self < other, zero if self
        == other, a positive integer if self > other.

        Networks with different prefixlen are considered non-equal.
        Networks with the same prefixlen and differing addresses are
        considered non equal but are compared by thair base address
        integer value to aid sorting of IP objects.

        The Version of Objects is not put into consideration.

        >>> IP('10.0.0.0/24') > IP('10.0.0.0')
        1
        >>> IP('10.0.0.0/24') < IP('10.0.0.0')
        0
        >>> IP('10.0.0.0/24') < IP('12.0.0.0/24')
        1
        >>> IP('10.0.0.0/24') > IP('12.0.0.0/24')
        0

        TODO: There is a bizarre effect with sorting which I still
        have to look into:

        >>> l = [IP('10.0.0.0/24'), IP('10.0.0.0/16'),IP('10.0.0.0/25'), IP('12.0.0.0/24'), IP('2.0.0.0/24'), IP('127.0.0.1')]
        >>> l.sort()
        >>> print l
        [IP('10.0.0.0/24'), IP('10.0.0.0/16'), IP('10.0.0.0/25'), IP('2.0.0.0/24'), IP('12.0.0.0/24'), IP('127.0.0.1')]
        >>> l = [IP('10.0.0.0/24'), IP('12.0.0.0/24'), IP('2.0.0.0/24'), IP('127.0.0.1')]
        >>> print l
        [IP('10.0.0.0/24'), IP('12.0.0.0/24'), IP('2.0.0.0/24'), IP('127.0.0.1')]
        >>> l.sort()
        >>> print l
        [IP('2.0.0.0/24'), IP('10.0.0.0/24'), IP('12.0.0.0/24'), IP('127.0.0.1')]

        """
        if self._prefixlen < other.prefixlen():
            return other.prefixlen() - self._prefixlen
        elif self._prefixlen > other.prefixlen():
            return self._prefixlen - other.prefixlen() * -1
        elif self.ip < other.ip:
            return -1
        elif self.ip > other.ip:
            return 1
        else:
            return 0

    def __hash__(self):
        """Called for the key object for dictionary operations, and by
        the built-in function hash() Should return a 32-bit integer
        usable as a hash value for dictionary operations. The only
        required property is that objects which compare equal have the
        same hash value

        >>> hex(IP('10.0.0.0/24').__hash__())
        '-0xa000019'
        """
        hash = int(-1)
        ip = self.ip
        while ip > 0:
            hash = hash ^ ip & 2147483647
            ip = ip >> 32

        hash = hash ^ self._prefixlen
        return int(hash)


class IP(IPint):
    """Class for handling IP Addresses and Networks."""
    __module__ = __name__

    def net(self):
        """Return the base (first) address of a network as an IP object.

        The same as IP[0].

        >>> IP('10.0.0.0/8').net()
        IP('10.0.0.0')
        """
        return IP(IPint.net(self))

    def broadcast(self):
        """Return the broadcast (last) address of a network as an IP object.

        The same as IP[-1].

        >>> IP('10.0.0.0/8').broadcast()
        IP('10.255.255.255')
        """
        return IP(IPint.broadcast(self))

    def netmask(self):
        """Return netmask as an IP object.

        >>> IP('10.0.0.0/8').netmask()
        IP('255.0.0.0')
         """
        return IP(IPint.netmask(self))

    def reverseNames(self):
        """Return a list with values forming the reverse lookup.

        >>> IP('213.221.113.87/32').reverseNames()
        ['87.113.221.213.in-addr.arpa.']
        >>> IP('213.221.112.224/30').reverseNames()
        ['224.112.221.213.in-addr.arpa.', '225.112.221.213.in-addr.arpa.', '226.112.221.213.in-addr.arpa.', '227.112.221.213.in-addr.arpa.']
        >>> IP('127.0.0.0/24').reverseNames()
        ['0.0.127.in-addr.arpa.']
        >>> IP('127.0.0.0/23').reverseNames()
        ['0.0.127.in-addr.arpa.', '1.0.127.in-addr.arpa.']
        >>> IP('127.0.0.0/16').reverseNames()
        ['0.127.in-addr.arpa.']
        >>> IP('127.0.0.0/15').reverseNames()
        ['0.127.in-addr.arpa.', '1.127.in-addr.arpa.']
        >>> IP('128.0.0.0/8').reverseNames()
        ['128.in-addr.arpa.']
        >>> IP('128.0.0.0/7').reverseNames()
        ['128.in-addr.arpa.', '129.in-addr.arpa.']
        
        """
        if self._ipversion == 4:
            ret = []
            if self.len() < 2 ** 8:
                for x in self:
                    ret.append(x.reverseName())

            else:
                if self.len() < 2 ** 16:
                    for i in range(0, self.len(), 2 ** 8):
                        ret.append(self[i].reverseName()[2:])

                if self.len() < 2 ** 24:
                    for i in range(0, self.len(), 2 ** 16):
                        ret.append(self[i].reverseName()[4:])

                for i in range(0, self.len(), 2 ** 24):
                    ret.append(self[i].reverseName()[6:])

            return ret
        elif self._ipversion == 6:
            s = hex(self.ip)[2:].lower()
            if s[(-1)] == 'l':
                s = s[:-1]
            if self._prefixlen % 4 != 0:
                raise NotImplementedError, "can't create IPv6 reverse names at sub nibble level"
            s = list(s)
            s.reverse()
            s = ('.').join(s)
            first_nibble_index = int(32 - self._prefixlen / 4) * 2
            return ['%s.ip6.int.' % s[first_nibble_index:]]
        else:
            raise ValueError, 'only IPv4 and IPv6 supported'

    def reverseName(self):
        """Return the value for reverse lookup/PTR records as RfC 2317 look alike.

        RfC 2317 is an ugly hack which only works for sub-/24 e.g. not
        for /23. Do not use it. Better set up a Zone for every
        address. See reverseName for a way to arcive that.

        >>> print IP('195.185.1.1').reverseName()
        1.1.185.195.in-addr.arpa.
        >>> print IP('195.185.1.0/28').reverseName()
        0-15.1.185.195.in-addr.arpa.
        """
        if self._ipversion == 4:
            s = self.strFullsize(0)
            s = s.split('.')
            s.reverse()
            first_byte_index = int(4 - self._prefixlen / 8)
            if self._prefixlen % 8 != 0:
                nibblepart = '%s-%s' % (s[(3 - self._prefixlen / 8)], intToIp(self.ip + self.len() - 1, 4).split('.')[(-1)])
                if nibblepart[(-1)] == 'l':
                    nibblepart = nibblepart[:-1]
                nibblepart += '.'
            else:
                nibblepart = ''
            s = ('.').join(s[first_byte_index:])
            return '%s%s.in-addr.arpa.' % (nibblepart, s)
        elif self._ipversion == 6:
            s = hex(self.ip)[2:].lower()
            if s[(-1)] == 'l':
                s = s[:-1]
            if self._prefixlen % 4 != 0:
                nibblepart = '%s-%s' % (s[self._prefixlen:], hex(self.ip + self.len() - 1)[2:].lower())
                if nibblepart[(-1)] == 'l':
                    nibblepart = nibblepart[:-1]
                nibblepart += '.'
            else:
                nibblepart = ''
            s = list(s)
            s.reverse()
            s = ('.').join(s)
            first_nibble_index = int(32 - self._prefixlen / 4) * 2
            return '%s%s.ip6.int.' % (nibblepart, s[first_nibble_index:])
        else:
            raise ValueError, 'only IPv4 and IPv6 supported'

    def __getitem__(self, key):
        """Called to implement evaluation of self[key].
        
        >>> ip=IP('127.0.0.0/30')
        >>> for x in ip:
        ...  print str(x)
        ...
        127.0.0.0
        127.0.0.1
        127.0.0.2
        127.0.0.3
        >>> print str(ip[2])
        127.0.0.2
        >>> print str(ip[-1])
        127.0.0.3
        """
        return IP(IPint.__getitem__(self, key))

    def __repr__(self):
        """Print a representation of the Object.

        >>> IP('10.0.0.0/8')
        IP('10.0.0.0/8')
        """
        return "IP('%s')" % self.strCompressed(1)

    def __add__(self, other):
        """Emulate numeric objects through network aggregation"""
        if self.prefixlen() != other.prefixlen():
            raise ValueError, 'Only networks with the same prefixlen can be added.'
        if self.prefixlen < 1:
            raise ValueError, "Networks with a prefixlen longer than /1 can't be added."
        if self.version() != other.version():
            raise ValueError, 'Only networks with teh same IP version can be added.'
        if self > other:
            other.__add__(self)
        else:
            ret = IP(self.int())
            ret._prefixlen = self.prefixlen() - 1
            return ret


def _countFollowingZeros(l):
    """Return Nr. of elements containing 0 at the beginning th the list."""
    if len(l) == 0:
        return 0
    elif l[0] != 0:
        return 0
    else:
        return 1 + _countFollowingZeros(l[1:])


_BitTable = {'0': '0000', '1': '0001', '2': '0010', '3': '0011', '4': '0100', '5': '0101', '6': '0110', '7': '0111', '8': '1000', '9': '1001', 'a': '1010', 'b': '1011', 'c': '1100', 'd': '1101', 'e': '1110', 'f': '1111'}

def _intToBin(val):
    """Return the binary representation of an integer as string."""
    if val < 0:
        raise ValueError, 'Only positive Values allowed'
    s = hex(val).lower()
    ret = ''
    if s[(-1)] == 'l':
        s = s[:-1]
    for x in s[2:]:
        if __debug__:
            if not _BitTable.has_key(x):
                raise AssertionError, 'hex() returned strange result'
        ret += _BitTable[x]

    while ret[0] == '0' and len(ret) > 1:
        ret = ret[1:]

    return ret


def parseAddress(ipstr):
    """Parse a string and return the corrospondending IPaddress and the a guess of the IP version.

    Following Forms ar recorgnized:
    0x0123456789abcdef           # IPv4 if <= 0xffffffff else IPv6
    123.123.123.123              # IPv4
    123.123                      # 0-padded IPv4
    1080:0000:0000:0000:0008:0800:200C:417A
    1080:0:0:0:8:800:200C:417A
    1080:0::8:800:200C:417A
    ::1
    ::
    0:0:0:0:0:FFFF:129.144.52.38
    ::13.1.68.3
    ::FFFF:129.144.52.38
    """
    if ipstr.startswith('0x'):
        ret = long(ipstr[2:], 16)
        if ret > 340282366920938463463374607431768211455:
            raise ValueError, "%r: IP Address can't be bigger than 2^128" % ipstr
        if ret < 4294967296:
            return (
             ret, 4)
        else:
            return (
             ret, 6)
    if ipstr.find(':') != -1:
        if ipstr.find(':::') != -1:
            raise ValueError, "%r: IPv6 Address can't contain ':::'" % ipstr
        hextets = ipstr.split(':')
        if ipstr.find('.') != -1:
            (v4, foo) = parseAddress(hextets[(-1)])
            assert foo == 4
            del hextets[-1]
            hextets.append(hex(v4 >> 16)[2:-1])
            hextets.append(hex(v4 & 65535)[2:-1])
        if len(hextets) > 8:
            raise ValueError, '%r: IPv6 Address with more than 8 hexletts' % ipstr
        if len(hextets) < 8:
            if '' not in hextets:
                raise ValueError, "%r IPv6 Address with less than 8 hexletts and without '::'" % ipstr
            if hextets.index('') < len(hextets) - 1 and hextets[(hextets.index('') + 1)] == '':
                hextets.remove('')
            if hextets.index('') < len(hextets) - 1 and hextets[(hextets.index('') + 1)] == '':
                hextets.remove('')
            for i in range(9 - len(hextets)):
                hextets.insert(hextets.index(''), '0')

            hextets.remove('')
            if '' in hextets:
                raise ValueError, "%r IPv6 Address may contain '::' only once" % ipstr
        if '' in hextets:
            raise ValueError, "%r IPv6 Address may contain '::' only if it has less than 8 hextets" % ipstr
        num = ''
        for x in hextets:
            if len(x) < 4:
                x = (4 - len(x)) * '0' + x
            if int(x, 16) < 0 or int(x, 16) > 65535:
                raise ValueError, "%r: single hextet must be 0 <= hextet <= 0xffff which isn't true for %s" % (ipstr, x)
            num += x

        return (
         long(num, 16), 6)
    elif len(ipstr) == 32:
        return (long(ipstr, 16), 6)
    elif ipstr.find('.') != -1 or len(ipstr) < 4 and int(ipstr) < 256:
        bytes = ipstr.split('.')
        if len(bytes) > 4:
            raise ValueError, 'IPv4 Address with more than 4 bytes'
        bytes += ['0'] * (4 - len(bytes))
        bytes = [ long(x) for x in bytes ]
        for x in bytes:
            if x > 255 or x < 0:
                raise ValueError, '%r: single byte must be 0 <= byte < 256' % ipstr

        return (
         (bytes[0] << 24) + (bytes[1] << 16) + (bytes[2] << 8) + bytes[3], 4)
    else:
        ret = long(ipstr)
        if ret > 340282366920938463463374607431768211455:
            raise ValueError, 'IP Address cant be bigger than 2^128'
        if ret <= 4294967295:
            return (
             ret, 4)
        else:
            return (
             ret, 6)


def intToIp(ip, version):
    """Transform an integer string into an IP address."""
    ip = long(ip)
    if ip < 0:
        raise ValueError, "IPs can't be negative: %d" % ip
    ret = ''
    if version == 4:
        if ip > 4294967295:
            raise ValueError, "IPv4 Addresses can't be larger than 0xffffffff: %s" % hex(ip)
        for l in range(4):
            ret = str(ip & 255) + '.' + ret
            ip = ip >> 8

        ret = ret[:-1]
    elif version == 6:
        if ip > 340282366920938463463374607431768211455:
            raise ValueError, "IPv6 Addresses can't be larger than 0xffffffffffffffffffffffffffffffff: %s" % hex(ip)
        l = '0' * 32 + hex(ip)[2:-1]
        for x in range(1, 33):
            ret = l[(-x)] + ret
            if x % 4 == 0:
                ret = ':' + ret

        ret = ret[1:]
    else:
        raise ValueError, 'only IPv4 and IPv6 supported'
    return ret


def _count1Bits(num):
    """Find the highest bit set to 1 in an integer."""
    ret = 0
    while num > 0:
        num = num >> 1
        ret += 1

    return ret


def _count0Bits(num):
    """Find the highest bit set to 0 in an integer."""
    num = long(num)
    if num < 0:
        raise ValueError, 'Only positive Numbers please: %s' % num
    ret = 0
    while num > 0:
        if num & 1 == 1:
            break
        num = num >> 1
        ret += 1

    return ret


def _checkPrefix(ip, prefixlen, version):
    """Check the validity of a prefix
    
    Checks if the variant part of a prefix only has 0s, and the length is
    correct.

    >>> _checkPrefix(0x7f000000L, 24, 4)
    1
    >>> _checkPrefix(0x7f000001L, 24, 4)
    0
    >>> repr(_checkPrefix(0x7f000001L, -1, 4))
    'None'
    >>> repr(_checkPrefix(0x7f000001L, 33, 4))
    'None'
    """
    if version == 4:
        bits = 32
    elif version == 6:
        bits = 128
    else:
        raise ValueError, 'only IPv4 and IPv6 supported'
    if prefixlen < 0 or prefixlen > bits:
        return
    if ip == 0:
        zbits = bits + 1
    else:
        zbits = _count0Bits(ip)
    if zbits < bits - prefixlen:
        return 0
    else:
        return 1
    return


def _checkNetmask(netmask, masklen):
    """Checks if a netmask is expressable as e prefixlen."""
    num = long(netmask)
    bits = masklen
    while num & 1 == 0:
        num = num >> 1
        bits -= 1
        if bits == 0:
            break

    while bits > 0:
        if num & 1 == 0:
            raise ValueError, "Netmask %s can't be expressed as an prefix." % hex(netmask)
        num = num >> 1
        bits -= 1


def _checkNetaddrWorksWithPrefixlen(net, prefixlen, version):
    """Check if a base addess of e network is compatible with a prefixlen"""
    if net & _prefixlenToNetmask(prefixlen, version) == net:
        return 1
    else:
        return 0


def _netmaskToPrefixlen(netmask):
    """Convert an Integer reprsenting a Netmask to an prefixlen.

    E.g. 0xffffff00 (255.255.255.0) returns 24
    """
    netlen = _count0Bits(netmask)
    masklen = _count1Bits(netmask)
    _checkNetmask(netmask, masklen)
    return masklen - netlen


def _prefixlenToNetmask(prefixlen, version):
    """Return a mask of n bits as a long integer.

    From 'IP address conversion functions with the builtin socket module' by Alex Martelli
    http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66517
    """
    if prefixlen == 0:
        return 0
    elif prefixlen < 0:
        raise ValueError, 'Prefixlen must be > 0'
    if version == 4:
        return (2 << prefixlen - 1) - 1 << 32 - prefixlen
    elif version == 6:
        return (2 << prefixlen - 1) - 1 << 128 - prefixlen
    else:
        raise ValueError, 'only IPv4 and IPv6 supported'


def _test():
    import doctest, IPy
    return doctest.testmod(IPy)


if __name__ == '__main__':
    _test()
    t = [
     240, 3840, 65280, 16776960, 4294967040]
    o = []
    for x in t:
        pass

    x = 0
from salamoia.tests import *
runDocTests()