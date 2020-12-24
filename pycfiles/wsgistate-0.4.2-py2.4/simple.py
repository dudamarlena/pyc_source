# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/wsgistate/simple.py
# Compiled at: 2007-10-22 20:28:52
"""Single-process in-memory cache backend."""
import time, random
from wsgistate import BaseCache
from wsgistate.cache import WsgiMemoize
from wsgistate.session import CookieSession, URLSession, SessionCache
__all__ = [
 'SimpleCache', 'memoize', 'session', 'urlsession']

def simplememo_deploy(global_conf, **kw):
    """Paste Deploy loader for caching."""

    def decorator(application):
        _simple_memo_cache = SimpleCache(kw.get('cache'), **kw)
        return WsgiMemoize(application, _simple_memo_cache, **kw)

    return decorator


def simplesess_deploy(global_conf, **kw):
    """Paste Deploy loader for sessions."""

    def decorator(application):
        _simple_base_cache = SimpleCache(kw.get('cache'), **kw)
        _simple_session_cache = SessionCache(_simple_base_cache, **kw)
        return CookieSession(application, _simple_session_cache, **kw)

    return decorator


def simpleurlsess_deploy(global_conf, **kw):
    """Paste Deploy loader for URL encoded sessions.

    @param initstr Database initialization string
    """

    def decorator(application):
        _simple_ubase_cache = SimpleCache(kw.get('cache'), **kw)
        _simple_url_cache = SessionCache(_simple_ubase_cache, **kw)
        return URLSession(application, _simple_url_cache, **kw)

    return decorator


def memoize(**kw):
    """Decorator for caching."""

    def decorator(application):
        _simple_memo_cache = SimpleCache(**kw)
        return WsgiMemoize(application, _simple_memo_cache, **kw)

    return decorator


def session(**kw):
    """Decorator for sessions."""

    def decorator(application):
        _simple_base_cache = SimpleCache(**kw)
        _simple_session_cache = SessionCache(_simple_base_cache, **kw)
        return CookieSession(application, _simple_session_cache, **kw)

    return decorator


def urlsession(**kw):
    """Decorator for URL encoded sessions."""

    def decorator(application):
        _simple_ubase_cache = SimpleCache(**kw)
        _simple_url_cache = SessionCache(_simple_ubase_cache, **kw)
        return URLSession(application, _simple_url_cache, **kw)

    return decorator


class SimpleCache(BaseCache):
    """Single-process in-memory cache backend."""
    __module__ = __name__

    def __init__(self, *a, **kw):
        super(SimpleCache, self).__init__(*a, **kw)
        random.seed()
        self._cache = dict()
        max_entries = kw.get('max_entries', 300)
        try:
            self._max_entries = int(max_entries)
        except (ValueError, TypeError):
            self._max_entries = 300

        self._maxcull = kw.get('maxcull', 10)

    def get(self, key, default=None):
        """Fetch a given key from the cache.  If the key does not exist, return
        default, which itself defaults to None.

        @param key Keyword of item in cache.
        @param default Default value (default: None)
        """
        values = self._cache.get(key)
        if values is None:
            return default
        if values[0] < time.time():
            self.delete(key)
            return default
        return values[1]

    def set(self, key, value):
        """Set a value in the cache.

        @param key Keyword of item in cache.
        @param value Value to be inserted in cache.
        """
        if len(self._cache) >= self._max_entries:
            self._cull()
        self._cache[key] = (
         time.time() + self.timeout, value)

    def delete(self, key):
        """Delete a key from the cache, failing silently.

        @param key Keyword of item in cache.
        """
        try:
            del self._cache[key]
        except KeyError:
            pass

    def keys(self):
        """Returns a list of keys in the cache."""
        return self._cache.keys()

    def _cull(self):
        """Remove items in cache to make room."""
        num, maxcull = 0, self._maxcull
        for key in self.keys():
            if num <= maxcull:
                if self.get(key) is None:
                    num += 1
            else:
                break

        while len(self.keys()) >= self._max_entries and num <= maxcull:
            self.delete(random.choice(self.keys()))
            num += 1

        return