# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/thirdparty_libs/dns/inet.py
# Compiled at: 2013-08-26 10:52:44
"""Generic Internet address helper functions."""
import socket, dns.ipv4, dns.ipv6
AF_INET = socket.AF_INET
try:
    AF_INET6 = socket.AF_INET6
except AttributeError:
    AF_INET6 = 9999

def inet_pton(family, text):
    """Convert the textual form of a network address into its binary form.

    @param family: the address family
    @type family: int
    @param text: the textual address
    @type text: string
    @raises NotImplementedError: the address family specified is not
    implemented.
    @rtype: string
    """
    if family == AF_INET:
        return dns.ipv4.inet_aton(text)
    if family == AF_INET6:
        return dns.ipv6.inet_aton(text)
    raise NotImplementedError


def inet_ntop(family, address):
    """Convert the binary form of a network address into its textual form.

    @param family: the address family
    @type family: int
    @param address: the binary address
    @type address: string
    @raises NotImplementedError: the address family specified is not
    implemented.
    @rtype: string
    """
    if family == AF_INET:
        return dns.ipv4.inet_ntoa(address)
    if family == AF_INET6:
        return dns.ipv6.inet_ntoa(address)
    raise NotImplementedError


def af_for_address(text):
    """Determine the address family of a textual-form network address.

    @param text: the textual address
    @type text: string
    @raises ValueError: the address family cannot be determined from the input.
    @rtype: int
    """
    try:
        junk = dns.ipv4.inet_aton(text)
        return AF_INET
    except:
        try:
            junk = dns.ipv6.inet_aton(text)
            return AF_INET6
        except:
            raise ValueError


def is_multicast(text):
    """Is the textual-form network address a multicast address?

    @param text: the textual address
    @raises ValueError: the address family cannot be determined from the input.
    @rtype: bool
    """
    try:
        first = ord(dns.ipv4.inet_aton(text)[0])
        return first >= 224 and first <= 239
    except:
        try:
            first = ord(dns.ipv6.inet_aton(text)[0])
            return first == 255
        except:
            raise ValueError