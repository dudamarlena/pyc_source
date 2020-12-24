# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/ipv6/server/config_datatypes.py
# Compiled at: 2016-09-05 09:40:14
# Size of source mod 2**32: 1121 bytes
"""
Extra datatypes for the server configuration
"""
from ipaddress import IPv6Address
from dhcpkit.ipv6.messages import Message
from dhcpkit.utils import camelcase_to_dash
from typing import Type

def unicast_address(value: str) -> IPv6Address:
    """
    Parse an IPv6 address and make sure it is a unicast address

    :param value: The address as string
    :return: The parsed IPv6 address
    """
    address = IPv6Address(value)
    if address.is_link_local or address.is_loopback or address.is_multicast or address.is_unspecified:
        raise ValueError('Address must be a routable IPv6 address')
    return address


def message_type(value: str) -> Type[Message]:
    """
    Parse the value as the name of a DHCPv6 message type

    :param value: The name of the message type
    :return: The message class
    """
    from dhcpkit.ipv6.message_registry import message_registry
    search_value = camelcase_to_dash(value)
    try:
        return message_registry.by_name[search_value]
    except KeyError:
        raise ValueError('{} is not a valid message type'.format(value))