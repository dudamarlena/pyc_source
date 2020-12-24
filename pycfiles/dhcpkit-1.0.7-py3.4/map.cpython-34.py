# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/ipv6/extensions/map.py
# Compiled at: 2017-06-08 11:09:29
# Size of source mod 2**32: 38770 bytes
"""
Implementation of MAP options as specified in :rfc:`7598`.
"""
import math
from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network
from struct import pack, unpack
from typing import Iterable, List, Optional, Type, Union
from dhcpkit.ipv6.messages import AdvertiseMessage, ConfirmMessage, RebindMessage, ReleaseMessage, RenewMessage, ReplyMessage, RequestMessage, SolicitMessage
from dhcpkit.ipv6.options import Option, SomeOption
OPTION_S46_RULE = 89
OPTION_S46_BR = 90
OPTION_S46_DMR = 91
OPTION_S46_V4V6BIND = 92
OPTION_S46_PORTPARAMS = 93
OPTION_S46_CONT_MAPE = 94
OPTION_S46_CONT_MAPT = 95
OPTION_S46_CONT_LW = 96

class S46RuleOption(Option):
    __doc__ = '\n    :rfc:`7598#section-4.1`\n\n    Figure 1 shows the format of the S46 Rule option (OPTION_S46_RULE)\n    used for conveying the Basic Mapping Rule (BMR) and Forwarding\n    Mapping Rule (FMR).\n\n    This option follows behavior described in Sections 17.1.1 and 18.1.1\n    of [RFC3315]. Clients can send those options, encapsulated in their\n    respective container options, with specific values as hints for the\n    server. See Section 5 for details. Depending on the server\n    configuration and policy, it may accept or ignore the hints. Clients\n    MUST be able to process received values that are different than the\n    hints it sent earlier.\n\n    .. code-block:: none\n\n       0                   1                   2                   3\n       0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      |        OPTION_S46_RULE        |         option-length         |\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      |     flags     |     ea-len    |  prefix4-len  | ipv4-prefix   |\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      |                  (continued)                  |  prefix6-len  |\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      |                           ipv6-prefix                         |\n      |                       (variable length)                       |\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      |                                                               |\n      .                        S46_RULE-options                       .\n      .                                                               .\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n\n                          Figure 1: S46 Rule Option\n\n    option-code\n        OPTION_S46_RULE (89)\n\n    option-length\n        length of the option, excluding option-code and option-length\n        fields, including length of all encapsulated options; expressed\n        in octets.\n\n    flags\n        8 bits long; carries flags applicable to the rule. The meanings of\n        the specific bits are explained in Figure 2.\n\n    ea-len\n        8 bits long; specifies the Embedded Address (EA) bit length.\n        Allowed values range from 0 to 48.\n\n    prefix4-len\n        8 bits long; expresses the prefix length of the Rule IPv4 prefix\n        specified in the ipv4-prefix field. Allowed values range from 0 to 32.\n\n    ipv4-prefix\n        a fixed-length 32-bit field that specifies the IPv4 prefix for the S46\n        rule. The bits in the prefix after prefix4-len number of bits are\n        reserved and MUST be initialized to zero by the sender and ignored by\n        the receiver.\n\n    prefix6-len\n        8 bits long; expresses the length of the Rule IPv6 prefix specified in\n        the ipv6-prefix field. Allowed values range from 0 to 128.\n\n    ipv6-prefix\n        a variable-length field that specifies the IPv6 domain prefix for the\n        S46 rule. The field is padded on the right with zero bits up to the\n        nearest octet boundary when prefix6-len is not evenly divisible by 8.\n\n    S46_RULE-options\n        a variable-length field that may contain zero or more options that\n        specify additional parameters for this S46 rule. This document\n        specifies one such option: OPTION_S46_PORTPARAMS.\n\n\n   The format of the S46 Rule Flags field is:\n\n    .. code-block:: none\n\n           0 1 2 3 4 5 6 7\n          +-+-+-+-+-+-+-+-+\n          |Reserved     |F|\n          +-+-+-+-+-+-+-+-+\n\n      Figure 2: S46 Rule Flags\n\n    Reserved\n        7 bits; reserved for future use as flags.\n\n    F-flag\n        1-bit field that specifies whether the rule is to be used for\n        forwarding (FMR). If set, this rule is used as an FMR; if not set,\n        this rule is a BMR only and MUST NOT be used for forwarding.\n\n        Note: A BMR can also be used as an FMR for forwarding if the F-flag is\n        set. The BMR is determined by a longest-prefix match of the Rule IPv6\n        prefix against the End-user IPv6 prefix(es).\n\n    It is expected that in a typical mesh deployment scenario there will be a\n    single BMR, which could also be designated as an FMR using the F-flag.\n    '
    option_type = OPTION_S46_RULE

    def __init__(self, flags: int=0,
                 ea_len: int=0, ipv4_prefix: IPv4Network=None, ipv6_prefix: IPv6Network=None,
                 options: Iterable[Option]=None):
        self.flags = flags
        self.ea_len = ea_len
        self.ipv4_prefix = ipv4_prefix or IPv4Network('0.0.0.0/0')
        self.ipv6_prefix = ipv6_prefix or IPv6Network('::/0')
        self.options = list(options or [])

    @property
    def fmr(self):
        """
        Extract the F flag

        :return: Whether the F flag is set
        """
        return bool(self.flags & 1)

    @fmr.setter
    def fmr(self, value: bool):
        """
        Set/unset the F flag

        :param value: The new value of the F flag
        """
        if value:
            self.flags |= 1
        else:
            self.flags &= -2

    def validate(self):
        """
        Validate that the contents of this object conform to protocol specs.
        """
        if not isinstance(self.flags, int) or not 0 <= self.flags < 256:
            raise ValueError('Flags must be an unsigned 8 bit integer')
        if not isinstance(self.ea_len, int) or not 0 <= self.ea_len <= 48:
            raise ValueError('EA-len value must be an integer in range from 0 to 48')
        if not isinstance(self.ipv4_prefix, IPv4Network):
            raise ValueError('IPv4 prefix must be an IPv4Network')
        if not isinstance(self.ipv6_prefix, IPv6Network):
            raise ValueError('IPv6 prefix must be an IPv6Network')
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
        my_offset, option_len = self.parse_option_header(buffer, offset, length, min_length=8)
        header_offset = my_offset
        self.flags = buffer[(offset + my_offset)]
        my_offset += 1
        self.ea_len = buffer[(offset + my_offset)]
        my_offset += 1
        ipv4_prefix_length = buffer[(offset + my_offset)]
        my_offset += 1
        if not 0 <= ipv4_prefix_length <= 32:
            raise ValueError('IPv4 prefix length must be in range from 0 to 32')
        ipv4_address = IPv4Address(buffer[offset + my_offset:offset + my_offset + 4])
        my_offset += 4
        self.ipv4_prefix = IPv4Network('{!s}/{:d}'.format(ipv4_address, ipv4_prefix_length), strict=False)
        ipv6_prefix_length = buffer[(offset + my_offset)]
        my_offset += 1
        if not 0 <= ipv6_prefix_length <= 128:
            raise ValueError('IPv6 prefix length must be in range from 0 to 128')
        included_octets = math.ceil(ipv6_prefix_length / 8)
        ipv6_address = IPv6Address(buffer[offset + my_offset:offset + my_offset + included_octets].ljust(16, b'\x00'))
        my_offset += included_octets
        self.ipv6_prefix = IPv6Network('{!s}/{:d}'.format(ipv6_address, ipv6_prefix_length), strict=False)
        self.options = []
        max_offset = option_len + header_offset
        while max_offset > my_offset:
            used_buffer, option = Option.parse(buffer, offset=offset + my_offset)
            self.options.append(option)
            my_offset += used_buffer

        if my_offset != max_offset:
            raise ValueError('Option length does not match the combined length of the parsed options')
        return my_offset

    def save(self) -> Union[(bytes, bytearray)]:
        """
        Save the internal state of this object as a buffer.

        :return: The buffer with the data from this element
        """
        included_octets = math.ceil(self.ipv6_prefix.prefixlen / 8)
        ipv6_address_bytes = self.ipv6_prefix.network_address.packed[:included_octets]
        options_buffer = bytearray()
        for option in self.options:
            options_buffer.extend(option.save())

        buffer = bytearray()
        buffer.extend(pack('!HHBBB', self.option_type, len(options_buffer) + included_octets + 8, self.flags, self.ea_len, self.ipv4_prefix.prefixlen))
        buffer.extend(self.ipv4_prefix.network_address.packed)
        buffer.append(self.ipv6_prefix.prefixlen)
        buffer.extend(ipv6_address_bytes)
        buffer.extend(options_buffer)
        return buffer

    def get_options_of_type(self, *args: Type[SomeOption]) -> List[SomeOption]:
        """
        Get all options that are subclasses of the given class.

        :param args: The classes to look for
        :returns: The list of options
        """
        classes = tuple(args)
        return [option for option in self.options if isinstance(option, classes)]

    def get_option_of_type(self, *args: Type[SomeOption]) -> Optional[SomeOption]:
        """
        Get the first option that is a subclass of the given class.

        :param args: The classes to look for
        :returns: The option or None
        """
        classes = tuple(args)
        for option in self.options:
            if isinstance(option, classes):
                return option


