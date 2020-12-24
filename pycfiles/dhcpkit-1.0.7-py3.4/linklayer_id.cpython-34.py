# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/ipv6/extensions/linklayer_id.py
# Compiled at: 2017-06-08 10:49:31
# Size of source mod 2**32: 4384 bytes
"""
Implementation of the Client LinkLayer Address relay option as specified in :rfc:`6939`.
"""
from struct import pack, unpack_from
from typing import Union
from dhcpkit.display_strings import hardware_types
from dhcpkit.ipv6.messages import RelayServerMessage
from dhcpkit.ipv6.options import Option
from dhcpkit.protocol_element import ElementDataRepresentation
OPTION_CLIENT_LINKLAYER_ADDR = 79

class LinkLayerIdOption(Option):
    __doc__ = '\n    :rfc:`6939#section-4`\n\n    The format of the DHCPv6 Client Link-Layer Address option is shown\n    below.\n\n    .. code-block:: none\n\n       0                   1                   2                   3\n       0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      | OPTION_CLIENT_LINKLAYER_ADDR  |           option-length       |\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      |   link-layer type (16 bits)   |                               |\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+                               |\n      |               link-layer address (variable length)            |\n      |                                                               |\n      |                                                               |\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n\n    option-code\n        OPTION_CLIENT_LINKLAYER_ADDR (79)\n\n    option-length\n        2 + length of link-layer address\n\n    link-layer type\n        Client link-layer address type.  The link-layer\n        type MUST be a valid hardware type assigned\n        by the IANA, as described in :rfc:`826`\n\n    link-layer address\n        Client link-layer address\n\n    '
    option_type = OPTION_CLIENT_LINKLAYER_ADDR

    def __init__(self, link_layer_type: int=0,
                 link_layer_address: bytes=b''):
        self.link_layer_type = link_layer_type
        self.link_layer_address = link_layer_address

    def display_link_layer_type(self) -> ElementDataRepresentation:
        """
        Nicer representation of hardware types
        :return: Representation of hardware type
        """
        display = hardware_types.get(self.link_layer_type, 'Unknown')
        return ElementDataRepresentation('{} ({})'.format(display, self.link_layer_type))

    def validate(self):
        """
        Validate that the contents of this object conform to protocol specs.
        """
        if not isinstance(self.link_layer_type, int) or not 0 <= self.link_layer_type < 65536:
            raise ValueError('Link-layer type must be an unsigned 16 bit integer')
        if not isinstance(self.link_layer_address, bytes):
            raise ValueError('Link-layer address must be a sequence of bytes')
        if len(self.link_layer_address) > 65533:
            raise ValueError('link-layer address cannot be longer than {} bytes'.format(65533))

    def load_from(self, buffer: bytes, offset: int=0, length: int=None) -> int:
        """
        Load the internal state of this object from the given buffer. The buffer may contain more data after the
        structured element is parsed. This data is ignored.

        :param buffer: The buffer to read data from
        :param offset: The offset in the buffer where to start reading
        :param length: The amount of data we are allowed to read from the buffer
        :return: The number of bytes used from the buffer
        """
        my_offset, option_len = self.parse_option_header(buffer, offset, length, min_length=2)
        self.link_layer_type = unpack_from('!H', buffer, offset=offset + my_offset)[0]
        my_offset += 2
        ll_len = option_len - 2
        self.link_layer_address = buffer[offset + my_offset:offset + my_offset + ll_len]
        my_offset += ll_len
        return my_offset

    def save(self) -> Union[(bytes, bytearray)]:
        """
        Save the internal state of this object as a buffer.

        :return: The buffer with the data from this element
        """
        buffer = bytearray()
        buffer.extend(pack('!HHH', self.option_type, len(self.link_layer_address) + 2, self.link_layer_type))
        buffer.extend(self.link_layer_address)
        return buffer


RelayServerMessage.add_may_contain(LinkLayerIdOption, 0, 1)