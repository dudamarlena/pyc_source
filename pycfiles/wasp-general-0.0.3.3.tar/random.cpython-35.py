# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/crypto/random.py
# Compiled at: 2017-04-24 15:57:13
# Size of source mod 2**32: 2258 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
from Crypto.Random.random import getrandbits
import math
from wasp_general.verify import verify_type, verify_value

@verify_type(bits_count=int)
@verify_value(bits_count=lambda x: x >= 0)
def random_bits(bits_count):
    """ Random generator (PyCrypto getrandbits wrapper). The result is a non-negative value.

        :param bits_count: random bits to generate
        :return: int
        """
    return getrandbits(bits_count)


@verify_type(maximum_value=int)
@verify_value(maximum_value=lambda x: x >= 0)
def random_int(maximum_value):
    """ Random generator (PyCrypto getrandbits wrapper). The result is a non-negative value.

        :param maximum_value: maximum integer value
        :return: int
        """
    if maximum_value == 0:
        return 0
    if maximum_value == 1:
        return random_bits(1)
    bits = math.floor(math.log2(maximum_value))
    result = random_bits(bits) + random_int(maximum_value - (2 ** bits - 1))
    return result


@verify_type(bytes_count=int)
@verify_value(bytes_count=lambda x: x >= 0)
def random_bytes(bytes_count):
    """ Generate random bytes sequence. (PyCrypto getrandbits wrapper)

        :param bytes_count: sequence length
        :return: bytes
        """
    return bytes([getrandbits(8) for x in range(bytes_count)])