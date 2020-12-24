# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\bip_utils\bip39_ex.py
# Compiled at: 2020-04-16 12:47:57
# Size of source mod 2**32: 1304 bytes


class Bip39InvalidFileError(Exception):
    __doc__ = ' Exception in case of invalid words list file. '


class Bip39ChecksumError(Exception):
    __doc__ = ' Exception in case of checksum error. '