class S46BROption(Option):
    __doc__ = '\n    :rfc:`7598#section-4.2`\n\n    The S46 BR option (OPTION_S46_BR) is used to convey the IPv6 address\n    of the Border Relay. Figure 3 shows the format of the OPTION_S46_BR\n    option.\n\n    .. code-block:: none\n\n       0                   1                   2                   3\n       0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      |         OPTION_S46_BR         |         option-length         |\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      |                      br-ipv6-address                          |\n      |                                                               |\n      |                                                               |\n      |                                                               |\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n\n                           Figure 3: S46 BR Option\n\n    option-code\n        OPTION_S46_BR (90)\n\n    option-length\n        16\n\n    br-ipv6-address\n        a fixed-length field of 16 octets that specifies the IPv6 address for the S46 BR.\n\n    BR redundancy can be implemented by using an anycast address for the\n    BR IPv6 address. Multiple OPTION_S46_BR options MAY be included in\n    the container; this document does not further explore the use of\n    multiple BR IPv6 addresses.\n    '
    option_type = OPTION_S46_BR

    def __init__(self, br_address: IPv6Address=None):
        self.br_address = br_address

    def validate(self):
        """
        Validate that the contents of this object conform to protocol specs.
        """
        if not isinstance(self.br_address, IPv6Address):
            raise ValueError('BR address must be an IPv6Address')

    def load_from(self, buffer: bytes, offset: int=0, length: int=None) -> int:
        """
        Load the internal state of this object from the given buffer. The buffer may contain more data after the
        structured element is parsed. This data is ignored.

        :param buffer: The buffer to read data from
        :param offset: The offset in the buffer where to start reading
        :param length: The amount of data we are allowed to read from the buffer
        :return: The number of bytes used from the buffer
        """
        my_offset, option_len = self.parse_option_header(buffer, offset, length, min_length=16, max_length=16)
        self.br_address = IPv6Address(buffer[offset + my_offset:offset + my_offset + 16])
        my_offset += 16
        return my_offset

    def save(self) -> Union[(bytes, bytearray)]:
        """
        Save the internal state of this object as a buffer.

        :return: The buffer with the data from this element
        """
        buffer = bytearray()
        buffer.extend(pack('!HH', self.option_type, 16))
        buffer.extend(self.br_address.packed)
        return buffer


