# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dez/memcache.py
# Compiled at: 2020-04-19 19:55:58
from . import json
MC = None

class Memcache(object):

    def __init__(self):
        self.cache = {}
        self.last_count = {}

    def get(self, key, tojson=True):
        val = self.cache.get(key)
        return val and tojson and json.encode(val) or val

    def set(self, key, val, fromjson=True):
        self.cache[key] = fromjson and json.decode(val) or val

    def rm(self, key):
        if key in self.cache:
            del self.cache[key]

    def clear(self):
        self.cache = {}

    def count(self, items=False):
        if items:
            count = {}
            for key, val in list(self.cache.items()):
                count[key] = len(val)

            return count
        return len(self.cache)

    def diff(self):
        diff = {}
        count = self.count(True)
        for key, val in list(count.items()):
            orig = self.last_count.get(key)
            if val != orig:
                diff[key] = [
                 orig, val]

        self.last_count = count
        return diff


def get_memcache():
    global MC
    if not MC:
        MC = Memcache()
    return MC