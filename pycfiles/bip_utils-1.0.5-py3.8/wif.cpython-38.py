# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\bip_utils\wif.py
# Compiled at: 2020-04-16 10:30:45
# Size of source mod 2**32: 4046 bytes
from .base58 import Base58Decoder, Base58Encoder
from .bip_coin_conf import BitcoinConf
from .key_helper import KeyHelper
from . import utils

class WifConst:
    __doc__ = ' Class container for WIF constants. '
    PUB_KEY_SUFFIX = b'\x01'


class WifEncoder:
    __doc__ = ' WIF encoder class. It provides methods for encoding to WIF format. '

    @staticmethod
    def Encode(key_bytes, net_addr_ver=BitcoinConf.WIF_NET_VER.Main()):
        """ Encode key bytes into a WIF string.

        Args:
            key_bytes (bytes)             : Key bytes
            net_addr_ver (bytes, optional): Net address version, default is Bitcoin main network

        Returns:
            str: WIF encoded string

        Raises:
            ValueError: If the key is not valid
        """
        if not KeyHelper.IsValid(key_bytes):
            raise ValueError('Invalid key (%s)' % utils.BytesToHexString(key_bytes))
        if KeyHelper.IsPublicCompressed(key_bytes):
            key_bytes += WifConst.PUB_KEY_SUFFIX
        key_bytes = net_addr_ver + key_bytes
        return Base58Encoder.CheckEncode(key_bytes)


class WifDecoder:
    __doc__ = ' WIF encoder class. It provides methods for encoding to WIF format.'

    @staticmethod
    def Decode(wif_str, net_addr_ver=BitcoinConf.WIF_NET_VER.Main()):
        """ Decode key bytes from a WIF string.

        Args:
            wif_str (str)                 : WIF string
            net_addr_ver (bytes, optional): Net address version, default is Bitcoin main network

        Returns:
            bytes: Key bytes

        Raises:
            Base58ChecksumError: If the base58 checksum is not valid
            ValueError: If the resulting key is not valid
        """
        key_bytes = Base58Decoder.CheckDecode(wif_str)
        if key_bytes[0] != ord(net_addr_ver):
            raise ValueError('Invalid net version (expected %x, got %x)' % (ord(net_addr_ver), key_bytes[0]))
        key_bytes = key_bytes[1:]
        if KeyHelper.IsPublicCompressed(key_bytes[:-1]):
            if key_bytes[(-1)] != ord(WifConst.PUB_KEY_SUFFIX):
                raise ValueError('Invalid compressed public key suffix (expected %x, got %x)' % (ord(WifConst.PUB_KEY_SUFFIX), key_bytes[(-1)]))
            key_bytes = key_bytes[:-1]
        if not KeyHelper.IsValid(key_bytes):
            raise ValueError('Invalid decoded key (%s)' % utils.BytesToHexString(key_bytes))
        return key_bytes