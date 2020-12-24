# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/wsgistate/__init__.py
# Compiled at: 2007-10-15 12:26:50
"""Base Cache class"""
__all__ = [
 'BaseCache', 'db', 'file', 'memory', 'memcached', 'session', 'simple', 'cache']

def synchronized(func):
    """Decorator to lock and unlock a method (Phillip J. Eby).

    @param func Method to decorate
    """

    def wrapper(self, *__args, **__kw):
        self._lock.acquire()
        try:
            return func(self, *__args, **__kw)
        finally:
            self._lock.release()

    wrapper.__name__ = func.__name__
    wrapper.__dict__ = func.__dict__
    wrapper.__doc__ = func.__doc__
    return wrapper


class BaseCache(object):
    """Base Cache class."""
    __module__ = __name__

    def __init__(self, *a, **kw):
        super(BaseCache, self).__init__()
        timeout = kw.get('timeout', 300)
        try:
            timeout = int(timeout)
        except (ValueError, TypeError):
            timeout = 300

        self.timeout = timeout

    def __getitem__(self, key):
        """Fetch a given key from the cache."""
        return self.get(key)

    def __setitem__(self, key, value):
        """Set a value in the cache. """
        self.set(key, value)

    def __delitem__(self, key):
        """Delete a key from the cache."""
        self.delete(key)

    def __contains__(self, key):
        """Tell if a given key is in the cache."""
        return self.get(key) is not None

    def get(self, key, default=None):
        """Fetch a given key from the cache.  If the key does not exist, return
        default, which itself defaults to None.

        @param key Keyword of item in cache.
        @param default Default value (default: None)
        """
        raise NotImplementedError()

    def set(self, key, value):
        """Set a value in the cache. 

        @param key Keyword of item in cache.
        @param value Value to be inserted in cache.        
        """
        raise NotImplementedError()

    def delete(self, key):
        """Delete a key from the cache, failing silently.

        @param key Keyword of item in cache.
        """
        raise NotImplementedError()

    def get_many(self, keys):
        """Fetch a bunch of keys from the cache. Returns a dict mapping each
        key in keys to its value.  If the given key is missing, it will be
        missing from the response dict.

        @param keys Keywords of items in cache.        
        """
        d = dict()
        for k in keys:
            val = self.get(k)
            if val is not None:
                d[k] = val

        return d