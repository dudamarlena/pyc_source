# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bitcoin/address/types.py
# Compiled at: 2017-07-08 11:42:23
# Size of source mod 2**32: 286 bytes
"""
Defines the existing address types
"""
from enum import Enum, unique

@unique
class Types(Enum):
    __doc__ = '\n    Defines the types a Bitcoin address can be\n    '
    unknown = -1
    p2pkh = 1
    p2sh = 2
    wif = 3
    bip32_pubkey = 4
    bip32_pkey = 5