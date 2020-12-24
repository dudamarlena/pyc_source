# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/paulos/.virtualenvs/doid/lib/python3.6/site-packages/doid/container.py
# Compiled at: 2018-09-26 01:10:49
# Size of source mod 2**32: 1308 bytes
from .filter import Q, ga

class K(object):
    __doc__ = 'Key getter object\n\n    Receives an arbitrary list of strings or callables. Callables\n    will be called with the object to be sorted and should return\n    a sort key. Strings are resolved to attributes following the\n    Django ORM protocol. Returns a list of keys in the same order\n    as the arguments.\n    '

    def __init__(self, *args):
        self._args = args

    @staticmethod
    def _ga(obj, attr_path):
        return ga(obj, *attr_path.split('__'))

    def _apply(self, obj, arg):
        if callable(arg):
            return arg(obj)
        else:
            return self._ga(obj, arg)

    def __call__(self, obj):
        return [self._apply(obj, arg) for arg in self._args]


class ListContainer(list):
    __doc__ = 'The list container object is an ordered collection of objects that can\n    be sorted and/or filtered\n    '

    def __getitem__(self, k):
        if isinstance(k, slice):
            return ListContainer(super().__getitem__(k))
        else:
            return super().__getitem__(k)

    def filter(self, *args, **kwargs):
        f = Q(*args, **kwargs)
        return ListContainer(item for item in self if f(item))

    def order_by(self, *args, **kwargs):
        copy = self[:]
        (copy.sort)(key=K(*args), **kwargs)
        return ListContainer(copy)