# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\bip_utils\bip_keys.py
# Compiled at: 2020-04-16 11:11:45
# Size of source mod 2**32: 5060 bytes
from .bip32_ex import Bip32KeyError
from .bip32_key_ser import Bip32KeySerializer
from .bip44_coins import Bip44BitcoinMainNet
from .wif import WifEncoder
from . import utils

class BipKeyBytes:
    __doc__ = ' BIP key bytes class. It allows to get key bytes in different formats. '

    def __init__(self, key_bytes):
        """ Construct class.

        Args:
            key_bytes (bytes): Key bytes
        """
        self.m_key_bytes = key_bytes

    def ToBytes(self):
        """ Get key bytes.

        Returns:
            bytes: Key bytes
        """
        return self.m_key_bytes

    def ToHex(self):
        """ Get key bytes in hex format.

        Returns:
            str: Key bytes in hex format
        """
        return utils.BytesToHexString(self.m_key_bytes)


class BipPublicKey:
    __doc__ = ' BIP public key class. It allows to get a public key in different formats. '

    def __init__(self, bip32_obj, coin_class=Bip44BitcoinMainNet):
        """ Construct class.

        Args:
            bip32_obj (Bip32 object)                       : Bip32 object
            coin_class (BipCoinBase child object, optional): BipCoinBase child object, Bip44BitcoinMainNet by default
        """
        self.m_bip32_obj = bip32_obj
        self.m_coin_class = coin_class

    def RawCompressed(self):
        """ Return raw compressed public key.

        Returns:
            BipKeyBytes object: BipKeyBytes object
        """
        return BipKeyBytes(self.m_bip32_obj.EcdsaPublicKey().to_string('compressed'))

    def RawUncompressed(self):
        """ Return raw uncompressed public key.

        Returns:
            BipKeyBytes object: BipKeyBytes object
        """
        return BipKeyBytes(self.m_bip32_obj.EcdsaPublicKey().to_string('uncompressed')[1:])

    def ToExtended(self):
        """ Return key in serialized extended format.

        Returns:
            str: Key in serialized extended format
        """
        return Bip32KeySerializer(self.m_bip32_obj).SerializePublicKey()

    def ToAddress(self):
        """ Return address correspondent tot he public key.

        Returns:
            str: Address
        """
        return self.m_coin_class.ComputeAddress(self)


class BipPrivateKey:
    __doc__ = ' BIP privte key class. It allows to get a privte key in different formats. '

    def __init__(self, bip32_obj, coin_class=Bip44BitcoinMainNet):
        """ Construct class.

        Args:
            bip32_obj (Bip32 object)                       : Bip32 object
            coin_class (BipCoinBase child object, optional): BipCoinBase child object, Bip44BitcoinMainNet by default

        Raises:
            Bip32KeyError: If the Bip32 object is public-only
        """
        if bip32_obj.IsPublicOnly():
            raise Bip32KeyError('Cannot create a private key form a public-only Bip32 object')
        self.m_bip32_obj = bip32_obj
        self.m_coin_class = coin_class

    def Raw(self):
        """ Return raw private key.

        Returns:
            BipKeyBytes object: BipKeyBytes object
        """
        return BipKeyBytes(self.m_bip32_obj.EcdsaPrivateKey().to_string())

    def ToExtended(self):
        """ Return key in serialized extended format.

        Returns:
            str: Key in serialized extended format
        """
        return Bip32KeySerializer(self.m_bip32_obj).SerializePrivateKey()

    def ToWif(self):
        """ Return key in WIF format.

        Returns:
            str: Key in WIF format
        """
        wif_net_ver = self.m_coin_class.WifNetVersion()
        if wif_net_ver is not None:
            return WifEncoder.Encode(self.Raw().ToBytes(), wif_net_ver)
        return ''