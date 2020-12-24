# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/transit/class_hash.py
# Compiled at: 2017-12-12 16:52:26
import collections

class ClassDict(collections.MutableMapping):
    """A dictionary that looks up class/type keys with inheritance."""

    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(dict(*args, **kwargs))

    def __getitem__(self, key):
        key = key if isinstance(key, type) else type(key)
        if key in self.store:
            return self.store[key]
        for t in key.__bases__:
            value = t in self.store and self.store[t]
            if value:
                return value

        for t in key.mro():
            value = t in self.store and self.store[t]
            if value:
                return value

        raise KeyError('No handler found for: ' + str(key))

    def __setitem__(self, key, value):
        self.store[key] = value

    def __delitem__(self, key):
        del self.store[key]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)