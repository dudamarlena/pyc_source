# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/ipv6/extensions/dslite.py
# Compiled at: 2017-06-08 10:49:31
# Size of source mod 2**32: 4422 bytes
"""
Implementation of DS-Lite AFTR Name option as specified in :rfc:`6334`.
"""
from struct import pack
from typing import Union
from dhcpkit.ipv6.messages import AdvertiseMessage, InformationRequestMessage, RebindMessage, RenewMessage, ReplyMessage, RequestMessage, SolicitMessage
from dhcpkit.ipv6.options import Option
from dhcpkit.utils import encode_domain, parse_domain_bytes
OPTION_AFTR_NAME = 64

class AFTRNameOption(Option):
    __doc__ = '\n    :rfc:`6334#section-3`\n\n    The AFTR-Name option consists of option-code and option-len fields\n    (as all DHCPv6 options have), and a variable-length tunnel-endpoint-\n    name field containing a fully qualified domain name that refers to\n    the AFTR to which the client MAY connect.\n\n    The AFTR-Name option SHOULD NOT appear in any DHCPv6 messages other\n    than the following: Solicit, Advertise, Request, Renew, Rebind,\n    Information-Request, and Reply.\n\n    The format of the AFTR-Name option is shown in the following figure:\n\n    .. code-block:: none\n\n       0                   1                   2                   3\n       0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1\n      +-------------------------------+-------------------------------+\n      |    OPTION_AFTR_NAME: 64       |          option-len           |\n      +-------------------------------+-------------------------------+\n      |                                                               |\n      |                  tunnel-endpoint-name (FQDN)                  |\n      |                                                               |\n      +---------------------------------------------------------------+\n\n    OPTION_AFTR_NAME\n        64\n\n    option-len\n        Length of the tunnel-endpoint-name field in octets.\n\n    tunnel-endpoint-name\n        A fully qualified domain name of the AFTR tunnel endpoint.\n\n    :type fqdn: str\n    '
    option_type = OPTION_AFTR_NAME

    def __init__(self, fqdn: str=''):
        self.fqdn = fqdn

    def validate(self):
        """
        Validate that the contents of this object conform to protocol specs.
        """
        if not isinstance(self.fqdn, str):
            raise ValueError('Tunnel endpoint name must be a string')
        fqdn = encode_domain(self.fqdn)
        if len(fqdn) < 4:
            raise ValueError('The FQDN of the tunnel endpoint is too short')

    def load_from(self, buffer: bytes, offset: int=0, length: int=None) -> int:
        """
        Load the internal state of this object from the given buffer. The buffer may contain more data after the
        structured element is parsed. This data is ignored.

        :param buffer: The buffer to read data from
        :param offset: The offset in the buffer where to start reading
        :param length: The amount of data we are allowed to read from the buffer
        :return: The number of bytes used from the buffer
        """
        my_offset, option_len = self.parse_option_header(buffer, offset, length, min_length=4)
        header_offset = my_offset
        max_offset = option_len + header_offset
        name_len, self.fqdn = parse_domain_bytes(buffer, offset=offset + my_offset, length=option_len)
        my_offset += name_len
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
        buffer.extend(pack('!HH', self.option_type, len(fqdn_buffer)))
        buffer.extend(fqdn_buffer)
        return buffer


SolicitMessage.add_may_contain(AFTRNameOption, 0, 1)
AdvertiseMessage.add_may_contain(AFTRNameOption, 0, 1)
RequestMessage.add_may_contain(AFTRNameOption, 0, 1)
RenewMessage.add_may_contain(AFTRNameOption, 0, 1)
RebindMessage.add_may_contain(AFTRNameOption, 0, 1)
InformationRequestMessage.add_may_contain(AFTRNameOption, 0, 1)
ReplyMessage.add_may_contain(AFTRNameOption, 0, 1)