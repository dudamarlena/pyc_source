# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/redisobjects/decorators.py
# Compiled at: 2019-09-28 15:18:33
# Size of source mod 2**32: 110 bytes
from .redis_index_atom import RedisIndexAtom

def indexed(prop):
    return RedisIndexAtom(primary_atom=prop)