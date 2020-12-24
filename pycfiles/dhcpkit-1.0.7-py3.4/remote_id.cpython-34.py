# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/ipv6/extensions/remote_id.py
# Compiled at: 2017-06-08 10:49:31
# Size of source mod 2**32: 4918 bytes
"""
Implementation of Remote-ID option as specified in :rfc:`4649`.
"""
from struct import pack, unpack_from
from typing import Union
from dhcpkit.ipv6.messages import RelayForwardMessage, RelayReplyMessage
from dhcpkit.ipv6.options import Option
OPTION_REMOTE_ID = 37

class RemoteIdOption(Option):
    __doc__ = '\n    :rfc:`4649#section-3`\n\n    This option may be added by DHCPv6 relay agents that terminate\n    switched or permanent circuits and have mechanisms to identify the\n    remote host end of the circuit.\n\n    The format of the DHCPv6 Relay Agent Remote-ID option is shown below:\n\n    .. code-block:: none\n\n       0                   1                   2                   3\n       0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      |       OPTION_REMOTE_ID        |         option-len            |\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      |                       enterprise-number                       |\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      .                                                               .\n      .                           remote-id                           .\n      .                                                               .\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n\n    option-code\n        OPTION_REMOTE_ID (37).\n\n    option-len\n        4 + the length, in octets, of the remote-id field.  The minimum option-len is 5 octets.\n\n    enterprise-number\n        The vendor\'s registered Enterprise Number as registered with IANA [5].\n\n    remote-id\n        The opaque value for the remote-id.\n\n    The definition of the remote-id carried in this option is vendor\n    specific.  The vendor is indicated in the enterprise-number field.\n    The remote-id field may be used to encode, for instance:\n\n    - a "caller ID" telephone number for dial-up connection\n    - a "user name" prompted for by a Remote Access Server\n    - a remote caller ATM address\n    - a "modem ID" of a cable data modem\n    - the remote IP address of a point-to-point link\n    - a remote X.25 address for X.25 connections\n    - an interface or port identifier\n\n    Each vendor must ensure that the remote-id is unique for its\n    enterprise-number, as the octet sequence of enterprise-number\n    followed by remote-id must be globally unique.  One way to achieve\n    uniqueness might be to include the relay agent\'s DHCP Unique\n    Identifier (DUID) [1] in the remote-id.\n\n    :type enterprise_number: int\n    :type remote_id: bytes\n    '
    option_type = OPTION_REMOTE_ID

    def __init__(self, enterprise_number: int=0,
                 remote_id: bytes=b''):
        self.enterprise_number = enterprise_number
        self.remote_id = remote_id

    def validate(self):
        """
        Validate that the contents of this object conform to protocol specs.
        """
        if not isinstance(self.enterprise_number, int) or not 0 <= self.enterprise_number < 4294967296:
            raise ValueError('Enterprise number must be an unsigned 32 bit integer')
        if not isinstance(self.remote_id, bytes) or len(self.remote_id) >= 65536:
            raise ValueError('Remote-ID must be sequence of bytes')

    def load_from(self, buffer: bytes, offset: int=0, length: int=None) -> int:
        """
        Load the internal state of this object from the given buffer. The buffer may contain more data after the
        structured element is parsed. This data is ignored.

        :param buffer: The buffer to read data from
        :param offset: The offset in the buffer where to start reading
        :param length: The amount of data we are allowed to read from the buffer
        :return: The number of bytes used from the buffer
        """
        my_offset, option_len = self.parse_option_header(buffer, offset, length)
        self.enterprise_number = unpack_from('!I', buffer, offset=offset + my_offset)[0]
        my_offset += 4
        remote_id_length = option_len - 4
        self.remote_id = buffer[offset + my_offset:offset + my_offset + remote_id_length]
        my_offset += remote_id_length
        return my_offset

    def save(self) -> Union[(bytes, bytearray)]:
        """
        Save the internal state of this object as a buffer.

        :return: The buffer with the data from this element
        """
        return pack('!HHI', self.option_type, len(self.remote_id) + 4, self.enterprise_number) + self.remote_id


RelayForwardMessage.add_may_contain(RemoteIdOption)
RelayReplyMessage.add_may_contain(RemoteIdOption)