# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\bip_utils\base58_ex.py
# Compiled at: 2020-04-16 14:18:48
# Size of source mod 2**32: 1196 bytes


class Base58ChecksumError(Exception):
    __doc__ = ' Exception in case of checksum error. '