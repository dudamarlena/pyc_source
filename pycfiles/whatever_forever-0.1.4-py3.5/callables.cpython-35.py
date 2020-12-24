# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/whatever/callables.py
# Compiled at: 2016-10-01 22:33:54
# Size of source mod 2**32: 2351 bytes
from collections import OrderedDict
from toolz.curried import flip, juxt, map, partial, pipe, valmap
from types import LambdaType
from typing import Iterable, Any
__all__ = [
 'Dispatch', 'DictCallable', 'TupleCallable', 'ListCallable', 'SetCallable']

class DictCallable(dict):

    def __call__(self, *args, **kwargs):
        return valmap(lambda x: x(*args, **kwargs), self)


class Condictional(OrderedDict):
    __doc__ = 'First key to satisfy the key condition executes.\n    '

    def key(self, x, *args, **kwargs) -> bool:
        return x(*args, **kwargs)

    def __init__(self, args=[], default=None, key=None):
        super().__init__(args)
        self.default = default
        if key:
            self.key = key

    def __call__(self, *args, **kwargs):
        for key, value in self.items():
            if self.key(key, *args, **kwargs):
                return value(*args, **kwargs)

        if self.default:
            return self.default(*args, **kwargs)
        raise KeyError('No conditions satisfied')


class Dispatch(Condictional):
    __doc__ = 'An object that provides multiple dispatch when it is called.\n    '

    def key(self, key, *args, **kwargs):
        if not isinstance(key, Iterable):
            key = tuple([key])
        if len(args) == len(key):
            return all(isinstance(arg, types) for arg, types in zip(args, key) if isinstance(types, Iterable) or types != Any)
        return False

    def __init__(self, args=[], default=None):
        super().__init__(args)
        self.default = default


class ListCallable(list):

    def __call__(self, *args, **kwargs):
        return list(juxt(*self)(*args, **kwargs))


class SetCallable(set):

    def __call__(self, *args, **kwargs):
        if pipe(self, map(partial(flip(isinstance), LambdaType)), any):
            raise TypeError('Cannot interpolate a LambdaType.')
        return pipe(zip(self, list(map(lambda x: x(*args, **kwargs), self))), list, dict)


class TupleCallable(tuple):

    def __call__(self, *args, **kwargs):
        return juxt(*self)(*args, **kwargs)