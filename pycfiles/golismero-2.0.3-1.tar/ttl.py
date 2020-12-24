# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/thirdparty_libs/dns/ttl.py
# Compiled at: 2013-08-26 10:52:44
"""DNS TTL conversion."""
import dns.exception

class BadTTL(dns.exception.SyntaxError):
    pass


def from_text(text):
    """Convert the text form of a TTL to an integer.

    The BIND 8 units syntax for TTLs (e.g. '1w6d4h3m10s') is supported.

    @param text: the textual TTL
    @type text: string
    @raises dns.ttl.BadTTL: the TTL is not well-formed
    @rtype: int
    """
    if text.isdigit():
        total = long(text)
    else:
        if not text[0].isdigit():
            raise BadTTL
        total = 0
        current = 0
        for c in text:
            if c.isdigit():
                current *= 10
                current += long(c)
            else:
                c = c.lower()
                if c == 'w':
                    total += current * 604800
                elif c == 'd':
                    total += current * 86400
                elif c == 'h':
                    total += current * 3600
                elif c == 'm':
                    total += current * 60
                elif c == 's':
                    total += current
                else:
                    raise BadTTL("unknown unit '%s'" % c)
                current = 0

    if not current == 0:
        raise BadTTL('trailing integer')
    if total < 0 or total > 2147483647:
        raise BadTTL('TTL should be between 0 and 2^31 - 1 (inclusive)')
    return total