# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\bip_utils\P2SH.py
# Compiled at: 2020-04-16 10:27:13
# Size of source mod 2**32: 2530 bytes
import binascii
from . import utils
from .base58 import Base58Encoder
from .bip_coin_conf import BitcoinConf
from .key_helper import KeyHelper

class P2SHConst:
    __doc__ = ' Class container for P2SH constants. '
    SCRIPT_BYTES = b'0014'


class P2SH:
    __doc__ = ' P2SH class. It allows the Pay-to-Script-Hash address generation. '

    @staticmethod
    def ToAddress(pub_key_bytes, net_addr_ver=BitcoinConf.P2SH_NET_VER.Main()):
        """ Get address in P2SH format.

        Args:
            pub_key_bytes (bytes)         : Public key bytes
            net_addr_ver (bytes, optional): Net address version, default is Bitcoin main network

        Returns:
            str: Address string

        Raises:
            ValueError: If the key is not a public compressed key
        """
        if not KeyHelper.IsPublicCompressed(pub_key_bytes):
            raise ValueError('Public compressed key is required for P2SH')
        key_hash = utils.Hash160(pub_key_bytes)
        script_sig = binascii.unhexlify(P2SHConst.SCRIPT_BYTES) + key_hash
        addr_bytes = utils.Hash160(script_sig)
        return Base58Encoder.CheckEncode(net_addr_ver + addr_bytes)