# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3\plugins\netblocker\netblock\netblock.py
# Compiled at: 2016-03-08 18:42:10
from b3.plugins.netblocker.netblock import ranges
__doc__ = "This module implements sets of IP address ranges,\nsupporting various notation for them and various routines for\ndealing with them. The primary data structure is IPRanges, the\nactual IP address ranges.\n\nRanges can generally be specified as IP addresses, in CIDR notation,\nor as ranges written 'LOWIP-HIGHIP'."

class NBError(Exception):
    """Raised for all netblock errors."""
    pass


class BadCIDRError(NBError):
    """Raised for a badly formed CIDR; subclass of NBError."""
    pass


B32M = 4294967295

def m32(n):
    """Mask a number to 32 bits."""
    return n & B32M


def lenmask(len):
    """Return the mask for a given network length."""
    return m32(-(1 << 32 - len))


def cidrrange(addr, length):
    """Given an IP address and a network size, return the low and
        high addresses in it."""
    m = lenmask(length)
    l = addr & m
    h = l + m32(-1 ^ m)
    return (
     l, h)


def strtoip(ipstr, min=4):
    """Convert an IP address in string form to numeric form (an unsigned
        32-bit integer in host byte order). min is the number of octets that
        the IP address string must have."""
    res = 0
    n = ipstr.split('.')
    ln = len(n)
    if ln > 4 or ln < min:
        raise NBError('Invalid number of IP octets')
    for i in n:
        res = res << 8
        try:
            ot = int(i)
        except ValueError:
            raise NBError('invalid IP octet')

        if ot < 0 or ot > 255:
            raise NBError('invalid IP octet')
        res = res + ot

    res = res << 8 * (4 - ln)
    return res


def convip(s):
    """Returns the start and end range of a single IP address, ie
        (ipnum,ipnum)."""
    res = strtoip(s)
    return (res, res)


def convcidr(cstr, strict=1):
    """Returns the start and end IPs of a CIDR from a string. strict
        is whether the CIDR must be a proper one."""
    pos = cstr.find('/')
    ip = strtoip(cstr[:pos], min=1)
    try:
        size = int(cstr[pos + 1:])
    except ValueError:
        raise NBError('invalid CIDR size')

    if size < 0 or size > 32:
        raise NBError('CIDR size not in 0 to 32')
    res = cidrrange(ip, size)
    if strict and res[0] != ip:
        raise BadCIDRError('CIDR start IP is not properly aligned: ' + cstr)
    return res


def convrange(s):
    """Returns the start and end IPs from a string range."""
    pos = s.find('-')
    low = strtoip(s[:pos])
    high = strtoip(s[pos + 1:])
    if low > high:
        raise NBError('IP range has start larger than end.')
    return (
     low, high)


def convtcpwr(s):
    """Returns the start and end IPs from a tcpwrapper style prefix.
        We mostly assume that it is validly formatted."""
    dots = s.count('.')
    if not 1 <= dots <= 3:
        raise NBError('invalid number of dots in tcpwrapper prefix')
    cidr = '%s/%d' % (s[:-1], 8 * dots)
    return convcidr(cidr, 0)


def convert(s, strict=1):
    """Return a (low,high) IP number tuple for s, regardless of
        whether s is a CIDR, an IP address, or a range. strict is
        whether the CIDR is allowed to be an odd CIDR."""
    if s[(-1)] == '.':
        return convtcpwr(s)
    else:
        if '/' in s:
            return convcidr(s, strict)
        if '-' in s:
            return convrange(s)
        return convip(s)


def octet(ip, n):
    """get octet n (0-3) of ip address ip. 0 is the first (left) octet."""
    s = (3 - n) * 8
    return ip >> s & 255


def ipstr(ip):
    """Convert an IP address in numberic form to string form."""
    o1, o2, o3, o4 = (
     octet(ip, 0), octet(ip, 1), octet(ip, 2), octet(ip, 3))
    return '%d.%d.%d.%d' % (o1, o2, o3, o4)


def cidrtostr(ip, len):
    """Convert an IP number and a length to CIDR string, or to a simple
        IP address string if len is 32."""
    if len == 32:
        return ipstr(ip)
    else:
        return '%s/%d' % (ipstr(ip), len)


def fmaxlen(ip):
    for i in range(0, 33):
        if ip & 1 << i:
            return 32 - i

    return 0


def lhcidrs(lip, hip, lst):
    """Convert a range from lowip to highip to a list of CIDR
        address/length values that are appended to lst."""
    while lip <= hip:
        lb = fmaxlen(lip)
        while lb <= 32:
            lt, ht = cidrrange(lip, lb)
            if lt == lip and ht <= hip:
                break
            lb = lb + 1

        assert 0 <= lb <= 32 and lt == lip and ht <= hip, 'failed to generate a valid, fitting CIDR'
        lst.append((lip, lb))
        lip = ht + 1


class IPRanges(ranges.Ranges):
    """Sets of IP address ranges (or single IPs, or both).

        All IP address arguments are supplied as strings, including for
        'in'. Iterating an IPRanges object yields each IP address that
        is included in the set of address ranges. The length of an IPRanges
        object is how many IP addresses it contains.
        
        The general interfaces accept four forms of addresses or
        address ranges: single IP address, CIDRs, LOWIP-HIGHIP ranges,
        or tcpwrappers style prefixes (eg '127.10.'). CIDRs must
        normally be 'proper', where the IP address is the low end of
        the proper CIDR. CIDRs may be specified in short form, eg
        127/8.

        This is built on top of ranges.Ranges; see there for more things."""

    def __init__(self, ival=None):
        """Optional ival is the initial IP address (range); it is
                passed to .add()."""
        ranges.Ranges.__init__(self)
        if ival:
            self.add(ival)

    def _rel(self, val):
        return ipstr(val)

    def __str__(self):
        return '<IPRanges: %s>' % ((' ').join(map(self._rrange, self._l)),)

    def add(self, val):
        """Add any form of IP address that we accept to this set
                of IP address ranges."""
        low, high = convert(val)
        self.addrange(low, high)

    def addoddcidr(self, val):
        """Add an improper 'odd' CIDR (one with an IP address that
                is not its lower boundary) to this set of IP address ranges."""
        low, high = convert(val, 0)
        self.addrange(low, high)

    def remove(self, val):
        """Remove any form of IP address that we accept from this
                set of IP address ranges."""
        low, high = convert(val)
        self.delrange(low, high)

    def removeoddcidr(self, val):
        """Remove an odd CIDR from this set of IP address ranges."""
        low, high = convert(val, 0)
        self.delrange(low, high)

    def __contains__(self, val):
        """Our argument (the first argument to 'in') is taken as
                a string, not an IPRanges object. Use .subset() if you want
                to know if one IPRanges is a subset of another."""
        if isinstance(val, (int, long, float)):
            return ranges.Ranges.__contains__(self, val)
        else:
            return ranges.Ranges.__contains__(self, strtoip(val))

    def tocidr(self):
        """Return a list of CIDR netblocks (as strings) that represent
                this set of IP address ranges."""
        r = []
        for irng in self._l:
            lhcidrs(irng[0], irng[1], r)

        return [ cidrtostr(x[0], x[1]) for x in r ]