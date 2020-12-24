# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\bip_utils\bip32_utils.py
# Compiled at: 2020-04-16 09:47:44
# Size of source mod 2**32: 1956 bytes


class Bip32UtilsConst:
    __doc__ = ' Class container for BIP32 utility constants. '
    HARDENED_IDX = 2147483648


class Bip32Utils:
    __doc__ = ' BIP32 utility class. It contains some helper method for Bip32 class. '

    @staticmethod
    def HardenIndex(index):
        """ Harden the specified index and return it.

        Args:
            index (int): Index

        Returns:
            int: Hardened index
        """
        return Bip32UtilsConst.HARDENED_IDX + index

    @staticmethod
    def IsHardenedIndex(index):
        """ Get if the specified index is hardened.

        Args:
            index (int): Index

        Returns:
            bool: True if hardened, false otherwise
        """
        return index & Bip32UtilsConst.HARDENED_IDX != 0