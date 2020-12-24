# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bitpeer/storage/mem.py
# Compiled at: 2015-11-28 05:54:57
# Size of source mod 2**32: 293 bytes
from . import storage

class MemStorage(storage.Storage):

    def __init__(self):
        self.db = {}

    def __getitem__(self, key):
        return self.db[key]

    def __setitem__(self, key, value):
        self.db[key] = value

    def __contains__(self, key):
        return key in self.db

    def sync(self):
        pass