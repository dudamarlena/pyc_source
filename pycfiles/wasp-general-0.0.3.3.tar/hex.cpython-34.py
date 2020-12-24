# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/crypto/hex.py
# Compiled at: 2017-04-24 15:57:07
# Size of source mod 2**32: 1930 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
from binascii import hexlify, unhexlify
from wasp_general.verify import verify_type

class WHex:
    __doc__ = ' binascii.hexlify wrapper. Converts bytes to hex-string\n\t'

    @verify_type(byte_sequence=bytes)
    def __init__(self, byte_sequence):
        """ Create converter

                :param byte_sequence: sequence to convert
                """
        self._WHex__byte_sequence = byte_sequence

    def __str__(self):
        """ Return result of converting the sequence

                :return: str
                """
        return hexlify(self._WHex__byte_sequence).decode('ascii')


class WUnHex:
    __doc__ = ' binascii.unhexlify wrapper. Converts string to bytes\n\t'

    @verify_type(string=(str, bytes))
    def __init__(self, string):
        """ Create converter

                :param string: hex-string to convert
                """
        self._WUnHex__string = string

    def __bytes__(self):
        """ Return result of converting the hex-string

                :return: bytes
                """
        return unhexlify(self._WUnHex__string)