class S46DMROption(Option):
    __doc__ = '\n    :rfc:`7598#section-4.3`\n\n    The S46 DMR option (OPTION_S46_DMR) is used to convey values for the\n    Default Mapping Rule (DMR). Figure 4 shows the format of the\n    OPTION_S46_DMR option used for conveying a DMR.\n\n    .. code-block:: none\n\n       0                   1                   2                   3\n       0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      |        OPTION_S46_DMR         |         option-length         |\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      |dmr-prefix6-len|            dmr-ipv6-prefix                    |\n      +-+-+-+-+-+-+-+-+           (variable length)                   |\n      .                                                              .\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n\n                          Figure 4: S46 DMR Option\n\n    option-code\n        OPTION_S46_DMR (91)\n\n    option-length\n        1 + length of dmr-ipv6-prefix specified in octets.\n\n    dmr-prefix6-len\n        8 bits long; expresses the bitmask length of the IPv6 prefix specified\n        in the dmr-ipv6-prefix field. Allowed values range from 0 to 128.\n\n    dmr-ipv6-prefix\n        a variable-length field specifying the IPv6 prefix or address for the\n        BR. This field is right-padded with zeros to the nearest octet\n        boundary when dmr-prefix6-len is not divisible by 8.\n    '
    option_type = OPTION_S46_DMR

    def __init__(self, dmr_prefix: IPv6Network=None):
        self.dmr_prefix = dmr_prefix

    def validate(self):
        """
        Validate that the contents of this object conform to protocol specs.
        """
        if not isinstance(self.dmr_prefix, IPv6Network):
            raise ValueError('DMR prefix must be an IPv6Network')

    def load_from(self, buffer: bytes, offset: int=0, length: int=None) -> int:
        """
        Load the internal state of this object from the given buffer. The buffer may contain more data after the
        structured element is parsed. This data is ignored.

        :param buffer: The buffer to read data from
        :param offset: The offset in the buffer where to start reading
        :param length: The amount of data we are allowed to read from the buffer
        :return: The number of bytes used from the buffer
        """
        my_offset, option_len = self.parse_option_header(buffer, offset, length, min_length=1, max_length=17)
        header_offset = my_offset
        ipv6_prefix_length = buffer[(offset + my_offset)]
        my_offset += 1
        if not 0 <= ipv6_prefix_length <= 128:
            raise ValueError('IPv6 prefix length must be in range from 0 to 128')
        included_octets = math.ceil(ipv6_prefix_length / 8)
        ipv6_address = IPv6Address(buffer[offset + my_offset:offset + my_offset + included_octets].ljust(16, b'\x00'))
        my_offset += included_octets
        self.dmr_prefix = IPv6Network('{!s}/{:d}'.format(ipv6_address, ipv6_prefix_length), strict=False)
        max_offset = option_len + header_offset
        if my_offset != max_offset:
            raise ValueError('Option length does not match the combined length of the parsed options')
        return my_offset

    def save(self) -> Union[(bytes, bytearray)]:
        """
        Save the internal state of this object as a buffer.

        :return: The buffer with the data from this element
        """
        included_octets = math.ceil(self.dmr_prefix.prefixlen / 8)
        ipv6_address_bytes = self.dmr_prefix.network_address.packed[:included_octets]
        buffer = bytearray()
        buffer.extend(pack('!HHB', self.option_type, 1 + included_octets, self.dmr_prefix.prefixlen))
        buffer.extend(ipv6_address_bytes)
        return buffer


