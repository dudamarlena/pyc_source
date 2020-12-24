# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/coltonprovias/Development/zymio/stackman/stackman/common/redis.py
# Compiled at: 2013-12-13 04:35:07
# Size of source mod 2**32: 281 bytes
"""
StackMan
Colton J. Provias - cj@coltonprovias.com
"""
from stackman.stack import StackItem

class Redis(StackItem):
    __doc__ = '\n    Initializes a redis server.\n\n    Arguments:\n    * command (str) Command\n                    Default: redis-server\n    '
    ready_text = 'ready'