# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/stuf/core.py
# Compiled at: 2014-12-22 20:16:59
"""core stuf."""
from itertools import chain
from collections import Mapping, defaultdict, namedtuple
from ._core import basewrite, writestuf, writewrapstuf, wraps, wrapstuf, asdict
from .deep import getcls
from .iterable import exhaustcall
from .desc import lazy_class, lazy
from .collects import ChainMap, Counter, OrderedDict
__all__ = ('defaultstuf fixedstuf frozenstuf orderedstuf stuf').split()

class chainstuf(basewrite, ChainMap):
    """stuf chained together."""

    def __init__(self, *args):
        super(chainstuf, self).__init__(*args)
        maps = self.maps
        for (idx, item) in enumerate(maps):
            maps[idx] = stuf(item)

    def __reduce__(self):
        return (getcls(self), tuple(self.maps))

    @lazy_class
    def _classkeys(self):
        return frozenset(chain(super(chainstuf, self)._classkeys, ['maps']))

    copy = ChainMap.copy
    update = ChainMap.update


class countstuf(basewrite, Counter):
    """stuf that counts."""
    pass


class defaultstuf(writestuf, defaultdict):
    """
    Dictionary with attribute-style access and a factory function to provide a
    default value for keys with no value.
    """
    __slots__ = []
    _map = defaultdict

    def __init__(self, default, *args, **kw):
        """
        :argument default: function that can provide default values
        :param *args: iterable of keys/value pairs
        :param **kw: keyword arguments
        """
        defaultdict.__init__(self, default)
        writestuf.update(self, *args, **kw)

    def _build(self, iterable):
        try:
            kind = self._map
            kw = kind(self.default_factory)
            exhaustcall(kw.update, iterable)
        except (ValueError, TypeError):
            kw.update(kind(self.default_factory, iterable))

        return kw

    def _new(self, iterable):
        return getcls(self)(self.default_factory, self._build(iterable))


class fixedstuf(writewrapstuf):
    """
    Dictionary with attribute-style access where mutability is restricted to
    initial keys.
    """

    def __setitem__(self, key, value):
        if key in self.allowed:
            super(fixedstuf, self).__setitem__(key, value)
        else:
            raise KeyError(('key "{0}" not allowed').format(key))

    def _prepop(self, *args, **kw):
        iterable = super(fixedstuf, self)._prepop(*args, **kw)
        self.allowed = frozenset(iterable)
        return iterable

    def clear(self):
        wraps(self).clear()

    def popitem(self):
        raise AttributeError()

    def pop(self, key, default=None):
        raise AttributeError()


class frozenstuf(wrapstuf, Mapping):
    """Immutable dictionary with attribute-style access."""
    __slots__ = [
     '_wrapped']

    def __getitem__(self, key):
        try:
            return getattr(wraps(self), key)
        except AttributeError:
            raise KeyError(('key {0} not found').format(key))

    def __iter__(self):
        return iter(asdict(self)())

    def __len__(self):
        return len(asdict(self)())

    def __reduce__(self):
        return (
         getcls(self), (asdict(self)().copy(),))

    @classmethod
    def _mapping(self, mapping):
        return namedtuple('frozenstuf', iter(mapping))(**mapping)


class orderedstuf(writewrapstuf):
    """Dictionary with dot attributes that remember insertion order."""
    _mapping = OrderedDict

    @lazy
    def __reversed__(self):
        return wraps(self).__reversed__

    @classmethod
    def fromkeys(cls, keys, value=None):
        return cls(cls._mapping.fromkeys(keys, value))


class stuf(writestuf, dict):
    """Dictionary with attribute-style access."""
    __slots__ = []
    __init__ = writestuf.update