class S46V4V6BindingOption(Option):
    __doc__ = '\n    :rfc:`7598#section-4.4`\n\n    The S46 IPv4/IPv6 Address Binding option (OPTION_S46_V4V6BIND) MAY be\n    used to specify the full or shared IPv4 address of the CE. The IPv6\n    prefix field is used by the CE to identify the correct prefix to use\n    for the tunnel source.\n\n    .. code-block:: none\n\n       0                   1                   2                   3\n       0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      |      OPTION_S46_V4V6BIND      |         option-length         |\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      |                         ipv4-address                          |\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      |bindprefix6-len|             bind-ipv6-prefix                  |\n      +-+-+-+-+-+-+-+-+             (variable length)                 |\n      .                                                               .\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      |                                                               |\n      .                      S46_V4V6BIND-options                     .\n      .                                                               .\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n\n               Figure 5: S46 IPv4/IPv6 Address Binding Option\n\n    option-code\n        OPTION_S46_V4V6BIND (92)\n\n    option-length\n        length of the option, excluding option-code and option-length fields,\n        including length of all encapsulated options; expressed in octets.\n\n    ipv4-address\n        a fixed-length field of 4 octets specifying an IPv4 address.\n\n    bindprefix6-len\n        8 bits long; expresses the bitmask length of the IPv6 prefix specified\n        in the bind-ipv6-prefix field. Allowed values range from 0 to 128.\n\n    bind-ipv6-prefix\n        a variable-length field specifying the IPv6 prefix or address for the\n        S46 CE. This field is right-padded with zeros to the nearest octet\n        boundary when bindprefix6-len is not divisible by 8.\n\n    S46_V4V6BIND-options\n        a variable-length field that may contain zero or more options that\n        specify additional parameters. This document specifies one such\n        option: OPTION_S46_PORTPARAMS.\n    '
    option_type = OPTION_S46_V4V6BIND

    def __init__(self, ipv4_address: IPv4Address=None,
                 ipv6_prefix: IPv6Network=None, options: Iterable[Option]=None):
        self.ipv4_address = ipv4_address or IPv4Address('0.0.0.0')
        self.ipv6_prefix = ipv6_prefix or IPv6Network('::/0')
        self.options = list(options or [])

    def validate(self):
        """
        Validate that the contents of this object conform to protocol specs.
        """
        if not isinstance(self.ipv4_address, IPv4Address):
            raise ValueError('IPv4 address must be an IPv4Address')
        if not isinstance(self.ipv6_prefix, IPv6Network):
            raise ValueError('IPv6 prefix must be an IPv6Network')
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
        my_offset, option_len = self.parse_option_header(buffer, offset, length, min_length=5)
        header_offset = my_offset
        self.ipv4_address = IPv4Address(buffer[offset + my_offset:offset + my_offset + 4])
        my_offset += 4
        ipv6_prefix_length = buffer[(offset + my_offset)]
        my_offset += 1
        if not 0 <= ipv6_prefix_length <= 128:
            raise ValueError('IPv6 prefix length must be in range from 0 to 128')
        included_octets = math.ceil(ipv6_prefix_length / 8)
        ipv6_address = IPv6Address(buffer[offset + my_offset:offset + my_offset + included_octets].ljust(16, b'\x00'))
        my_offset += included_octets
        self.ipv6_prefix = IPv6Network('{!s}/{:d}'.format(ipv6_address, ipv6_prefix_length), strict=False)
        self.options = []
        max_offset = option_len + header_offset
        while max_offset > my_offset:
            used_buffer, option = Option.parse(buffer, offset=offset + my_offset)
            self.options.append(option)
            my_offset += used_buffer

        if my_offset != max_offset:
            raise ValueError('Option length does not match the combined length of the parsed options')
        return my_offset

    def save(self) -> Union[(bytes, bytearray)]:
        """
        Save the internal state of this object as a buffer.

        :return: The buffer with the data from this element
        """
        included_octets = math.ceil(self.ipv6_prefix.prefixlen / 8)
        ipv6_address_bytes = self.ipv6_prefix.network_address.packed[:included_octets]
        options_buffer = bytearray()
        for option in self.options:
            options_buffer.extend(option.save())

        buffer = bytearray()
        buffer.extend(pack('!HH', self.option_type, len(options_buffer) + included_octets + 5))
        buffer.extend(self.ipv4_address.packed)
        buffer.append(self.ipv6_prefix.prefixlen)
        buffer.extend(ipv6_address_bytes)
        buffer.extend(options_buffer)
        return buffer

    def get_options_of_type(self, *args: Type[SomeOption]) -> List[SomeOption]:
        """
        Get all options that are subclasses of the given class.

        :param args: The classes to look for
        :returns: The list of options
        """
        classes = tuple(args)
        return [option for option in self.options if isinstance(option, classes)]

    def get_option_of_type(self, *args: Type[SomeOption]) -> Optional[SomeOption]:
        """
        Get the first option that is a subclass of the given class.

        :param args: The classes to look for
        :returns: The option or None
        """
        classes = tuple(args)
        for option in self.options:
            if isinstance(option, classes):
                return option


