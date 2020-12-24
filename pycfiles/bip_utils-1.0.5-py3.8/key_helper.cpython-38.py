# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\bip_utils\key_helper.py
# Compiled at: 2020-04-16 10:25:57
# Size of source mod 2**32: 3101 bytes


class KeyHelperConst:
    __doc__ = ' Class container for key helper constants. '
    PRIV_KEY_LEN = 32
    PUB_KEY_UNCOMPR_LEN = 64
    PUB_KEY_COMPR_LEN = 33
    PUB_KEY_COMPR_PREFIX = (2, 3)


class KeyHelper:
    __doc__ = ' Key helper class. It provides methods for checking formats of ECDSA keys. '

    @staticmethod
    def IsPrivate(key_bytes):
        """ Get if the specified key is private.

        Args:
            key_bytes (bytes): Key bytes

        Returns:
            bool: True if private, false otherwise
        """
        return len(key_bytes) == KeyHelperConst.PRIV_KEY_LEN

    @staticmethod
    def IsPublicUncompressed(key_bytes):
        """ Get if the specified key is public uncompressed.

        Args:
            key_bytes (bytes): Key bytes

        Returns:
            bool: True if public uncompressed, false otherwise
        """
        return len(key_bytes) == KeyHelperConst.PUB_KEY_UNCOMPR_LEN

    @staticmethod
    def IsPublicCompressed(key_bytes):
        """ Get if the specified key is public compressed.

        Args:
            key_bytes (bytes): Key bytes

        Returns:
            bool: True if public compressed, false otherwise
        """
        return len(key_bytes) == KeyHelperConst.PUB_KEY_COMPR_LEN and key_bytes[0] in KeyHelperConst.PUB_KEY_COMPR_PREFIX

    @staticmethod
    def IsValid(key_bytes):
        """ Get if the specified key is valid.

        Args:
            key_bytes (bytes): Key bytes

        Returns:
            bool: True if private or public compressed/decompressed, false otherwise
        """
        return KeyHelper.IsPrivate(key_bytes) or KeyHelper.IsPublicUncompressed(key_bytes) or KeyHelper.IsPublicCompressed(key_bytes)