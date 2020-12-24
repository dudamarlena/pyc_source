# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit_technicolor/options.py
# Compiled at: 2016-08-04 05:52:10
# Size of source mod 2**32: 3286 bytes
"""
Implementation of SOL-MAX-RT using the Technicolor-specific option ID
"""
from struct import unpack_from, pack
from dhcpkit.ipv6.messages import AdvertiseMessage, ReplyMessage
from dhcpkit.ipv6.options import Option
OPTION_SOL_MAX_RT_TECHNICOLOR = 65279

class SolMaxRTTechnicolorOption(Option):
    __doc__ = '\n    :rfc:`7083#section-4`\n\n    A DHCPv6 server sends the SOL_MAX_RT option to a client to override\n    the default value of SOL_MAX_RT.  The value of SOL_MAX_RT in the\n    option replaces the default value defined in Section 3.  One use for\n    the SOL_MAX_RT option is to set a longer value for SOL_MAX_RT, which\n    reduces the Solicit traffic from a client that has not received a\n    response to its Solicit messages.\n\n    The format of the SOL_MAX_RT option is::\n\n       0                   1                   2                   3\n       0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      |          option-code          |         option-len            |\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n      |                       SOL_MAX_RT value                        |\n      +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n\n    option-code\n        OPTION_SOL_MAX_RT Technicolor version (65279).\n\n    option-len\n        4.\n\n    SOL_MAX_RT value\n        Overriding value for SOL_MAX_RT in seconds; MUST be in range: 60 <= "value" <= 86400 (1 day).\n\n    :type sol_max_rt: int\n    '
    option_type = OPTION_SOL_MAX_RT_TECHNICOLOR

    def __init__(self, sol_max_rt: int=0):
        self.sol_max_rt = sol_max_rt

    def validate(self):
        """
        Validate that the contents of this object conform to protocol specs.
        """
        if not isinstance(self.sol_max_rt, int) or not 0 <= self.sol_max_rt < 4294967296:
            raise ValueError('SOL_MAX_RT must be an unsigned 32 bit integer')

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
        if option_len != 4:
            raise ValueError('SOL_MAX_RT Options must have length 4')
        self.sol_max_rt = unpack_from('!I', buffer, offset=offset + my_offset)[0]
        my_offset += 4
        self.validate()
        return my_offset

    def save(self) -> bytes:
        """
        Save the internal state of this object as a buffer.

        :return: The buffer with the data from this element
        """
        self.validate()
        return pack('!HHI', self.option_type, 4, self.sol_max_rt)


AdvertiseMessage.add_may_contain(SolMaxRTTechnicolorOption)
ReplyMessage.add_may_contain(SolMaxRTTechnicolorOption)