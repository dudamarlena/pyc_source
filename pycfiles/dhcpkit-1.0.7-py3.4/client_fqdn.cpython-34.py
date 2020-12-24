# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/ipv6/extensions/client_fqdn.py
# Compiled at: 2017-06-23 17:21:00
# Size of source mod 2**32: 8973 bytes
"""
Implementation of the Client FQDN option as specified in :rfc:`4704`.
"""
from struct import pack
from dhcpkit.ipv6.messages import AdvertiseMessage, RebindMessage, RenewMessage, ReplyMessage, RequestMessage, SolicitMessage
from dhcpkit.ipv6.options import Option
from dhcpkit.utils import encode_domain, parse_domain_bytes
from typing import Union
OPTION_CLIENT_FQDN = 39

class ClientFQDNOption(Option):
    __doc__ = '\n    To update the IPv6-address-to-FQDN mapping, a DHCPv6 server needs to\n    know the FQDN of the client for the addresses for the client\'s IA_NA\n    bindings.  To allow the client to convey its FQDN to the server, this\n    document defines a new DHCPv6 option called "Client FQDN".  The\n    Client FQDN option also contains Flags that DHCPv6 clients and\n    servers use to negotiate who does which updates.\n\n    The code for this option is 39.  Its minimum length is 1 octet.\n\n    The format of the DHCPv6 Client FQDN option is shown below::\n\n        0                   1                   2                   3\n        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1\n       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n       |          OPTION_FQDN          |         option-len            |\n       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n       |   flags       |                                               |\n       +-+-+-+-+-+-+-+-+                                               |\n       .                                                               .\n       .                          domain-name                          .\n       .                                                               .\n       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n\n    option-code\n        OPTION_CLIENT_FQDN (39).\n\n    option-len\n        1 + length of domain name.\n\n    flags\n        flag bits used between client and server to negotiate who performs which updates.\n\n    domain-name\n        the partial or fully qualified domain name (with length option-len - 1).\n\n    The Client FQDN option MUST only appear in a message\'s options field\n    and applies to all addresses for all IA_NA bindings in the\n    transaction.\n\n    4.1.  The Flags Field\n\n    The format of the Flags field is::\n\n        0 1 2 3 4 5 6 7\n       +-+-+-+-+-+-+-+-+\n       |  MBZ    |N|O|S|\n       +-+-+-+-+-+-+-+-+\n\n    The "S" bit indicates whether the server SHOULD or SHOULD NOT perform\n    the AAAA RR (FQDN-to-address) DNS updates.  A client sets the bit to\n    0 to indicate that the server SHOULD NOT perform the updates and 1 to\n    indicate that the server SHOULD perform the updates.  The state of\n    the bit in the reply from the server indicates the action to be taken\n    by the server; if it is 1, the server has taken responsibility for\n    AAAA RR updates for the FQDN.\n\n    The "O" bit indicates whether the server has overridden the client\'s\n    preference for the "S" bit.  A client MUST set this bit to 0.  A\n    server MUST set this bit to 1 if the "S" bit in its reply to the\n    client does not match the "S" bit received from the client.\n\n    The "N" bit indicates whether the server SHOULD NOT perform any DNS\n    updates.  A client sets this bit to 0 to request that the server\n    SHOULD perform updates (the PTR RR and possibly the AAAA RR based on\n    the "S" bit) or to 1 to request that the server SHOULD NOT perform\n    any DNS updates.  A server sets the "N" bit to indicate whether the\n    server SHALL (0) or SHALL NOT (1) perform DNS updates.  If the "N"\n    bit is 1, the "S" bit MUST be 0.\n\n    The remaining bits in the Flags field are reserved for future\n    assignment.  DHCPv6 clients and servers that send the Client FQDN\n    option MUST clear the MBZ bits, and they MUST ignore these bits.\n\n    4.2.  The Domain Name Field\n\n    The Domain Name part of the option carries all or part of the FQDN of\n    a DHCPv6 client.  The data in the Domain Name field MUST be encoded\n    as described in Section 8 of [5].  In order to determine whether the\n    FQDN has changed between message exchanges, the client and server\n    MUST NOT alter the Domain Name field contents unless the FQDN has\n    actually changed.\n\n    A client MAY be configured with a fully qualified domain name or with\n    a partial name that is not fully qualified.  If a client knows only\n    part of its name, it MAY send a name that is not fully qualified,\n    indicating that it knows part of the name but does not necessarily\n    know the zone in which the name is to be embedded.\n\n    To send a fully qualified domain name, the Domain Name field is set\n    to the DNS-encoded domain name including the terminating zero-length\n    label.  To send a partial name, the Domain Name field is set to the\n    DNS-encoded domain name without the terminating zero-length label.\n\n    A client MAY also leave the Domain Name field empty if it desires the\n    server to provide a name.\n\n    Servers SHOULD send the complete fully qualified domain name in\n    Client FQDN options.\n    '
    option_type = OPTION_CLIENT_FQDN

    def __init__(self, flags: int=0,
                 domain_name: str=None):
        self.flags = flags
        self.domain_name = domain_name

    @property
    def server_aaaa_update(self):
        """
        Extract the S flag

        :return: Whether the S flag is set
        """
        return bool(self.flags & 1)

    @server_aaaa_update.setter
    def server_aaaa_update(self, value: bool):
        """
        Set/unset the S flag

        :param value: The new value of the S flag
        """
        if value:
            self.flags |= 1
        else:
            self.flags &= -2

    @property
    def server_aaaa_override(self):
        """
        Extract the O flag

        :return: Whether the O flag is set
        """
        return bool(self.flags & 2)

    @server_aaaa_override.setter
    def server_aaaa_override(self, value: bool):
        """
        Set/unset the O flag

        :param value: The new value of the O flag
        """
        if value:
            self.flags |= 2
        else:
            self.flags &= -3

    @property
    def no_server_dns_update(self):
        """
        Extract the N flag

        :return: Whether the N flag is set
        """
        return bool(self.flags & 4)

    @no_server_dns_update.setter
    def no_server_dns_update(self, value: bool):
        """
        Set/unset the N flag

        :param value: The new value of the N flag
        """
        if value:
            self.flags |= 4
        else:
            self.flags &= -5

    def validate(self):
        """
        Validate that the contents of this object conform to protocol specs.
        """
        if self.domain_name:
            encode_domain(self.domain_name, allow_relative=True)

    def load_from(self, buffer: bytes, offset: int=0, length: int=None) -> int:
        """
        Load the internal state of this object from the given buffer. The buffer may
        contain more data after the structured element is parsed. This data is ignored.

        :param buffer: The buffer to read data from
        :param offset: The offset in the buffer where to start reading
        :param length: The amount of data we are allowed to read from the buffer
        :return: The number of bytes used from the buffer
        """
        my_offset, option_len = self.parse_option_header(buffer, offset, length)
        header_offset = my_offset
        self.flags = buffer[(offset + my_offset)]
        my_offset += 1
        max_offset = option_len + header_offset
        domain_name_len, self.domain_name = parse_domain_bytes(buffer, offset=offset + my_offset, length=option_len - 1, allow_relative=True)
        my_offset += domain_name_len
        if my_offset != max_offset:
            raise ValueError('Option length does not match the combined length of the included domain name')
        return my_offset

    def save(self) -> Union[(bytes, bytearray)]:
        """
        Save the internal state of this object as a buffer.

        :return: The buffer with the data from this element
        """
        domain_buffer = encode_domain(self.domain_name)
        buffer = bytearray()
        buffer.extend(pack('!HHB', self.option_type, 1 + len(domain_buffer), self.flags))
        buffer.extend(domain_buffer)
        return buffer


SolicitMessage.add_may_contain(ClientFQDNOption, 0, 1)
AdvertiseMessage.add_may_contain(ClientFQDNOption, 0, 1)
RequestMessage.add_may_contain(ClientFQDNOption, 0, 1)
RenewMessage.add_may_contain(ClientFQDNOption, 0, 1)
RebindMessage.add_may_contain(ClientFQDNOption, 0, 1)
ReplyMessage.add_may_contain(ClientFQDNOption, 0, 1)