class S46PortParametersOption(Option):
    __doc__ = "\n    :rfc:`7598#section-4.5`\n\n    The S46 Port Parameters option (OPTION_S46_PORTPARAMS) specifies\n    optional port set information that MAY be provided to CEs.\n\n    See Section 5.1 of [RFC7597] for a description of the MAP algorithm\n    and detailed explanation of all of the parameters.\n\n    .. code-block:: none\n\n       0                   1                   2                   3\n       0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      |     OPTION_S46_PORTPARAMS     |         option-length         |\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      |    offset     |   PSID-len    |             PSID              |\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n\n                    Figure 6: S46 Port Parameters Option\n\n    option-code\n        OPTION_S46_PORTPARAMS (93)\n\n    option-length\n        4\n\n    offset\n        Port Set Identifier (PSID) offset. 8 bits long; specifies the numeric\n        value for the S46 algorithm's excluded port range/offset bits\n        (a-bits), as per Section 5.1 of [RFC7597]. Allowed values are between\n        0 and 15. Default values for this field are specific to the softwire\n        mechanism being implemented and are defined in the relevant\n        specification document.\n\n    PSID-len\n        8 bits long; specifies the number of significant bits in the PSID\n        field (also known as 'k'). When set to 0, the PSID field is to be\n        ignored. After the first 'a' bits, there are k bits in the port\n        number representing the value of the PSID. Consequently, the\n        address-sharing ratio would be 2^k.\n\n    PSID\n        16 bits long. The PSID value algorithmically identifies a set of\n        ports assigned to a CE. The first k bits on the left of this field\n        contain the PSID binary value. The remaining (16 - k) bits on the\n        right are padding zeros.\n\n    When receiving the OPTION_S46_PORTPARAMS option with an explicit\n    PSID, the client MUST use this explicit PSID when configuring its\n    softwire interface. The OPTION_S46_PORTPARAMS option with an\n    explicit PSID MUST be discarded if the S46 CE isn't configured with a\n    full IPv4 address (e.g., IPv4 prefix).\n\n    The OPTION_S46_PORTPARAMS option is contained within an\n    OPTION_S46_RULE option or an OPTION_S46_V4V6BIND option.\n    "
    option_type = OPTION_S46_PORTPARAMS

    def __init__(self, offset: int=0,
                 psid_len: int=0, psid: int=0):
        self.offset = offset
        self.psid_len = psid_len
        self.psid = psid

    def validate(self):
        """
        Validate that the contents of this object conform to protocol specs.
        """
        if not isinstance(self.offset, int) or not 0 <= self.offset <= 15:
            raise ValueError('Offset must be an unsigned 4 bit integer')
        if not isinstance(self.psid_len, int) or not 0 <= self.psid_len <= 16:
            raise ValueError('PSID length must be an integer in range from 0 to 16')
        if self.offset + self.psid_len > 16:
            raise ValueError('Offset and PSID length together must be 16 or less')
        if not isinstance(self.psid, int) or not 0 <= self.psid < 2 ** self.psid_len:
            raise ValueError('PSID must be an unsigned {} bit integer'.format(self.psid_len))

    def load_from(self, buffer: bytes, offset: int=0, length: int=None) -> int:
        """
        Load the internal state of this object from the given buffer. The buffer may contain more data after the
        structured element is parsed. This data is ignored.

        :param buffer: The buffer to read data from
        :param offset: The offset in the buffer where to start reading
        :param length: The amount of data we are allowed to read from the buffer
        :return: The number of bytes used from the buffer
        """
        my_offset, option_len = self.parse_option_header(buffer, offset, length, min_length=4, max_length=4)
        self.offset, self.psid_len, raw_psid = unpack('!BBH', buffer[offset + my_offset:offset + my_offset + 4])
        my_offset += 4
        self.psid = raw_psid >> 16 - self.psid_len
        return my_offset

    def save(self) -> Union[(bytes, bytearray)]:
        """
        Save the internal state of this object as a buffer.

        :return: The buffer with the data from this element
        """
        raw_psid = self.psid << 16 - self.psid_len
        buffer = bytearray()
        buffer.extend(pack('!HHBBH', self.option_type, 4, self.offset, self.psid_len, raw_psid))
        return buffer


