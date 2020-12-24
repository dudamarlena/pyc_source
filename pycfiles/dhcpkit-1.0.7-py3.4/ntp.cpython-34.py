# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/ipv6/extensions/ntp.py
# Compiled at: 2017-06-23 19:17:12
# Size of source mod 2**32: 22330 bytes
"""
Implementation of NTP options as specified in :rfc:`5908`.
"""
import codecs
from ipaddress import IPv6Address
from struct import pack, unpack_from
from dhcpkit.ipv6.messages import AdvertiseMessage, InformationRequestMessage, RebindMessage, RenewMessage, ReplyMessage, RequestMessage, SolicitMessage
from dhcpkit.ipv6.options import Option
from dhcpkit.protocol_element import ProtocolElement
from dhcpkit.utils import encode_domain, parse_domain_bytes
from typing import Iterable, Tuple, Union
OPTION_NTP_SERVER = 56
NTP_SUBOPTION_SRV_ADDR = 1
NTP_SUBOPTION_MC_ADDR = 2
NTP_SUBOPTION_SRV_FQDN = 3

class NTPSubOption(ProtocolElement):
    __doc__ = '\n    :rfc:`5908`\n\n    :type suboption_type: int\n    '
    suboption_type = 0
    config_datatype = None

    @property
    def value(self) -> str:
        """
        Return a simple string representation of the value of this sub-option.

        :return: The value of this option as a string
        """
        raise NotImplementedError

    @classmethod
    def determine_class(cls, buffer: bytes, offset: int=0) -> type:
        """
        Return the appropriate subclass from the registry, or UnknownNTPSubOption if no subclass is registered.

        :param buffer: The buffer to read data from
        :param offset: The offset in the buffer where to start reading
        :return: The best known class for this suboption data
        """
        from .ntp_suboption_registry import ntp_suboption_registry
        suboption_type = unpack_from('!H', buffer, offset=offset)[0]
        return ntp_suboption_registry.get(suboption_type, UnknownNTPSubOption)

    def parse_suboption_header(self, buffer: bytes, offset: int=0,
                               length: int=None) -> Tuple[(int, int)]:
        """
        Parse the option code and length from the buffer and perform some basic validation.

        :param buffer: The buffer to read data from
        :param offset: The offset in the buffer where to start reading
        :param length: The amount of data we are allowed to read from the buffer
        :return: The number of bytes used from the buffer and the value of the suboption-len field
        """
        suboption_type, suboption_len = unpack_from('!HH', buffer, offset=offset)
        my_offset = 4
        if suboption_type != self.suboption_type:
            raise ValueError('The provided buffer does not contain {} data'.format(self.__class__.__name__))
        if length is not None:
            if suboption_len + my_offset > length:
                raise ValueError('This suboption is longer than the available buffer')
        return (
         my_offset, suboption_len)


class UnknownNTPSubOption(NTPSubOption):
    __doc__ = "\n    Container for raw NTP sub-option content for cases where we don't know how to decode it.\n\n    :type suboption_data: bytes\n    "

    def __init__(self, suboption_type: int=0,
                 suboption_data: bytes=b''):
        self.suboption_type = suboption_type
        self.suboption_data = suboption_data

    @property
    def value(self) -> str:
        """
        Return a simple string representation of the value of this sub-option.

        :return: The value of this option as a string
        """
        return codecs.encode(self.suboption_data, 'hex').decode('ascii')

    def validate(self):
        """
        Validate that the contents of this object conform to protocol specs.
        """
        if not isinstance(self.suboption_type, int) or not 0 <= self.suboption_type < 65536:
            raise ValueError('Sub-option type must be an unsigned 16 bit integer')
        if not isinstance(self.suboption_data, bytes):
            raise ValueError('Sub-option data must be sequence of bytes')

    def load_from(self, buffer: bytes, offset: int=0, length: int=None) -> int:
        """
        Load the internal state of this object from the given buffer. The buffer may contain more data after the
        structured element is parsed. This data is ignored.

        :param buffer: The buffer to read data from
        :param offset: The offset in the buffer where to start reading
        :param length: The amount of data we are allowed to read from the buffer
        :return: The number of bytes used from the buffer
        """
        my_offset = 0
        self.suboption_type, option_len = unpack_from('!HH', buffer, offset=offset + my_offset)
        my_offset += 4
        max_length = length or len(buffer) - offset
        if my_offset + option_len > max_length:
            raise ValueError('This suboption is longer than the available buffer')
        self.suboption_data = buffer[offset + my_offset:offset + my_offset + option_len]
        my_offset += option_len
        return my_offset

    def save(self) -> Union[(bytes, bytearray)]:
        """
        Save the internal state of this object as a buffer.

        :return: The buffer with the data from this element
        """
        return pack('!HH', self.suboption_type, len(self.suboption_data)) + self.suboption_data


