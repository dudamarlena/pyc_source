# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/ipv6/server/listeners/factories.py
# Compiled at: 2017-06-20 18:44:39
# Size of source mod 2**32: 1573 bytes
"""
Factory base classes for listener factories
"""
import socket
from ipaddress import IPv6Address
from dhcpkit.common.server.config_elements import ConfigElementFactory
from dhcpkit.ipv6 import SERVER_PORT

class ListenerFactory(ConfigElementFactory):
    __doc__ = '\n    Base class for listener factories\n    '
    sock_type = None
    sock_proto = None
    listen_port = SERVER_PORT

    def match_socket(self, sock: socket.socket, address: IPv6Address, interface: int=0) -> bool:
        """
        Determine if we can recycle this socket

        :param sock: An existing socket
        :param address: The address we want
        :param interface: The interface number we want
        :return: Whether the socket is suitable
        """
        if sock.family != socket.AF_INET6 or sock.type != self.sock_type or sock.proto != self.sock_proto:
            return False
        sockname = sock.getsockname()
        if IPv6Address(sockname[0].split('%')[0]) != address or sockname[1] != self.listen_port or sockname[3] != interface:
            return False
        return True


class UDPListenerFactory(ListenerFactory):
    __doc__ = '\n    Base class for UDP listener factories\n    '
    sock_type = socket.SOCK_DGRAM
    sock_proto = socket.IPPROTO_UDP


class TCPListenerFactory(ListenerFactory):
    __doc__ = '\n    Base class for TCP listener factories\n    '
    sock_type = socket.SOCK_STREAM
    sock_proto = socket.IPPROTO_TCP