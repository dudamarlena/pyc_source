# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\strategycontainer\utils\cache.py
# Compiled at: 2018-01-19 01:43:27
# Size of source mod 2**32: 4348 bytes
"""
Caching utilities for zipline
"""
from .sentinel import sentinel

class Expired(Exception):
    __doc__ = 'Marks that a :class:`CachedObject` has expired.\n    '


ExpiredCachedObject = sentinel('ExpiredCachedObject')
AlwaysExpired = sentinel('AlwaysExpired')

class CachedObject(object):
    __doc__ = "\n    A simple struct for maintaining a cached object with an expiration date.\n\n    Parameters\n    ----------\n    value : object\n        The object to cache.\n    expires : datetime-like\n        Expiration date of `value`. The cache is considered invalid for dates\n        **strictly greater** than `expires`.\n\n    Examples\n    --------\n    >>> from pandas import Timestamp, Timedelta\n    >>> expires = Timestamp('2014', tz='UTC')\n    >>> obj = CachedObject(1, expires)\n    >>> obj.unwrap(expires - Timedelta('1 minute'))\n    1\n    >>> obj.unwrap(expires)\n    1\n    >>> obj.unwrap(expires + Timedelta('1 minute'))\n    ... # doctest: +IGNORE_EXCEPTION_DETAIL\n    Traceback (most recent call last):\n        ...\n    Expired: 2014-01-01 00:00:00+00:00\n    "

    def __init__(self, value, expires):
        self._value = value
        self._expires = expires

    @classmethod
    def expired(cls):
        """Construct a CachedObject that's expired at any time.
        """
        return cls(ExpiredCachedObject, expires=AlwaysExpired)

    def unwrap(self, dt):
        """
        Get the cached value.

        Returns
        -------
        value : object
            The cached value.

        Raises
        ------
        Expired
            Raised when `dt` is greater than self.expires.
        """
        expires = self._expires
        if expires is AlwaysExpired or expires < dt:
            raise Expired(self._expires)
        return self._value

    def _unsafe_get_value(self):
        """You almost certainly shouldn't use this."""
        return self._value


class ExpiringCache(object):
    __doc__ = "\n    A cache of multiple CachedObjects, which returns the wrapped the value\n    or raises and deletes the CachedObject if the value has expired.\n\n    Parameters\n    ----------\n    cache : dict-like, optional\n        An instance of a dict-like object which needs to support at least:\n        `__del__`, `__getitem__`, `__setitem__`\n        If `None`, than a dict is used as a default.\n\n    cleanup : callable, optional\n        A method that takes a single argument, a cached object, and is called\n        upon expiry of the cached object, prior to deleting the object. If not\n        provided, defaults to a no-op.\n\n    Examples\n    --------\n    >>> from pandas import Timestamp, Timedelta\n    >>> expires = Timestamp('2014', tz='UTC')\n    >>> value = 1\n    >>> cache = ExpiringCache()\n    >>> cache.set('foo', value, expires)\n    >>> cache.get('foo', expires - Timedelta('1 minute'))\n    1\n    >>> cache.get('foo', expires + Timedelta('1 minute'))\n    Traceback (most recent call last):\n        ...\n    KeyError: 'foo'\n    "

    def __init__(self, cache=None, cleanup=lambda value_to_clean: None):
        if cache is not None:
            self._cache = cache
        else:
            self._cache = {}
        self.cleanup = cleanup

    def get(self, key, dt):
        """Get the value of a cached object.

        Parameters
        ----------
        key : any
            The key to lookup.
        dt : datetime
            The time of the lookup.

        Returns
        -------
        result : any
            The value for ``key``.

        Raises
        ------
        KeyError
            Raised if the key is not in the cache or the value for the key
            has expired.
        """
        try:
            return self._cache[key].unwrap(dt)
        except Expired:
            self.cleanup(self._cache[key]._unsafe_get_value())
            del self._cache[key]
            raise KeyError(key)

    def set(self, key, value, expiration_dt):
        """Adds a new key value pair to the cache.

        Parameters
        ----------
        key : any
            The key to use for the pair.
        value : any
            The value to store under the name ``key``.
        expiration_dt : datetime
            When should this mapping expire? The cache is considered invalid
            for dates **strictly greater** than ``expiration_dt``.
        """
        self._cache[key] = CachedObject(value, expiration_dt)