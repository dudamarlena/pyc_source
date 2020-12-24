# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bitcoin/crypto/ecdsa/defaults.py
# Compiled at: 2017-07-08 11:42:23
# Size of source mod 2**32: 177 bytes
"""
Defines ECDSA defaults
"""
from .secp256k1 import Secp256k1
DEFAULT_CURVE = Secp256k1()