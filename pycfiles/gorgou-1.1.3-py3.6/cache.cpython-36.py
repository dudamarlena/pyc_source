# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/gorgou/cache.py
# Compiled at: 2018-02-02 23:22:40
# Size of source mod 2**32: 897 bytes
import time, re

class Cache:
    _ = {}

    @staticmethod
    def obtain(key):
        if key in Cache._:
            try:
                if 'v' in Cache._[key]:
                    if 'e' in Cache._[key]:
                        if Cache._[key]['e'] is None or Cache._[key]['e'] > int(time.time()):
                            return Cache._[key]['v']
                Cache.delete(key)
            except:
                pass

    @staticmethod
    def upsert(key, val, lft=3600):
        Cache._[key] = {'v':val,  'e':None if lft is None else int(time.time()) + int(lft)}

    @staticmethod
    def delete(key, exp=False):
        try:
            if exp:
                for k in Cache._:
                    if re.search(key, k):
                        del Cache._[k]

            else:
                if key in Cache._:
                    del Cache._[key]
        except:
            pass