class NTPServerAddressSubOption(NTPSubOption):
    __doc__ = '\n    :rfc:`5908#section-4.1`\n\n    This suboption is intended to appear inside the OPTION_NTP_SERVER\n    option.  It specifies the IPv6 unicast address of an NTP server or\n    SNTP server available to the client.\n\n    The format of the NTP Server Address Suboption is:\n\n    .. code-block:: none\n\n       0                   1                   2                   3\n       0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      |    NTP_SUBOPTION_SRV_ADDR     |        suboption-len = 16     |\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      |                                                               |\n      |                                                               |\n      |                   IPv6 address of NTP server                  |\n      |                                                               |\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n\n    IPv6 address of the NTP server\n        An IPv6 address.\n\n    suboption-code\n        NTP_SUBOPTION_SRV_ADDR (1).\n\n    suboption-len\n        16.\n\n    :type address: IPv6Address\n    '
    suboption_type = NTP_SUBOPTION_SRV_ADDR

    def __init__(self, address: IPv6Address=None):
        self.address = address

    @staticmethod
    def config_datatype(value: str) -> IPv6Address:
        """
        Convert string data from the configuration to an IPv6address.

        :param value: String from config file
        :return: Parsed IPv6 address
        """
        value = IPv6Address(value)
        if value.is_link_local or value.is_loopback or value.is_multicast or value.is_unspecified:
            raise ValueError('NTP server address must be a routable IPv6 address')
        return value

    @property
    def value(self) -> str:
        """
        Return a simple string representation of the value of this sub-option.

        :return: The value of this option as a string
        """
        return str(self.address)

    def validate(self):
        """
        Validate that the contents of this object conform to protocol specs.
        """
        if not isinstance(self.address, IPv6Address) or self.address.is_link_local or self.address.is_loopback or self.address.is_multicast or self.address.is_unspecified:
            raise ValueError('NTP server address must be a routable IPv6 address')

    def load_from(self, buffer: bytes, offset: int=0, length: int=None) -> int:
        """
        Load the internal state of this object from the given buffer. The buffer may contain more data after the
        structured element is parsed. This data is ignored.

        :param buffer: The buffer to read data from
        :param offset: The offset in the buffer where to start reading
        :param length: The amount of data we are allowed to read from the buffer
        :return: The number of bytes used from the buffer
        """
        my_offset, suboption_len = self.parse_suboption_header(buffer, offset, length)
        if suboption_len != 16:
            raise ValueError('NTP Server Address SubOptions must have length 16')
        self.address = IPv6Address(buffer[offset + my_offset:offset + my_offset + 16])
        my_offset += 16
        return my_offset

    def save(self) -> Union[(bytes, bytearray)]:
        """
        Save the internal state of this object as a buffer.

        :return: The buffer with the data from this element
        """
        buffer = bytearray()
        buffer.extend(pack('!HH', self.suboption_type, 16))
        buffer.extend(self.address.packed)
        return buffer


