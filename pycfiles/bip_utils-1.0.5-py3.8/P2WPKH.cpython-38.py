# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\bip_utils\P2WPKH.py
# Compiled at: 2020-04-16 10:28:35
# Size of source mod 2**32: 2416 bytes
import binascii
from . import utils
from .bech32 import Bech32Encoder
from .bip_coin_conf import BitcoinConf
from .key_helper import KeyHelper

class P2WPKHConst:
    __doc__ = ' Class container for P2WPKH constants. '
    WITNESS_VER = 0


class P2WPKH:
    __doc__ = ' P2WPKH class. It allows the Pay-to-Witness-Public-Key-Hash address generation.\n    Refer to:\n    https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki\n    https://github.com/bitcoin/bips/blob/master/bip-0173.mediawiki\n    '

    @staticmethod
    def ToAddress(pub_key_bytes, net_addr_ver=BitcoinConf.P2WPKH_NET_VER.Main()):
        """ Get address in P2WPKH format.

        Args:
            pub_key_bytes (bytes)         : Public key bytes
            net_addr_ver (bytes, optional): Net address version, default is Bitcoin main network

        Returns:
            str: Address string

        Raises:
            ValueError: If key is not a public compressed key
        """
        if not KeyHelper.IsPublicCompressed(pub_key_bytes):
            raise ValueError('Public compressed key is required for P2WPKH')
        return Bech32Encoder.EncodeAddr(net_addr_ver, P2WPKHConst.WITNESS_VER, utils.Hash160(pub_key_bytes))