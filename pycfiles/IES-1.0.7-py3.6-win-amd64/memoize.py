# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\strategycontainer\utils\memoize.py
# Compiled at: 2018-01-16 04:53:04
# Size of source mod 2**32: 9232 bytes
"""
Tools for memoization of function results.
"""
from collections import OrderedDict, Sequence
from itertools import compress
from weakref import WeakKeyDictionary, ref
from six.moves._thread import allocate_lock as Lock
from toolz.sandbox import unzip
from strategycontainer.utils.compat import wraps

class lazyval(object):
    __doc__ = 'Decorator that marks that an attribute of an instance should not be\n    computed until needed, and that the value should be memoized.\n\n    Example\n    -------\n\n    >>> from zipline.utils.memoize import lazyval\n    >>> class C(object):\n    ...     def __init__(self):\n    ...         self.count = 0\n    ...     @lazyval\n    ...     def val(self):\n    ...         self.count += 1\n    ...         return "val"\n    ...\n    >>> c = C()\n    >>> c.count\n    0\n    >>> c.val, c.count\n    (\'val\', 1)\n    >>> c.val, c.count\n    (\'val\', 1)\n    >>> c.val = \'not_val\'\n    Traceback (most recent call last):\n    ...\n    AttributeError: Can\'t set read-only attribute.\n    >>> c.val\n    \'val\'\n    '

    def __init__(self, get):
        self._get = get
        self._cache = WeakKeyDictionary()

    def __get__(self, instance, owner):
        if instance is None:
            return self
        try:
            return self._cache[instance]
        except KeyError:
            self._cache[instance] = val = self._get(instance)
            return val

    def __set__(self, instance, value):
        raise AttributeError("Can't set read-only attribute.")

    def __delitem__(self, instance):
        del self._cache[instance]


class classlazyval(lazyval):
    __doc__ = ' Decorator that marks that an attribute of a class should not be\n    computed until needed, and that the value should be memoized.\n\n    Example\n    -------\n\n    >>> from zipline.utils.memoize import classlazyval\n    >>> class C(object):\n    ...     count = 0\n    ...     @classlazyval\n    ...     def val(cls):\n    ...         cls.count += 1\n    ...         return "val"\n    ...\n    >>> C.count\n    0\n    >>> C.val, C.count\n    (\'val\', 1)\n    >>> C.val, C.count\n    (\'val\', 1)\n    '

    def __get__(self, instance, owner):
        return super(classlazyval, self).__get__(owner, owner)


def _weak_lru_cache(maxsize=100):
    """
    Users should only access the lru_cache through its public API:
    cache_info, cache_clear
    The internals of the lru_cache are encapsulated for thread safety and
    to allow the implementation to change.
    """

    def decorating_function(user_function, tuple=tuple, sorted=sorted, len=len, KeyError=KeyError):
        hits, misses = [
         0], [0]
        kwd_mark = (object(),)
        lock = Lock()
        if maxsize is None:
            cache = _WeakArgsDict()

            @wraps(user_function)
            def wrapper(*args, **kwds):
                key = args
                if kwds:
                    key += kwd_mark + tuple(sorted(kwds.items()))
                try:
                    result = cache[key]
                    hits[0] += 1
                    return result
                except KeyError:
                    pass

                result = user_function(*args, **kwds)
                cache[key] = result
                misses[0] += 1
                return result

        else:
            cache = _WeakArgsOrderedDict()
            cache_popitem = cache.popitem
            cache_renew = cache.move_to_end

            @wraps(user_function)
            def wrapper(*args, **kwds):
                key = args
                if kwds:
                    key += kwd_mark + tuple(sorted(kwds.items()))
                with lock:
                    try:
                        result = cache[key]
                        cache_renew(key)
                        hits[0] += 1
                        return result
                    except KeyError:
                        pass

                result = user_function(*args, **kwds)
                with lock:
                    cache[key] = result
                    misses[0] += 1
                    if len(cache) > maxsize:
                        cache_popitem(False)
                return result

        def cache_info():
            with lock:
                return (
                 hits[0], misses[0], maxsize, len(cache))

        def cache_clear():
            with lock:
                cache.clear()
                hits[0] = misses[0] = 0

        wrapper.cache_info = cache_info
        wrapper.cache_clear = cache_clear
        return wrapper

    return decorating_function


