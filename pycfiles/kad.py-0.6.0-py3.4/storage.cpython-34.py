# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kad/storage.py
# Compiled at: 2017-12-29 11:36:17
# Size of source mod 2**32: 398 bytes
import shelve

def test():
    pass


class Shelve:

    def __init__(self, f):
        self.shelve = shelve.open(f)

    def dump(self):
        for x in self.shelve:
            print('key:', x, '\t\tvalue:', self.shelve[x])

    def __getitem__(self, key):
        return self.shelve[str(key)]

    def __setitem__(self, key, value):
        self.shelve[str(key)] = value

    def __contains__(self, key):
        return str(key) in self.shelve