# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/schema/util.py
# Compiled at: 2018-12-02 18:51:48
# Size of source mod 2**32: 1579 bytes
"""Convienent utilities."""
from collections import OrderedDict as odict
from warnings import warn
from .declarative import Container, Attribute

class Attributes(Container):
    __doc__ = 'Easily access the known declarative attributes of an object, preserving definition order.'
    only = Attribute(default=None)

    def __get__(self, obj, cls=None):
        if not obj:
            obj = cls
        else:
            return self.only or obj.__attributes__.copy()
        return odict(((k, v) for k, v in obj.__attributes__.items() if isinstance(v, self.only)))


def ensure_tuple(length, tuples):
    """Yield `length`-sized tuples from the given collection.
        
        Will truncate longer tuples to the desired length, and pad using the leading element if shorter.
        """
    for elem in tuples:
        if not isinstance(elem, (tuple, list)):
            yield (
             elem,) * length
            continue
        l = len(elem)
        if l == length:
            yield elem
        elif l > length:
            yield tuple(elem[:length])
        elif l < length:
            yield (
             elem[0],) * (length - l) + tuple(elem)


class DeclarativeAttributes(Attributes):
    __doc__ = 'DeclarativeAttributes is now called Attributes.'

    def __init__(self, *args, **kw):
        warn('Use of DeclarativeAttributes is deprecated, use Attributes instead.', DeprecationWarning)
        (super().__init__)(*args, **kw)