# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bitcoin/nets.py
# Compiled at: 2017-07-08 11:42:23
# Size of source mod 2**32: 349 bytes
"""
Defines the Bitcoin networks available as constants to agree around the
module
"""
from enum import Enum, unique

@unique
class Network(Enum):
    unknown = -1
    mainnet = 0
    testnet = 1


DEFAULT_NETWORK = Network.testnet