class _WeakArgs(Sequence):
    __doc__ = "\n    Works with _WeakArgsDict to provide a weak cache for function args.\n    When any of those args are gc'd, the pair is removed from the cache.\n    "

    def __init__(self, items, dict_remove=None):

        def remove(k, selfref=ref(self), dict_remove=dict_remove):
            self = selfref()
            if self is not None:
                if dict_remove is not None:
                    dict_remove(self)

        self._items, self._selectors = unzip(self._try_ref(item, remove) for item in items)
        self._items = tuple(self._items)
        self._selectors = tuple(self._selectors)

    def __getitem__(self, index):
        return self._items[index]

    def __len__(self):
        return len(self._items)

    @staticmethod
    def _try_ref(item, callback):
        try:
            return (
             ref(item, callback), True)
        except TypeError:
            return (
             item, False)

    @property
    def alive(self):
        return all(item() is not None for item in compress(self._items, self._selectors))

    def __eq__(self, other):
        return self._items == other._items

    def __hash__(self):
        try:
            return self._WeakArgs__hash
        except AttributeError:
            h = self._WeakArgs__hash = hash(self._items)
            return h


class _WeakArgsDict(WeakKeyDictionary, object):

    def __delitem__(self, key):
        del self.data[_WeakArgs(key)]

    def __getitem__(self, key):
        return self.data[_WeakArgs(key)]

    def __repr__(self):
        return '%s(%r)' % (type(self).__name__, self.data)

    def __setitem__(self, key, value):
        self.data[_WeakArgs(key, self._remove)] = value

    def __contains__(self, key):
        try:
            wr = _WeakArgs(key)
        except TypeError:
            return False
        else:
            return wr in self.data

    def pop(self, key, *args):
        return (self.data.pop)(_WeakArgs(key), *args)


class _WeakArgsOrderedDict(_WeakArgsDict, object):

    def __init__(self):
        super(_WeakArgsOrderedDict, self).__init__()
        self.data = OrderedDict()

    def popitem(self, last=True):
        while 1:
            key, value = self.data.popitem(last)
            if key.alive:
                return (
                 tuple(key), value)

    def move_to_end(self, key):
        """Move an existing element to the end.

        Raises KeyError if the element does not exist.
        """
        self[key] = self.pop(key)


def weak_lru_cache(maxsize=100):
    """Weak least-recently-used cache decorator.

    If *maxsize* is set to None, the LRU features are disabled and the cache
    can grow without bound.

    Arguments to the cached function must be hashable. Any that are weak-
    referenceable will be stored by weak reference.  Once any of the args have
    been garbage collected, the entry will be removed from the cache.

    View the cache statistics named tuple (hits, misses, maxsize, currsize)
    with f.cache_info().  Clear the cache and statistics with f.cache_clear().

    See:  http://en.wikipedia.org/wiki/Cache_algorithms#Least_Recently_Used

    """

    class desc(lazyval):

        def __get__(self, instance, owner):
            if instance is None:
                return self
            try:
                return self._cache[instance]
            except KeyError:
                inst = ref(instance)

                @_weak_lru_cache(maxsize)
                @wraps(self._get)
                def wrapper(*args, **kwargs):
                    return (self._get)(inst(), *args, **kwargs)

                self._cache[instance] = wrapper
                return wrapper

        @_weak_lru_cache(maxsize)
        def __call__(self, *args, **kwargs):
            return (self._get)(*args, **kwargs)

    return desc


remember_last = weak_lru_cache(1)