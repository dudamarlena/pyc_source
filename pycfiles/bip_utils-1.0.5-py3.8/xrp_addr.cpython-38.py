# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\bip_utils\xrp_addr.py
# Compiled at: 2020-04-28 06:22:06
# Size of source mod 2**32: 1800 bytes
from . import utils
from .base58 import Base58Alphabets
from .bip_coin_conf import RippleConf
from .P2PKH import P2PKH

class XrpAddr:
    __doc__ = ' Ripple address class. It allows the Ripple address generation. '

    @staticmethod
    def ToAddress(pub_key_bytes):
        """ Get address in Ripple format.

        Args:
            pub_key_bytes (bytes): Public key bytes

        Returns:
            str: Address string

        Raises:
            ValueError: If key is not a public compressed key
        """
        return P2PKH.ToAddress(pub_key_bytes, RippleConf.P2PKH_NET_VER.Main(), Base58Alphabets.RIPPLE)