class NTPMulticastAddressSubOption(NTPSubOption):
    __doc__ = '\n    :rfc:`5908#section-4.2`\n\n    This suboption is intended to appear inside the OPTION_NTP_SERVER\n    option.  It specifies the IPv6 address of the IPv6 multicast group\n    address used by NTP on the local network.\n\n    The format of the NTP Multicast Address Suboption is:\n\n    .. code-block:: none\n\n       0                   1                   2                   3\n       0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      |    NTP_SUBOPTION_MC_ADDR      |        suboption-len = 16     |\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      |                                                               |\n      |                                                               |\n      |                   Multicast IPv6 address                      |\n      |                                                               |\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n\n    Multicast IPv6 address\n        An IPv6 address.\n\n    suboption-code\n        NTP_SUBOPTION_MC_ADDR (2).\n\n    suboption-len\n        16.\n\n    :type address: IPv6Address\n    '
    suboption_type = NTP_SUBOPTION_MC_ADDR

    def __init__(self, address: IPv6Address=None):
        self.address = address

    @staticmethod
    def config_datatype(value: str) -> IPv6Address:
        """
        Convert string data from the configuration to an IPv6address.

        :param value: String from config file
        :return: Parsed IPv6 address
        """
        value = IPv6Address(value)
        if not value.is_multicast:
            raise ValueError('NTP multicast address must be a multicast IPv6 address')
        return value

    @property
    def value(self) -> str:
        """
        Return a simple string representation of the value of this sub-option.

        :return: The value of this option as a string
        """
        return str(self.address)

    def validate(self):
        """
        Validate that the contents of this object conform to protocol specs.
        """
        if not isinstance(self.address, IPv6Address) or not self.address.is_multicast:
            raise ValueError('NTP multicast address must be a multicast IPv6 address')

    def load_from(self, buffer: bytes, offset: int=0, length: int=None) -> int:
        """
        Load the internal state of this object from the given buffer. The buffer may contain more data after the
        structured element is parsed. This data is ignored.

        :param buffer: The buffer to read data from
        :param offset: The offset in the buffer where to start reading
        :param length: The amount of data we are allowed to read from the buffer
        :return: The number of bytes used from the buffer
        """
        my_offset, suboption_len = self.parse_suboption_header(buffer, offset, length)
        if suboption_len != 16:
            raise ValueError('NTP Multicast Address SubOptions must have length 16')
        self.address = IPv6Address(buffer[offset + my_offset:offset + my_offset + 16])
        my_offset += 16
        return my_offset

    def save(self) -> Union[(bytes, bytearray)]:
        """
        Save the internal state of this object as a buffer.

        :return: The buffer with the data from this element
        """
        buffer = bytearray()
        buffer.extend(pack('!HH', self.suboption_type, 16))
        buffer.extend(self.address.packed)
        return buffer


class NTPServerFQDNSubOption(NTPSubOption):
    __doc__ = '\n    :rfc:`5908#section-4.3`\n\n    This suboption is intended to appear inside the OPTION_NTP_SERVER\n    option.  It specifies the FQDN of an NTP server or SNTP server\n    available to the client.\n\n    The format of the NTP Server FQDN Suboption is:\n\n    .. code-block:: none\n\n      0                   1                   2                   3\n      0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      |    NTP_SUBOPTION_SRV_FQDN     |         suboption-len         |\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      |                                                               |\n      |                      FQDN of NTP server                       |\n      :                                                               :\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n\n    suboption-code\n        NTP_SUBOPTION_SRV_FQDN (3).\n\n    suboption-len\n        Length of the included FQDN field.\n\n    FQDN\n        Fully-Qualified Domain Name of the NTP server or SNTP server. This field MUST be encoded as described in\n        :rfc:`3315`, Section 8.  Internationalized domain names are not allowed in this field.\n\n    :type fqdn: str\n    '
    suboption_type = NTP_SUBOPTION_SRV_FQDN

    def __init__(self, fqdn: str=''):
        self.fqdn = fqdn

    @staticmethod
    def config_datatype(value: str) -> str:
        """
        Convert string data from the configuration to, well, a string. But a validated string!

        :param value: String from config file
        :return: Parsed fqdn
        """
        encode_domain(value)
        return value

    @property
    def value(self) -> str:
        """
        Return a simple string representation of the value of this sub-option.

        :return: The value of this option as a string
        """
        return self.fqdn

    def validate(self):
        """
        Validate that the contents of this object conform to protocol specs.
        """
        if not isinstance(self.fqdn, str):
            raise ValueError('FQDN must be a string')
        encode_domain(self.fqdn)

    def load_from(self, buffer: bytes, offset: int=0,
                  length: int=None) -> int:
        """
        Load the internal state of this object from the given buffer. The buffer may contain more data after the
        structured element is parsed. This data is ignored.

        :param buffer: The buffer to read data from
        :param offset: The offset in the buffer where to start reading
        :param length: The amount of data we are allowed to read from the buffer
        :return: The number of bytes used from the buffer
        """
        my_offset, suboption_len = self.parse_suboption_header(buffer, offset, length)
        header_offset = my_offset
        max_offset = suboption_len + header_offset
        domain_name_len, self.fqdn = parse_domain_bytes(buffer, offset=offset + my_offset, length=suboption_len)
        my_offset += domain_name_len
        if my_offset != max_offset:
            raise ValueError('Option length does not match the length of the included fqdn')
        return my_offset

    def save(self) -> Union[(bytes, bytearray)]:
        """
        Save the internal state of this object as a buffer.

        :return: The buffer with the data from this element
        """
        fqdn_buffer = encode_domain(self.fqdn)
        buffer = bytearray()
        buffer.extend(pack('!HH', self.suboption_type, len(fqdn_buffer)))
        buffer.extend(fqdn_buffer)
        return buffer


