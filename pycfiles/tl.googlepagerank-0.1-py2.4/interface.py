# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tl/googlepagerank/interface.py
# Compiled at: 2007-01-24 14:37:04
"""Requesting a URL's page rank from Google and parsing the response.

The hash algorithm and query string assembly have been implemented after the
WWW::Google::PageRank Perl module by Yuri Karaban, who says he took the
knowledge from the pagerankstatus Mozilla extension in turn.
"""
import urllib, re
HOST = 'toolbarqueries.google.com'

def _cutoff32(value):
    return value % 4294967296


def _le_encode(value):
    """Encode an integer into 4 bytes in little-endian order.
    """
    value = _cutoff32(value)
    return [ value >> 8 * i & 255 for i in (0, 1, 2, 3) ]


def _le_decode(value):
    """Decode 4 bytes in little-endian order into an integer.
    """
    return sum((c << 8 * i for (i, c) in enumerate(value[:4])))


def _mix(a, b, c):
    c = _cutoff32(c)
    a = _cutoff32(a - b - c) ^ c >> 13
    b = _cutoff32(b - c - a) ^ _cutoff32(a << 8)
    c = _cutoff32(c - a - b) ^ b >> 13
    a = _cutoff32(a - b - c) ^ c >> 12
    b = _cutoff32(b - c - a) ^ _cutoff32(a << 16)
    c = _cutoff32(c - a - b) ^ b >> 5
    a = _cutoff32(a - b - c) ^ c >> 3
    b = _cutoff32(b - c - a) ^ _cutoff32(a << 10)
    c = _cutoff32(c - a - b) ^ b >> 15
    return (a, b, c)


def _checksum(value):
    (a, b, c) = (2654435769, 2654435769, 3862272608)
    index = 0
    while index <= len(value) - 12:
        (a, b, c) = _mix(a + _le_decode(value[index:index + 4]), b + _le_decode(value[index + 4:index + 8]), c + _le_decode(value[index + 8:index + 12]))
        index += 12

    (a, b, c) = _mix(a + _le_decode(value[index:index + 4]), b + _le_decode(value[index + 4:index + 8]), c + (_le_decode(value[index + 8:]) << 8) + len(value))
    return c


def checksum(value):
    ch = _checksum([ ord(c) for c in value ])
    ch = ch % 13 & 7 | ch / 7 << 2
    return _checksum(sum((_le_encode(ch - 9 * i) for i in xrange(20)), []))


def query_url(target):
    query = 'info:' + target
    params = urllib.urlencode({'client': 'navclient-auto', 'ch': '6%s' % checksum(query), 'ie': 'UTF-8', 'oe': 'UTF-8', 'features': 'Rank', 'q': query})
    return 'http://%s/search?%s' % (HOST, params)


def read_rank(response):
    groups = re.findall('^Rank_\\d+:\\d+:(\\d+)$', response.strip())
    if len(groups) == 1:
        return groups[0]
    else:
        raise ValueError