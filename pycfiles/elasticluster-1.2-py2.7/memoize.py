# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/elasticluster/memoize.py
# Compiled at: 2014-10-22 16:00:16
__docformat__ = 'reStructuredText'
__author__ = 'Antonio Messina <antonio.s.messina@gmail.com>'
import time

class memoize(object):
    """Decorator that caches a function's return value each time it is
    called within a TTL If called within the TTL and the same
    arguments, the cached value is returned, If called outside the TTL
    or a different value, a fresh value is returned.

    """

    def __init__(self, ttl):
        self.cache = {}
        self.ttl = ttl

    def __call__(self, f):

        def wrapped_f(*args):
            now = time.time()
            try:
                value, last_update = self.cache[args]
                if self.ttl > 0 and now - last_update > self.ttl:
                    raise AttributeError
                return value
            except (KeyError, AttributeError):
                value = f(*args)
                self.cache[args] = (value, now)
                return value
            except TypeError:
                return f(*args)

        return wrapped_f