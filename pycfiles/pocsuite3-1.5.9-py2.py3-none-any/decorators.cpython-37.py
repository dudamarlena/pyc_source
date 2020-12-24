# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/boyhack/programs/pocsuite3/pocsuite3/lib/core/decorators.py
# Compiled at: 2019-03-15 03:35:12
# Size of source mod 2**32: 482 bytes
import hashlib

def cachedmethod(f, cache={}):
    """
    Method with a cached content
    Reference: http://code.activestate.com/recipes/325205-cache-decorator-in-python-24/
    """

    def _(*args, **kwargs):
        key_string = '|'.join((str(_) for _ in (f, args, kwargs))).encode()
        key = int(hashlib.md5(key_string).hexdigest(), 16) & 9223372036854775807
        if key not in cache:
            cache[key] = f(*args, **kwargs)
        return cache[key]

    return _