class S46ContainerOption(Option):
    __doc__ = '\n    Common code for MAP-E, MAP-T and LW4over6 containers\n    '
    option_type = 0

    def __init__(self, options: Iterable[Option]=None):
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
        my_offset, option_len = self.parse_option_header(buffer, offset, length, min_length=5)
        self.options = []
        max_offset = option_len + my_offset
        while max_offset > my_offset:
            used_buffer, option = Option.parse(buffer, offset=offset + my_offset)
            self.options.append(option)
            my_offset += used_buffer

        if my_offset != max_offset:
            raise ValueError('Option length does not match the combined length of the parsed options')
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

    def get_options_of_type(self, *args: Type[SomeOption]) -> List[SomeOption]:
        """
        Get all options that are subclasses of the given class.

        :param args: The classes to look for
        :returns: The list of options
        """
        classes = tuple(args)
        return [option for option in self.options if isinstance(option, classes)]

    def get_option_of_type(self, *args: Type[SomeOption]) -> Optional[SomeOption]:
        """
        Get the first option that is a subclass of the given class.

        :param args: The classes to look for
        :returns: The option or None
        """
        classes = tuple(args)
        for option in self.options:
            if isinstance(option, classes):
                return option


class S46MapEContainerOption(S46ContainerOption):
    __doc__ = '\n    :rfc:`7598#section-5.1`\n\n    The S46 MAP-E Container option (OPTION_S46_CONT_MAPE) specifies the\n    container used to group all rules and optional port parameters for a\n    specified domain.\n\n    .. code-block:: none\n\n       0                   1                   2                   3\n       0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      |        OPTION_S46_CONT_MAPE   |         option-length         |\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      |                                                               |\n      .            encapsulated-options (variable length)             .\n      .                                                               .\n      +---------------------------------------------------------------+\n\n                    Figure 7: S46 MAP-E Container Option\n\n    option-code\n        OPTION_S46_CONT_MAPE (94)\n\n    option-length\n        length of encapsulated options, expressed in octets.\n\n    encapsulated-options\n        options associated with this Softwire46 MAP-E domain.\n\n    The encapsulated-options field conveys options specific to the\n    OPTION_S46_CONT_MAPE option. Currently, there are two encapsulated\n    options specified: OPTION_S46_RULE and OPTION_S46_BR. There MUST be\n    at least one OPTION_S46_RULE option and at least one OPTION_S46_BR\n    option.\n\n    Other options applicable to a domain may be defined in the future. A\n    DHCPv6 message MAY include multiple OPTION_S46_CONT_MAPE options\n    (representing multiple domains).\n    '
    option_type = OPTION_S46_CONT_MAPE


