# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/martijndevos/Documents/tribler/Tribler/community/market/core/socket_address.py
# Compiled at: 2018-08-23 09:53:25
from Tribler.Core.Utilities.network_utils import is_valid_address

class SocketAddress(object):
    """Used for having a validated instance of a socket address for the candidate destination."""

    def __init__(self, ip, port):
        """
        :param ip: String representation of an ipv4 address
        :type ip: str
        :param port: Integer representation of a port
        :type port: int
        :raises ValueError: Thrown when one of the arguments are invalid
        """
        super(SocketAddress, self).__init__()
        if not is_valid_address((ip, port)):
            raise ValueError('Address is not valid')
        self._ip = ip
        self._port = port

    @property
    def ip(self):
        """
        :return: The ip
        :rtype: str
        """
        return self._ip

    @property
    def port(self):
        """
        :return: The port
        :rtype: int
        """
        return self._port