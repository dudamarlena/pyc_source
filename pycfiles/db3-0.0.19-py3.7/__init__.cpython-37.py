# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ssdb/__init__.py
# Compiled at: 2020-03-25 11:37:00
# Size of source mod 2**32: 620 bytes
from ssdb.kv import KV
from ssdb.hash import HashMap
from ssdb.queue import Queue
from ssdb.z_hash import ZHash

class Client(HashMap, KV, ZHash, Queue):
    pass


__version__ = '0.0.19'
VERSION = tuple(map(int, __version__.split('.')))