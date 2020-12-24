# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/thirdparty_libs/dns/reversename.py
# Compiled at: 2013-08-26 10:52:44
"""DNS Reverse Map Names.

@var ipv4_reverse_domain: The DNS IPv4 reverse-map domain, in-addr.arpa.
@type ipv4_reverse_domain: dns.name.Name object
@var ipv6_reverse_domain: The DNS IPv6 reverse-map domain, ip6.arpa.
@type ipv6_reverse_domain: dns.name.Name object
"""
import dns.name, dns.ipv6, dns.ipv4
ipv4_reverse_domain = dns.name.from_text('in-addr.arpa.')
ipv6_reverse_domain = dns.name.from_text('ip6.arpa.')

def from_address(text):
    """Convert an IPv4 or IPv6 address in textual form into a Name object whose
    value is the reverse-map domain name of the address.
    @param text: an IPv4 or IPv6 address in textual form (e.g. '127.0.0.1',
    '::1')
    @type text: str
    @rtype: dns.name.Name object
    """
    try:
        parts = list(dns.ipv6.inet_aton(text).encode('hex_codec'))
        origin = ipv6_reverse_domain
    except:
        parts = [ '%d' % ord(byte) for byte in dns.ipv4.inet_aton(text) ]
        origin = ipv4_reverse_domain

    parts.reverse()
    return dns.name.from_text(('.').join(parts), origin=origin)


def to_address(name):
    """Convert a reverse map domain name into textual address form.
    @param name: an IPv4 or IPv6 address in reverse-map form.
    @type name: dns.name.Name object
    @rtype: str
    """
    if name.is_subdomain(ipv4_reverse_domain):
        name = name.relativize(ipv4_reverse_domain)
        labels = list(name.labels)
        labels.reverse()
        text = ('.').join(labels)
        return dns.ipv4.inet_ntoa(dns.ipv4.inet_aton(text))
    if name.is_subdomain(ipv6_reverse_domain):
        name = name.relativize(ipv6_reverse_domain)
        labels = list(name.labels)
        labels.reverse()
        parts = []
        i = 0
        l = len(labels)
        while i < l:
            parts.append(('').join(labels[i:i + 4]))
            i += 4

        text = (':').join(parts)
        return dns.ipv6.inet_ntoa(dns.ipv6.inet_aton(text))
    raise dns.exception.SyntaxError('unknown reverse-map address family')