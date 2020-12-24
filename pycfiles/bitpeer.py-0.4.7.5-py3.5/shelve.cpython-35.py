# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bitpeer/storage/shelve.py
# Compiled at: 2015-11-28 05:43:12
# Size of source mod 2**32: 370 bytes
from . import storage
import shelve

class ShelveStorage(storage.Storage):

    def __init__(self, f):
        self.shelve = shelve.open(f)

    def __getitem__(self, key):
        return self.shelve[key]

    def __setitem__(self, key, value):
        self.shelve[key] = value

    def __contains__(self, key):
        return key in self.shelve

    def sync(self):
        return self.shelve.sync()