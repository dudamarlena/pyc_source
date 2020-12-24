# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/dave/Projects/Github/proxenos/src/proxenos/node.py
# Compiled at: 2017-01-23 19:52:58
"""Provides structures for representing nodes."""
from __future__ import absolute_import
import socket, struct, typing, attr, netaddr, netaddr.strategy.ipv6
__all__ = ('Service', 'SocketAddress')

def ipv6_address(addr, resolve=True):
    try:
        return netaddr.IPAddress(addr).ipv6(ipv4_compatible=True)
    except netaddr.AddrFormatError:
        if not resolve or isinstance(addr, int):
            raise
        return ipv6_address(socket.gethostbyname(str(addr)), resolve=False)


@attr.s(frozen=True, slots=True)
class SocketAddress(object):
    """Represents an Internet (AF_INET) socket address.

    Args:
        host (str or int): Accepts an IP address in the form of a string
            or integer, or a domain name. Both IPv4 and IPv6 addresses
            are supported.
        port (int): The port number of the destination socket.

    """
    host = attr.ib(convert=ipv6_address)
    port = attr.ib(convert=int)

    @classmethod
    def unpack(cls, addr_bytes):
        """Unpacks a 24-bit bytestring to a :class:`SocketAddress`.

        Args:
            addr_bytes: A bytestring containing an IPv6 address as a
                packed binary string followed by a port number.

        Returns:
            A :class:`~.node.SocketAddress` instance.

        """
        unpacked = struct.unpack('>8H4H', addr_bytes)
        port = 0
        for i, word in enumerate(unpacked[8:][::-1]):
            port |= word << 4 * i

        host = netaddr.strategy.ipv6.words_to_int(unpacked[:8])
        return cls(host, port)

    def pack(self):
        """Packs a socket address into a 24-bit struct.

        Returns:
            A bytestring containing the packed host and port.

        """
        port_words = netaddr.strategy.ipv6.int_to_words(self.port, 4, 4)
        return struct.pack('>8H4H', *(self.host.words + port_words))

    def __bytes__(self):
        return self.pack()

    def __str__(self):
        try:
            return ('{}:{}').format(self.host.ipv4(), self.port)
        except netaddr.AddrConversionError:
            return ('{}:{}').format(self.host, self.port)


@attr.s(frozen=True, slots=True)
class Service(object):
    """Represents a named service."""
    name = attr.ib(convert=str)
    socket_address = attr.ib(validator=attr.validators.instance_of(SocketAddress))
    tags = attr.ib(convert=frozenset)