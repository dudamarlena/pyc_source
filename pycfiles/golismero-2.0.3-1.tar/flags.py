# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/thirdparty_libs/dns/flags.py
# Compiled at: 2013-08-26 10:52:44
"""DNS Message Flags."""
QR = 32768
AA = 1024
TC = 512
RD = 256
RA = 128
AD = 32
CD = 16
DO = 32768
_by_text = {'QR': QR, 
   'AA': AA, 
   'TC': TC, 
   'RD': RD, 
   'RA': RA, 
   'AD': AD, 
   'CD': CD}
_edns_by_text = {'DO': DO}
_by_value = dict([ (y, x) for x, y in _by_text.iteritems() ])
_edns_by_value = dict([ (y, x) for x, y in _edns_by_text.iteritems() ])

def _order_flags(table):
    order = list(table.iteritems())
    order.sort()
    order.reverse()
    return order


_flags_order = _order_flags(_by_value)
_edns_flags_order = _order_flags(_edns_by_value)

def _from_text(text, table):
    flags = 0
    tokens = text.split()
    for t in tokens:
        flags = flags | table[t.upper()]

    return flags


def _to_text(flags, table, order):
    text_flags = []
    for k, v in order:
        if flags & k != 0:
            text_flags.append(v)

    return (' ').join(text_flags)


def from_text(text):
    """Convert a space-separated list of flag text values into a flags
    value.
    @rtype: int"""
    return _from_text(text, _by_text)


def to_text(flags):
    """Convert a flags value into a space-separated list of flag text
    values.
    @rtype: string"""
    return _to_text(flags, _by_value, _flags_order)


def edns_from_text(text):
    """Convert a space-separated list of EDNS flag text values into a EDNS
    flags value.
    @rtype: int"""
    return _from_text(text, _edns_by_text)


def edns_to_text(flags):
    """Convert an EDNS flags value into a space-separated list of EDNS flag
    text values.
    @rtype: string"""
    return _to_text(flags, _edns_by_value, _edns_flags_order)