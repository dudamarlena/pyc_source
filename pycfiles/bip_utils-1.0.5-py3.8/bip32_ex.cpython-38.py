# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\bip_utils\bip32_ex.py
# Compiled at: 2020-04-13 05:41:00
# Size of source mod 2**32: 1321 bytes


class Bip32KeyError(Exception):
    __doc__ = ' Exception in case of key error. '


class Bip32PathError(Exception):
    __doc__ = ' Expcetion in case of path error. '