# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /uri/bucket.py
# Compiled at: 2018-10-22 09:58:17
# Size of source mod 2**32: 1953 bytes
from __future__ import unicode_literals
from collections import ItemsView, KeysView, MutableMapping, MutableSequence, ValuesView, deque, namedtuple
from .compat import SENTINEL, py2, quote_plus, str, unquote_plus

class Bucket(object):
    __doc__ = 'A bucket is a mutable container for an optionally named scalar value.'
    __slots__ = ('name', 'value', 'sep', 'valid')

    def __init__(self, name, value='', sep='=', strict=False):
        self.valid = True
        self.sep = sep
        if not value:
            if isinstance(name, str):
                if name.count(sep) > 1:
                    if strict:
                        raise ValueError("Multiple occurrences of separator {!r} in: '{!s}'".format(sep, name))
                    self.valid = False
                name, value = self.split(name)
            else:
                if isinstance(name, Bucket):
                    name, value = name.name, name.value
                else:
                    name, value = name
        self.name = name
        self.value = value

    def __eq__(self, other):
        return str(self) == str(other)

    def __ne__(self, other):
        return not str(self) == str(other)

    def split(self, string):
        name, match, value = string.partition(self.sep)
        name = unquote_plus(name)
        value = unquote_plus(value)
        return (
         name if match else None, value if match else name)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, str(self))

    if py2:

        def __repr__(self):
            return '{}({})'.format(self.__class__.__name__, str(self)).encode('unicode-escape')

    def __iter__(self):
        if self.name is not None:
            yield self.name
        yield self.value

    def __len__(self):
        if self.name is None:
            return 1
        return 2

    def __str__(self):
        iterator = (quote_plus(i).replace('%3F', '?').replace('%2F', '/') for i in self) if self.valid else self
        return self.sep.join(iterator)

    if py2:
        __unicode__ = __str__
        del __str__