# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/wsgistate/file.py
# Compiled at: 2007-10-22 20:29:15
"""File-based cache backend"""
import os, time, urllib
try:
    import cPickle as pickle
except ImportError:
    import pickle

from wsgistate.simple import SimpleCache
from wsgistate.cache import WsgiMemoize
from wsgistate.session import CookieSession, URLSession, SessionCache
__all__ = [
 'FileCache', 'memoize', 'session', 'urlsession']

def filememo_deploy(global_conf, **kw):
    """Paste Deploy loader for caching."""

    def decorator(application):
        _file_memo_cache = FileCache(kw.get('cache'), **kw)
        return WsgiMemoize(application, _file_memo_cache, **kw)

    return decorator


def filesess_deploy(global_conf, **kw):
    """Paste Deploy loader for sessions."""

    def decorator(application):
        _file_base_cache = FileCache(kw.get('cache'), **kw)
        _file_session_cache = SessionCache(_file_base_cache, **kw)
        return CookieSession(application, _file_session_cache, **kw)

    return decorator


def fileurlsess_deploy(global_conf, **kw):
    """Paste Deploy loader for URL encoded sessions.

    @param initstr Database initialization string
    """

    def decorator(application):
        _file_ubase_cache = FileCache(kw.get('cache'), **kw)
        _file_url_cache = SessionCache(_file_ubase_cache, **kw)
        return URLSession(application, _file_url_cache, **kw)

    return decorator


def memoize(path, **kw):
    """Decorator for caching.

    @param path Filesystem path
    """

    def decorator(application):
        _file_memo_cache = FileCache(path, **kw)
        return WsgiMemoize(application, _file_memo_cache, **kw)

    return decorator


def session(path, **kw):
    """Decorator for sessions.

    @param path Filesystem path
    """

    def decorator(application):
        _file_base_cache = FileCache(path, **kw)
        _file_session_cache = SessionCache(_file_base_cache, **kw)
        return CookieSession(application, _file_session_cache, **kw)

    return decorator


def urlsession(path, **kw):
    """Decorator for URL encoded sessions.

    @param path Filesystem path
    """

    def decorator(application):
        _file_ubase_cache = FileCache(path, **kw)
        _file_url_cache = SessionCache(_file_ubase_cache, **kw)
        return URLSession(application, _file_url_cache, **kw)

    return decorator


class FileCache(SimpleCache):
    """File-based cache backend"""
    __module__ = __name__

    def __init__(self, *a, **kw):
        super(FileCache, self).__init__(*a, **kw)
        try:
            self._dir = a[0]
        except IndexError:
            raise IOError('file.FileCache requires a valid directory path.')

        if not os.path.exists(self._dir):
            self._createdir()
        del self._cache

    def __contains__(self, key):
        """Tell if a given key is in the cache."""
        return os.path.exists(self._key_to_file(key))

    def get(self, key, default=None):
        """Fetch a given key from the cache.  If the key does not exist, return
        default, which itself defaults to None.

        @param key Keyword of item in cache.
        @param default Default value (default: None)
        """
        try:
            (exp, value) = pickle.load(open(self._key_to_file(key), 'rb'))
            if exp < time.time():
                self.delete(key)
                return default
            return value
        except (IOError, OSError, EOFError, pickle.PickleError):
            pass

        return default

    def set(self, key, value):
        """Set a value in the cache.

        @param key Keyword of item in cache.
        @param value Value to be inserted in cache.
        """
        if len(self.keys()) > self._max_entries:
            self._cull()
        try:
            fname = self._key_to_file(key)
            pickle.dump((time.time() + self.timeout, value), open(fname, 'wb'), 2)
        except (IOError, OSError):
            pass

    def delete(self, key):
        """Delete a key from the cache, failing silently.

        @param key Keyword of item in cache.
        """
        try:
            os.remove(self._key_to_file(key))
        except (IOError, OSError):
            pass

    def keys(self):
        """Returns a list of keys in the cache."""
        return os.listdir(self._dir)

    def _createdir(self):
        """Creates the cache directory."""
        try:
            os.makedirs(self._dir)
        except OSError:
            raise EnvironmentError('Cache directory "%s" does not exist and could not be created' % self._dir)

    def _key_to_file(self, key):
        """Gives the filesystem path for a key."""
        return os.path.join(self._dir, urllib.quote_plus(key))