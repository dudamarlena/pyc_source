# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/thirdparty_libs/dns/rdataclass.py
# Compiled at: 2013-08-26 10:52:44
"""DNS Rdata Classes.

@var _by_text: The rdata class textual name to value mapping
@type _by_text: dict
@var _by_value: The rdata class value to textual name mapping
@type _by_value: dict
@var _metaclasses: If an rdataclass is a metaclass, there will be a mapping
whose key is the rdatatype value and whose value is True in this dictionary.
@type _metaclasses: dict"""
import re, dns.exception
RESERVED0 = 0
IN = 1
CH = 3
HS = 4
NONE = 254
ANY = 255
_by_text = {'RESERVED0': RESERVED0, 
   'IN': IN, 
   'CH': CH, 
   'HS': HS, 
   'NONE': NONE, 
   'ANY': ANY}
_by_value = dict([ (y, x) for x, y in _by_text.iteritems() ])
_by_text.update({'INTERNET': IN, 
   'CHAOS': CH, 
   'HESIOD': HS})
_metaclasses = {NONE: True, 
   ANY: True}
_unknown_class_pattern = re.compile('CLASS([0-9]+)$', re.I)

class UnknownRdataclass(dns.exception.DNSException):
    """Raised when a class is unknown."""
    pass


def from_text(text):
    """Convert text into a DNS rdata class value.
    @param text: the text
    @type text: string
    @rtype: int
    @raises dns.rdataclass.UnknownRdataclass: the class is unknown
    @raises ValueError: the rdata class value is not >= 0 and <= 65535
    """
    value = _by_text.get(text.upper())
    if value is None:
        match = _unknown_class_pattern.match(text)
        if match == None:
            raise UnknownRdataclass
        value = int(match.group(1))
        if value < 0 or value > 65535:
            raise ValueError('class must be between >= 0 and <= 65535')
    return value


def to_text(value):
    """Convert a DNS rdata class to text.
    @param value: the rdata class value
    @type value: int
    @rtype: string
    @raises ValueError: the rdata class value is not >= 0 and <= 65535
    """
    if value < 0 or value > 65535:
        raise ValueError('class must be between >= 0 and <= 65535')
    text = _by_value.get(value)
    if text is None:
        text = 'CLASS' + `value`
    return text


def is_metaclass(rdclass):
    """True if the class is a metaclass.
    @param rdclass: the rdata class
    @type rdclass: int
    @rtype: bool"""
    if _metaclasses.has_key(rdclass):
        return True
    return False