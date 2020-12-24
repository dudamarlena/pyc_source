# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\AsyncSpider\core\data.py
# Compiled at: 2018-03-10 13:44:21
# Size of source mod 2**32: 3366 bytes
from abc import ABCMeta
from collections import Mapping, MutableMapping, KeysView
__all__ = ['DefinedKeysDictMeta', 'DefinedKeysDict', 'FrozenDict']

class DefinedKeysDictMeta(ABCMeta):

    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        keys = getattr(cls, '_keys')
        setattr(cls, '_key_num', len(keys))
        setattr(cls, '_key2index', {k:i for i, k in enumerate(keys)})


class DefinedKeysDict(MutableMapping, metaclass=DefinedKeysDictMeta):
    __slots__ = ('_values', )
    _DefinedKeysDict__marker = object()
    _keys = ()
    _key_num = 0
    _key2index = {}

    def __init__(self, **kwargs):
        self._values = [
         self._DefinedKeysDict__marker] * self._key_num
        for key, value in kwargs.items():
            if key not in self._keys:
                raise KeyError(key)
            self._values[self._key2index[key]] = value

    def __getitem__(self, key):
        if key not in self._keys:
            raise KeyError(key)
        v = self._values[self._key2index[key]]
        if v is self._DefinedKeysDict__marker:
            raise KeyError(key)
        return v

    def __setitem__(self, key, value):
        if key not in self._keys:
            raise KeyError(key)
        self._values[self._key2index[key]] = value

    def __delitem__(self, key):
        if key not in self._keys:
            raise KeyError(key)
        self._values[self._key2index[key]] = self._DefinedKeysDict__marker

    def __iter__(self):
        for i in range(self._key_num):
            if self._values[i] is not self._DefinedKeysDict__marker:
                yield self._keys[i]

    def __len__(self):
        return self._key_num

    def __str__(self):
        return '{' + ', '.join('{!r}: {!r}'.format(k, v) for k, v in self.items()) + '}'

    def pop(self, key, default=_DefinedKeysDict__marker):
        try:
            v = self[key]
        except KeyError:
            if default is self._DefinedKeysDict__marker:
                raise
            return default
        else:
            del self[key]
            return v

    def clear(self):
        for i in range(self._key_num):
            self._values[i] = self._DefinedKeysDict__marker

    def copy(self):
        return (self.__class__)(**self)

    @classmethod
    def all_keys(cls):
        return KeysView(cls._keys)


class FrozenDict(Mapping):

    def __init__(self, *args, **kwargs):
        self._d = dict(*args, **kwargs)
        self._hash = None

    def __iter__(self):
        return iter(self._d)

    def __len__(self):
        return len(self._d)

    def __getitem__(self, key):
        return self._d[key]

    def __hash__(self):
        if self._hash is None:
            self._hash = 0
            for pair in self.items():
                self._hash ^= hash(pair)

        return self._hash