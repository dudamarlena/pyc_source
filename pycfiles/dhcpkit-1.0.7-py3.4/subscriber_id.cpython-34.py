# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/ipv6/extensions/subscriber_id.py
# Compiled at: 2017-06-08 10:49:31
# Size of source mod 2**32: 4411 bytes
"""
Implementation of Subscriber-ID option as specified in :rfc:`4580`.
"""
from struct import pack
from typing import Union
from dhcpkit.ipv6.messages import RelayForwardMessage, RelayReplyMessage
from dhcpkit.ipv6.options import Option
OPTION_SUBSCRIBER_ID = 38

class SubscriberIdOption(Option):
    __doc__ = "\n    :rfc:`4580#section-2`\n\n    The subscriber-id information allows the service provider to assign/\n    activate subscriber-specific actions; e.g., assignment of specific IP\n    addresses, prefixes, DNS configuration, trigger accounting, etc.\n    This option is de-coupled from the access network's physical\n    structure, so a subscriber that moves from one access-point to\n    another, for example, would not require reconfiguration at the\n    service provider's DHCPv6 servers.\n\n    The subscriber-id information is only intended for use within a\n    single administrative domain and is only exchanged between the relay\n    agents and DHCPv6 servers within that domain.  Therefore, the format\n    and encoding of the data in the option is not standardized, and this\n    specification does not establish any semantic requirements on the\n    data.  This specification only defines the option for conveying this\n    information from relay agents to DHCPv6 servers.\n\n    However, as the DHCPv4 Subscriber-ID suboption [3] specifies Network\n    Virtual Terminal (NVT) American Standard Code for Information\n    Interchange (ASCII) [4] encoded data, in environments where both\n    DHCPv4 [5] and DHCPv6 are being used, it may be beneficial to use\n    that encoding.\n\n    The format of the DHCPv6 Relay Agent Subscriber-ID option is shown\n    below:\n\n    .. code-block:: none\n\n       0                   1                   2                   3\n       0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      |     OPTION_SUBSCRIBER_ID      |         option-len            |\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      .                                                               .\n      .                         subscriber-id                         .\n      .                                                               .\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n\n    option-code\n        OPTION_SUBSCRIBER_ID (38)\n\n    option-len\n        length, in octets, of the subscriber-id field.\n        The minimum length is 1 octet.\n\n    subscriber-id\n        The subscriber's identity.\n\n    "
    option_type = OPTION_SUBSCRIBER_ID

    def __init__(self, subscriber_id: bytes=b''):
        self.subscriber_id = subscriber_id

    def validate(self):
        """
        Validate that the contents of this object conform to protocol specs.
        """
        if not isinstance(self.subscriber_id, bytes):
            raise ValueError('Subscriber-ID must be sequence of bytes')
        if len(self.subscriber_id) > 65535:
            raise ValueError('Subscriber-ID cannot be longer than {} bytes'.format(65535))

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
        self.subscriber_id = buffer[offset + my_offset:offset + my_offset + option_len]
        my_offset += option_len
        return my_offset

    def save(self) -> Union[(bytes, bytearray)]:
        """
        Save the internal state of this object as a buffer.

        :return: The buffer with the data from this element
        """
        return pack('!HH', self.option_type, len(self.subscriber_id)) + self.subscriber_id


RelayForwardMessage.add_may_contain(SubscriberIdOption)
RelayReplyMessage.add_may_contain(SubscriberIdOption)