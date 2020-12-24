# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/thirdparty_libs/dns/rdatatype.py
# Compiled at: 2013-08-26 10:52:44
"""DNS Rdata Types.

@var _by_text: The rdata type textual name to value mapping
@type _by_text: dict
@var _by_value: The rdata type value to textual name mapping
@type _by_value: dict
@var _metatypes: If an rdatatype is a metatype, there will be a mapping
whose key is the rdatatype value and whose value is True in this dictionary.
@type _metatypes: dict
@var _singletons: If an rdatatype is a singleton, there will be a mapping
whose key is the rdatatype value and whose value is True in this dictionary.
@type _singletons: dict"""
import re, dns.exception
NONE = 0
A = 1
NS = 2
MD = 3
MF = 4
CNAME = 5
SOA = 6
MB = 7
MG = 8
MR = 9
NULL = 10
WKS = 11
PTR = 12
HINFO = 13
MINFO = 14
MX = 15
TXT = 16
RP = 17
AFSDB = 18
X25 = 19
ISDN = 20
RT = 21
NSAP = 22
NSAP_PTR = 23
SIG = 24
KEY = 25
PX = 26
GPOS = 27
AAAA = 28
LOC = 29
NXT = 30
SRV = 33
NAPTR = 35
KX = 36
CERT = 37
A6 = 38
DNAME = 39
OPT = 41
APL = 42
DS = 43
SSHFP = 44
IPSECKEY = 45
RRSIG = 46
NSEC = 47
DNSKEY = 48
DHCID = 49
NSEC3 = 50
NSEC3PARAM = 51
TLSA = 52
HIP = 55
SPF = 99
UNSPEC = 103
TKEY = 249
TSIG = 250
IXFR = 251
AXFR = 252
MAILB = 253
MAILA = 254
ANY = 255
TA = 32768
DLV = 32769
_by_text = {'NONE': NONE, 
   'A': A, 
   'NS': NS, 
   'MD': MD, 
   'MF': MF, 
   'CNAME': CNAME, 
   'SOA': SOA, 
   'MB': MB, 
   'MG': MG, 
   'MR': MR, 
   'NULL': NULL, 
   'WKS': WKS, 
   'PTR': PTR, 
   'HINFO': HINFO, 
   'MINFO': MINFO, 
   'MX': MX, 
   'TXT': TXT, 
   'RP': RP, 
   'AFSDB': AFSDB, 
   'X25': X25, 
   'ISDN': ISDN, 
   'RT': RT, 
   'NSAP': NSAP, 
   'NSAP-PTR': NSAP_PTR, 
   'SIG': SIG, 
   'KEY': KEY, 
   'PX': PX, 
   'GPOS': GPOS, 
   'AAAA': AAAA, 
   'LOC': LOC, 
   'NXT': NXT, 
   'SRV': SRV, 
   'NAPTR': NAPTR, 
   'KX': KX, 
   'CERT': CERT, 
   'A6': A6, 
   'DNAME': DNAME, 
   'OPT': OPT, 
   'APL': APL, 
   'DS': DS, 
   'SSHFP': SSHFP, 
   'IPSECKEY': IPSECKEY, 
   'RRSIG': RRSIG, 
   'NSEC': NSEC, 
   'DNSKEY': DNSKEY, 
   'DHCID': DHCID, 
   'NSEC3': NSEC3, 
   'NSEC3PARAM': NSEC3PARAM, 
   'TLSA': TLSA, 
   'HIP': HIP, 
   'SPF': SPF, 
   'UNSPEC': UNSPEC, 
   'TKEY': TKEY, 
   'TSIG': TSIG, 
   'IXFR': IXFR, 
   'AXFR': AXFR, 
   'MAILB': MAILB, 
   'MAILA': MAILA, 
   'ANY': ANY, 
   'TA': TA, 
   'DLV': DLV}
_by_value = dict([ (y, x) for x, y in _by_text.iteritems() ])
_metatypes = {OPT: True}
_singletons = {SOA: True, 
   NXT: True, 
   DNAME: True, 
   NSEC: True}
_unknown_type_pattern = re.compile('TYPE([0-9]+)$', re.I)

class UnknownRdatatype(dns.exception.DNSException):
    """Raised if a type is unknown."""
    pass


def from_text(text):
    """Convert text into a DNS rdata type value.
    @param text: the text
    @type text: string
    @raises dns.rdatatype.UnknownRdatatype: the type is unknown
    @raises ValueError: the rdata type value is not >= 0 and <= 65535
    @rtype: int"""
    value = _by_text.get(text.upper())
    if value is None:
        match = _unknown_type_pattern.match(text)
        if match == None:
            raise UnknownRdatatype
        value = int(match.group(1))
        if value < 0 or value > 65535:
            raise ValueError('type must be between >= 0 and <= 65535')
    return value


def to_text(value):
    """Convert a DNS rdata type to text.
    @param value: the rdata type value
    @type value: int
    @raises ValueError: the rdata type value is not >= 0 and <= 65535
    @rtype: string"""
    if value < 0 or value > 65535:
        raise ValueError('type must be between >= 0 and <= 65535')
    text = _by_value.get(value)
    if text is None:
        text = 'TYPE' + `value`
    return text


def is_metatype(rdtype):
    """True if the type is a metatype.
    @param rdtype: the type
    @type rdtype: int
    @rtype: bool"""
    if rdtype >= TKEY and rdtype <= ANY or _metatypes.has_key(rdtype):
        return True
    return False


def is_singleton(rdtype):
    """True if the type is a singleton.
    @param rdtype: the type
    @type rdtype: int
    @rtype: bool"""
    if _singletons.has_key(rdtype):
        return True
    return False