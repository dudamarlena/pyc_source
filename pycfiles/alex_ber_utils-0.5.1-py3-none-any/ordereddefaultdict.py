# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: kaldi2/ordereddefaultdict.py
# Compiled at: 2015-10-26 06:28:05
__doc__ = b'\nDefaultOrderedDict combine functionality from ordered and default dict.\n'
from __future__ import unicode_literals
from collections import Callable
try:
    from collections import OrderedDict
except:
    from ordereddict import OrderedDict

class DefaultOrderedDict(OrderedDict):
    """Combine functionality from ordered and default dict."""

    def __init__(self, default_factory=None, *a, **kw):
        if default_factory is not None and not isinstance(default_factory, Callable):
            raise TypeError(b'first argument must be callable')
        OrderedDict.__init__(self, *a, **kw)
        self.default_factory = default_factory
        return

    def __getitem__(self, key):
        try:
            return OrderedDict.__getitem__(self, key)
        except KeyError:
            return self.__missing__(key)

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        self[key] = value = self.default_factory()
        return value

    def __reduce__(self):
        if self.default_factory is None:
            args = tuple()
        else:
            args = (
             self.default_factory,)
        return (type(self), args, None, None, self.items())

    def copy(self):
        return self.__copy__()

    def __copy__(self):
        return type(self)(self.default_factory, self)

    def __deepcopy__(self, memo):
        import copy
        return type(self)(self.default_factory, copy.deepcopy(self.items()))

    def __repr__(self):
        return b'OrderedDefaultDict(%s, %s)' % (self.default_factory, OrderedDict.__repr__(self))