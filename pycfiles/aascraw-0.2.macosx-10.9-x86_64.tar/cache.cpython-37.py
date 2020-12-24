# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanghunkang/dev/aascraw/venv/lib/python3.7/site-packages/aascraw/cache.py
# Compiled at: 2019-08-27 10:47:14
# Size of source mod 2**32: 651 bytes
import json, os

class Cache:

    def __init__(self, fpath_cache):
        self._Cache__fpath_cache = fpath_cache
        self._Cache__cache = []
        with open(self._Cache__fpath_cache, 'r') as (f):
            try:
                self._Cache__cache = json.loads(f.read())
            except:
                pass

    def add(self, action_taken, page):
        self._Cache__cache.append([action_taken, page])

    def save(self):
        with open(self._Cache__fpath_cache, 'w') as (f):
            f.write(json.dumps((self._Cache__cache), ensure_ascii=False))

    def get(self):
        index = 0
        return (self._Cache__cache[index][0], self._Cache__cache[index][1])