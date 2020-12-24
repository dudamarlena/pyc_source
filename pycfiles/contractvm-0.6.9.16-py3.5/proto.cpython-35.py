# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/contractvmd/proto.py
# Compiled at: 2015-11-30 17:03:25
# Size of source mod 2**32: 720 bytes
from . import config

class Protocol:
    VERSION = 1
    MAGIC_FLAG = 'CCHN'
    STORAGE_OPRETURN_LIMIT = 40
    DATA_HASH_SIZE = 64
    TIME_UNIT_BLOCKS = 1

    def timeUnit(chain):
        return TIME_UNIT_BLOCKS

    def estimateFee(chain, weight=1000):
        return config.CHAINS[chain]['base_fee'] + weight * 4 + 2

    def estimateExpiryFromFee(chain, fee, weight):
        fee = int(fee) - config.CHAINS[chain]['base_fee'] - 2
        return int(fee / weight)