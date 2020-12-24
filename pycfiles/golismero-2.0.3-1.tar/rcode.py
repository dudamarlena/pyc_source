# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/thirdparty_libs/dns/rcode.py
# Compiled at: 2013-08-26 10:52:44
"""DNS Result Codes."""
import dns.exception
NOERROR = 0
FORMERR = 1
SERVFAIL = 2
NXDOMAIN = 3
NOTIMP = 4
REFUSED = 5
YXDOMAIN = 6
YXRRSET = 7
NXRRSET = 8
NOTAUTH = 9
NOTZONE = 10
BADVERS = 16
_by_text = {'NOERROR': NOERROR, 
   'FORMERR': FORMERR, 
   'SERVFAIL': SERVFAIL, 
   'NXDOMAIN': NXDOMAIN, 
   'NOTIMP': NOTIMP, 
   'REFUSED': REFUSED, 
   'YXDOMAIN': YXDOMAIN, 
   'YXRRSET': YXRRSET, 
   'NXRRSET': NXRRSET, 
   'NOTAUTH': NOTAUTH, 
   'NOTZONE': NOTZONE, 
   'BADVERS': BADVERS}
_by_value = dict([ (y, x) for x, y in _by_text.iteritems() ])

class UnknownRcode(dns.exception.DNSException):
    """Raised if an rcode is unknown."""
    pass


def from_text(text):
    """Convert text into an rcode.

    @param text: the texual rcode
    @type text: string
    @raises UnknownRcode: the rcode is unknown
    @rtype: int
    """
    if text.isdigit():
        v = int(text)
        if v >= 0 and v <= 4095:
            return v
    v = _by_text.get(text.upper())
    if v is None:
        raise UnknownRcode
    return v


def from_flags(flags, ednsflags):
    """Return the rcode value encoded by flags and ednsflags.

    @param flags: the DNS flags
    @type flags: int
    @param ednsflags: the EDNS flags
    @type ednsflags: int
    @raises ValueError: rcode is < 0 or > 4095
    @rtype: int
    """
    value = flags & 15 | ednsflags >> 20 & 4080
    if value < 0 or value > 4095:
        raise ValueError('rcode must be >= 0 and <= 4095')
    return value


def to_flags(value):
    """Return a (flags, ednsflags) tuple which encodes the rcode.

    @param value: the rcode
    @type value: int
    @raises ValueError: rcode is < 0 or > 4095
    @rtype: (int, int) tuple
    """
    if value < 0 or value > 4095:
        raise ValueError('rcode must be >= 0 and <= 4095')
    v = value & 15
    ev = long(value & 4080) << 20
    return (v, ev)


def to_text(value):
    """Convert rcode into text.

    @param value: the rcode
    @type value: int
    @rtype: string
    """
    text = _by_value.get(value)
    if text is None:
        text = str(value)
    return text