class S46MapTContainerOption(S46ContainerOption):
    __doc__ = '\n    :rfc:`7598#section-5.2`\n\n    The S46 MAP-T Container option (OPTION_S46_CONT_MAPT) specifies the\n    container used to group all rules and optional port parameters for a\n    specified domain.\n\n    .. code-block:: none\n\n       0                   1                   2                   3\n       0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      |     OPTION_S46_CONT_MAPT      |         option-length         |\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      |                                                               |\n      .            encapsulated-options (variable length)             .\n      .                                                               .\n      +---------------------------------------------------------------+\n\n                    Figure 8: S46 MAP-T Container Option\n\n    option-code\n        OPTION_S46_CONT_MAPT (95)\n\n    option-length\n        length of encapsulated options, expressed in octets.\n\n    encapsulated-options\n        options associated with this Softwire46 MAP-T domain.\n\n    The encapsulated-options field conveys options specific to the\n    OPTION_S46_CONT_MAPT option. Currently, there are two options\n    specified: the OPTION_S46_RULE and OPTION_S46_DMR options. There\n    MUST be at least one OPTION_S46_RULE option and exactly one\n    OPTION_S46_DMR option.\n    '
    option_type = OPTION_S46_CONT_MAPT


class S46LWContainerOption(S46ContainerOption):
    __doc__ = '\n    :rfc:`7598#section-5.3`\n\n    The S46 Lightweight 4over6 Container option (OPTION_S46_CONT_LW)\n    specifies the container used to group all rules and optional port\n    parameters for a specified domain.\n\n    .. code-block:: none\n\n       0                   1                   2                   3\n       0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      |      OPTION_S46_CONT_LW       |         option-length         |\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      |                                                               |\n      +            encapsulated-options (variable length)             .\n      .                                                               .\n      +---------------------------------------------------------------+\n\n              Figure 9: S46 Lightweight 4over6 Container Option\n\n    option-code\n        OPTION_S46_CONT_LW (96)\n\n    option-length\n        length of encapsulated options, expressed in octets.\n\n    encapsulated-options\n        options associated with this Softwire46 Lightweight 4over6 domain.\n\n    The encapsulated-options field conveys options specific to the\n    OPTION_S46_CONT_LW option. Currently, there are two options\n    specified: OPTION_S46_V4V6BIND and OPTION_S46_BR. There MUST be at\n    most one OPTION_S46_V4V6BIND option and at least one OPTION_S46_BR\n    option.\n    '
    option_type = OPTION_S46_CONT_LW


