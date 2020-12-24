# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\bip_utils\bip84.py
# Compiled at: 2020-04-16 11:15:54
# Size of source mod 2**32: 6464 bytes
from .bip32_utils import Bip32Utils
from .bip44_base import Bip44Base, Bip44Coins
from .bip84_coins import *

class Bip84Const:
    __doc__ = ' Class container for BIP44 constants. '
    SPEC_NAME = 'BIP-0084'
    PURPOSE = Bip32Utils.HardenIndex(84)
    ALLOWED_COINS = [
     Bip44Coins.BITCOIN, Bip44Coins.BITCOIN_TESTNET,
     Bip44Coins.LITECOIN, Bip44Coins.LITECOIN_TESTNET]
    COIN_TO_CLASS = {Bip44Coins.BITCOIN: Bip84BitcoinMainNet, 
     Bip44Coins.BITCOIN_TESTNET: Bip84BitcoinTestNet, 
     Bip44Coins.LITECOIN: Bip84LitecoinMainNet, 
     Bip44Coins.LITECOIN_TESTNET: Bip84LitecoinTestNet}


class Bip84(Bip44Base):
    __doc__ = ' BIP84 class. It allows master key generation and children keys derivation in according to BIP-0084.\n    BIP-0084 specifications: https://github.com/bitcoin/bips/blob/master/bip-0084.mediawiki\n    '

    def Purpose(self):
        """ Derive a child key from the purpose and return a new Bip object (e.g. BIP44, BIP49, BIP84).
        It calls the underlying _PurposeGeneric method with the current object as parameter.

        Returns:
            Bip84 object: Bip84 object

        Raises:
            Bip44DepthError: If current depth is not suitable for deriving keys
            Bip32KeyError: If the derivation results in an invalid key
        """
        return self._PurposeGeneric(self)

    def Coin(self):
        """ Derive a child key from the coin type specified at construction and return a new Bip object (e.g. BIP44, BIP49, BIP84).
        It calls the underlying _CoinGeneric method with the current object as parameter.

        Returns:
            Bip84 object: Bip84 object

        Raises:
            Bip44DepthError: If current depth is not suitable for deriving keys
            Bip32KeyError: If the derivation results in an invalid key
        """
        return self._CoinGeneric(self)

    def Account(self, acc_idx):
        """ Derive a child key from the specified account index and return a new Bip object (e.g. BIP44, BIP49, BIP84).
        It calls the underlying _AccountGeneric method with the current object as parameter.

        Args:
            acc_idx (int): Account index

        Returns:
            Bip84 object: Bip84 object

        Raises:
            Bip44DepthError: If current depth is not suitable for deriving keys
            Bip32KeyError: If the derivation results in an invalid key
        """
        return self._AccountGeneric(self, acc_idx)

    def Change(self, change_idx):
        """ Derive a child key from the specified account index and return a new Bip object (e.g. BIP44, BIP49, BIP84).
        It calls the underlying _ChangeGeneric method with the current object as parameter.

        Args:
            change_idx (Bip44Changes): Change index, must a Bip44Changes enum

        Returns:
            Bip84 object: Bip84 object

        Raises:
            TypeError: If chain index is not a Bip44Changes enum
            Bip44DepthError: If current depth is not suitable for deriving keys
            Bip32KeyError: If the derivation results in an invalid key
        """
        return self._ChangeGeneric(self, change_idx)

    def AddressIndex(self, addr_idx):
        """ Derive a child key from the specified account index and return a new Bip object (e.g. BIP44, BIP49, BIP84).
        It calls the underlying _AddressIndexGeneric method with the current object as parameter.

        Args:
            addr_idx (int): Address index

        Returns:
            Bip84 object: Bip84 object

        Raises:
            Bip44DepthError: If current depth is not suitable for deriving keys
            Bip32KeyError: If the derivation results in an invalid key
        """
        return self._AddressIndexGeneric(self, addr_idx)

    @staticmethod
    def SpecName():
        """ Get specification name.

        Returns:
            str: Specification name
        """
        return Bip84Const.SPEC_NAME

    @staticmethod
    def IsCoinAllowed(coin_idx):
        """ Get if the specified coin is allowed.

        Args:
            coin_idx (Bip44Coins): Coin index, must be a Bip44Coins enum

        Returns :
            bool: True if allowed, false otherwise

        Raises:
            TypeError: If coin_idx is not of Bip44Coins enum
        """
        if not isinstance(coin_idx, Bip44Coins):
            raise TypeError('Coin index is not an enumerative of Bip44Coins')
        return coin_idx in Bip84Const.ALLOWED_COINS

    @staticmethod
    def _GetPurpose():
        """ Get purpose.

        Returns:
            int: Purpose index
        """
        return Bip84Const.PURPOSE

    @staticmethod
    def _GetCoinClass(coin_idx):
        """ Get coin class.

        Args:
            coin_idx (Bip44Coins): Coin index, must be a Bip44Coins enum

        Returns:
            BipCoinBase child object: BipCoinBase child object
        """
        return Bip84Const.COIN_TO_CLASS[coin_idx]