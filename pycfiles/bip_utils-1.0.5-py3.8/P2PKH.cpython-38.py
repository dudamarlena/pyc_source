# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\bip_utils\P2PKH.py
# Compiled at: 2020-04-28 06:19:11
# Size of source mod 2**32: 2217 bytes
from . import utils
from .base58 import Base58Encoder, Base58Alphabets
from .bip_coin_conf import BitcoinConf
from .key_helper import KeyHelper

class P2PKH:
    __doc__ = ' P2PKH class. It allows the Pay-to-Public-Key-Hash address generation. '

    @staticmethod
    def ToAddress(pub_key_bytes, net_addr_ver=BitcoinConf.P2PKH_NET_VER.Main(), base58_alph=Base58Alphabets.BITCOIN):
        """ Get address in P2PKH format.

        Args:
            pub_key_bytes (bytes)                  : Public key bytes
            net_addr_ver (bytes, optional)         : Net address version, default is Bitcoin main network
            base58_alph (Base58Alphabets, optional): Base58 alphabet, Bitcoin by default

        Returns:
            str: Address string

        Raises:
            ValueError: If the key is not a public compressed key
        """
        if not KeyHelper.IsPublicCompressed(pub_key_bytes):
            raise ValueError('Public compressed key is required for P2PKH')
        return Base58Encoder.CheckEncode(net_addr_ver + utils.Hash160(pub_key_bytes), base58_alph)