SolicitMessage.add_may_contain(S46ContainerOption)
AdvertiseMessage.add_may_contain(S46ContainerOption)
RequestMessage.add_may_contain(S46ContainerOption)
ConfirmMessage.add_may_contain(S46ContainerOption)
RenewMessage.add_may_contain(S46ContainerOption)
RebindMessage.add_may_contain(S46ContainerOption)
ReleaseMessage.add_may_contain(S46ContainerOption)
ReplyMessage.add_may_contain(S46ContainerOption)
S46RuleOption.add_may_contain(S46PortParametersOption)
S46V4V6BindingOption.add_may_contain(S46PortParametersOption)
S46MapEContainerOption.add_may_contain(S46RuleOption, min_occurrence=1)
S46MapEContainerOption.add_may_contain(S46BROption, min_occurrence=1)
S46MapEContainerOption.add_may_contain(S46PortParametersOption)
S46MapTContainerOption.add_may_contain(S46RuleOption, min_occurrence=1)
S46MapTContainerOption.add_may_contain(S46DMROption, min_occurrence=1, max_occurrence=1)
S46MapTContainerOption.add_may_contain(S46PortParametersOption)
S46LWContainerOption.add_may_contain(S46V4V6BindingOption, min_occurrence=0, max_occurrence=1)
S46LWContainerOption.add_may_contain(S46BROption, min_occurrence=1)
S46LWContainerOption.add_may_contain(S46PortParametersOption)