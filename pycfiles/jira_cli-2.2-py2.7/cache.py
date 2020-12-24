# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/jiracli/cache.py
# Compiled at: 2016-10-11 22:05:56
"""

"""
from contextlib import closing
from functools import wraps
import hashlib, os, pickle, shutil, time
from jiracli.utils import CONFIG_DIR
CACHE_DIR = os.path.join(CONFIG_DIR, 'cache')
CACHE_DURATION = 86400

def cached(name):

    def __inner(fn):

        @wraps(fn)
        def _inner(*args, **kwargs):
            token = hashlib.md5(('').join([ str(k) for k in args ] + [ str(k) for k in kwargs.values() ]).encode('utf-8')).hexdigest()
            cached = CachedData(name + token)
            if not cached.get():
                resp = fn(*args, **kwargs)
                cached.update(resp)
            return cached.get()

        return _inner

    return __inner


class CachedData(object):

    def __init__(self, name):
        self.name = name
        self.cached = None
        self.path = os.path.join(CACHE_DIR, self.name + '.cache')
        if not os.path.isdir(CACHE_DIR):
            os.makedirs(CACHE_DIR)
        return

    def update(self, data):
        with closing(open(self.path, 'wb')) as (fp):
            self.cached = data
            fp.write(pickle.dumps(data))

    def invalidate(self):
        if os.path.isfile(self.path):
            os.unlink(self.path)
        self.cached = None
        return

    def get(self):
        try:
            try:
                with closing(open(self.path, 'rb')) as (fp):
                    if time.time() - os.stat(self.path).st_mtime >= CACHE_DURATION:
                        self.invalidate()
                    else:
                        self.cached = pickle.loads(fp.read())
            except AttributeError:
                self.invalidate()
            except IOError:
                return None

        finally:
            return self.cached


def clear_cache(*cached_data):
    if not cached_data:
        if os.path.isdir(CACHE_DIR):
            shutil.rmtree(CACHE_DIR)
    else:
        for data in cached_data:
            data.invalidate()