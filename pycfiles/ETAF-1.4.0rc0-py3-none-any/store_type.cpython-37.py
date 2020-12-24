# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/arch/api/base/utils/store_type.py
# Compiled at: 2020-04-28 09:19:05
# Size of source mod 2**32: 969 bytes


class StoreTypes(object):
    ROLLPAIR_IN_MEMORY = 'IN_MEMORY'
    ROLLPAIR_LMDB = 'LMDB'
    ROLLPAIR_LEVELDB = 'LEVEL_DB'
    ROLLFRAME_FILE = 'ROLL_FRAME_FILE'
    ROLLPAIR_ROLLSITE = 'ROLL_SITE'
    ROLLPAIR_FILE = 'ROLL_PAIR_FILE'
    ROLLPAIR_MMAP = 'ROLL_PAIR_MMAP'
    ROLLPAIR_CACHE = 'ROLL_PAIR_CACHE'
    ROLLPAIR_QUEUE = 'ROLL_PAIR_QUEUE'