class NTPServersOption(Option):
    __doc__ = "\n    :rfc:`5908#section-4`\n\n    This option serves as a container for server location information\n    related to one NTP server or Simple Network Time Protocol (SNTP)\n    :rfc:`4330` server.  This option can appear multiple times in a DHCPv6\n    message.  Each instance of this option is to be considered by the NTP\n    client or SNTP client as a server to include in its configuration.\n\n    The option itself does not contain any value.  Instead, it contains\n    one or several suboptions that carry NTP server or SNTP server\n    location.  This option MUST include one, and only one, time source\n    suboption.  The currently defined time source suboptions are\n    NTP_OPTION_SRV_ADDR, NTP_OPTION_SRV_MC_ADDR, and NTP_OPTION_SRV_FQDN.\n    It carries the NTP server or SNTP server location as a unicast or\n    multicast IPv6 address or as an NTP server or SNTP server FQDN.  More\n    time source suboptions may be defined in the future.  While the FQDN\n    option offers the most deployment flexibility, resiliency as well as\n    security, the IP address options are defined to cover cases where a\n    DNS dependency is not desirable.\n\n    If the NTP server or SNTP server location is an IPv6 multicast\n    address, the client SHOULD use this address as an NTP multicast group\n    address and listen to messages sent to this group in order to\n    synchronize its clock.\n\n    The format of the NTP Server Option is:\n\n    .. code-block:: none\n\n       0                   1                   2                   3\n       0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      |      OPTION_NTP_SERVER        |          option-len           |\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      |                         suboption-1                           |\n      :                                                               :\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      |                         suboption-2                           |\n      :                                                               :\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      :                                                               :\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      |                         suboption-n                           |\n      :                                                               :\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n\n    option-code\n        OPTION_NTP_SERVER (56).\n\n    option-len\n        Total length of the included suboptions.\n\n    This document does not define any priority relationship between the\n    client's embedded configuration (if any) and the NTP or SNTP servers\n    discovered via this option.  In particular, the client is allowed to\n    simultaneously use its own configured NTP servers or SNTP servers and\n    the servers discovered via DHCP.\n\n    :type options: list[NTPSubOption]\n    "
    option_type = OPTION_NTP_SERVER

    def __init__(self, options: Iterable[NTPSubOption]=None):
        self.options = list(options or [])

    def validate(self):
        """
        Validate that the contents of this object conform to protocol specs.
        """
        self.validate_contains(self.options)
        for option in self.options:
            option.validate()

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
        header_offset = my_offset
        self.options = []
        max_offset = option_len + header_offset
        while max_offset > my_offset:
            used_buffer, option = NTPSubOption.parse(buffer, offset=offset + my_offset)
            self.options.append(option)
            my_offset += used_buffer

        if my_offset != max_offset:
            raise ValueError('Option length does not match the combined length of the parsed suboptions')
        return my_offset

    def save(self) -> Union[(bytes, bytearray)]:
        """
        Save the internal state of this object as a buffer.

        :return: The buffer with the data from this element
        """
        options_buffer = bytearray()
        for option in self.options:
            options_buffer.extend(option.save())

        buffer = bytearray()
        buffer.extend(pack('!HH', self.option_type, len(options_buffer)))
        buffer.extend(options_buffer)
        return buffer


SolicitMessage.add_may_contain(NTPServersOption)
AdvertiseMessage.add_may_contain(NTPServersOption)
RequestMessage.add_may_contain(NTPServersOption)
RenewMessage.add_may_contain(NTPServersOption)
RebindMessage.add_may_contain(NTPServersOption)
InformationRequestMessage.add_may_contain(NTPServersOption)
ReplyMessage.add_may_contain(NTPServersOption)
NTPServersOption.add_may_contain(NTPSubOption, 1)