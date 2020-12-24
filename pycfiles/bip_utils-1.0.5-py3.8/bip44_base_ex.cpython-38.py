# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\bip_utils\bip44_base_ex.py
# Compiled at: 2020-04-16 12:50:23
# Size of source mod 2**32: 1350 bytes


class Bip44DepthError(Exception):
    __doc__ = ' Exception in case of derivation from wrong depth. '


class Bip44CoinNotAllowedError(Exception):
    __doc__ = ' Exception in case of derivation from wrong depth. '