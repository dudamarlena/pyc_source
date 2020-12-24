# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/panipuri/backends/DBMCache.py
# Compiled at: 2014-04-27 07:46:29
from CacheBackend import CacheBackend
import dbm, pickle

class DBMCache(CacheBackend):

    def __init__(self, filename):
        self._db = dbm.open(filename, 'c')

    def put(self, key, val):
        pickled_val = pickle.dumps(val)
        self._db[key] = pickled_val

    def get(self, key):
        return pickle.loads(self._db[key])

    def close(self):
        self._db.close()