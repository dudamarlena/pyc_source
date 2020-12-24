# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\bip_utils\bip49.py
# Compiled at: 2020-04-16 11:15:42
# Size of source mod 2**32: 6840 bytes
from .bip32_utils import Bip32Utils
from .bip44_base import Bip44Base, Bip44Coins
from .bip49_coins import *

class Bip49Const:
    __doc__ = ' Class container for BIP44 constants. '
    SPEC_NAME = 'BIP-0049'
    PURPOSE = Bip32Utils.HardenIndex(49)
    ALLOWED_COINS = [
     Bip44Coins.BITCOIN, Bip44Coins.BITCOIN_TESTNET,
     Bip44Coins.LITECOIN, Bip44Coins.LITECOIN_TESTNET,
     Bip44Coins.DOGECOIN, Bip44Coins.DOGECOIN_TESTNET,
     Bip44Coins.DASH, Bip44Coins.DASH_TESTNET]
    COIN_TO_CLASS = {Bip44Coins.BITCOIN: Bip49BitcoinMainNet, 
     Bip44Coins.BITCOIN_TESTNET: Bip49BitcoinTestNet, 
     Bip44Coins.LITECOIN: Bip49LitecoinMainNet, 
     Bip44Coins.LITECOIN_TESTNET: Bip49LitecoinTestNet, 
     Bip44Coins.DOGECOIN: Bip49DogecoinMainNet, 
     Bip44Coins.DOGECOIN_TESTNET: Bip49DogecoinTestNet, 
     Bip44Coins.DASH: Bip49DashMainNet, 
     Bip44Coins.DASH_TESTNET: Bip49DashTestNet}


class Bip49(Bip44Base):
    __doc__ = ' BIP49 class. It allows master key generation and children keys derivation in according to BIP-0049.\n    BIP-0049 specifications: https://github.com/bitcoin/bips/blob/master/bip-0049.mediawiki\n    '

    def Purpose(self):
        """ Derive a child key from the purpose and return a new Bip object (e.g. BIP44, BIP49, BIP84).
        It calls the underlying _PurposeGeneric method with the current object as parameter.

        Returns:
            Bip49 object: Bip49 object

        Raises:
            Bip44DepthError: If current depth is not suitable for deriving keys
            Bip32KeyError: If the derivation results in an invalid key
        """
        return self._PurposeGeneric(self)

    def Coin(self):
        """ Derive a child key from the coin type specified at construction and return a new Bip object (e.g. BIP44, BIP49, BIP84).
        It calls the underlying _CoinGeneric method with the current object as parameter.

        Returns:
            Bip49 object: Bip49 object

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
            Bip49 object: Bip49 object

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
            Bip49 object: Bip49 object

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
            Bip49 object: Bip49 object

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
        return Bip49Const.SPEC_NAME

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
        return coin_idx in Bip49Const.ALLOWED_COINS

    @staticmethod
    def _GetPurpose():
        """ Get purpose.

        Returns:
            int: Purpose index
        """
        return Bip49Const.PURPOSE

    @staticmethod
    def _GetCoinClass(coin_idx):
        """ Get coin class.

        Args:
            coin_idx (Bip44Coins): Coin index, must be a Bip44Coins enum

        Returns:
            BipCoinBase child object: BipCoinBase child object
        """
        return Bip49Const.COIN_TO_CLASS[coin_idx]