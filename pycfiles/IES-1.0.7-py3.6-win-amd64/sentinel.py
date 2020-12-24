# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\strategycontainer\utils\sentinel.py
# Compiled at: 2018-01-15 22:32:31
# Size of source mod 2**32: 1729 bytes
import sys
from textwrap import dedent

class _Sentinel(object):
    __doc__ = 'Base class for Sentinel objects.\n    '
    __slots__ = ('__weakref__', )


def is_sentinel(obj):
    return isinstance(obj, _Sentinel)


def sentinel(name, doc=None):
    try:
        value = sentinel._cache[name]
    except KeyError:
        pass
    else:
        if doc == value.__doc__:
            return value
        raise ValueError(dedent('            New sentinel value %r conflicts with an existing sentinel of the\n            same name.\n            Old sentinel docstring: %r\n            New sentinel docstring: %r\n            Resolve this conflict by changing the name of one of the sentinels.\n            ') % (
         name, value.__doc__, doc))

    @object.__new__
    class Sentinel(_Sentinel):
        __doc__ = doc
        __name__ = name

        def __new__(cls):
            raise TypeError('cannot create %r instances' % name)

        def __repr__(self):
            return 'sentinel(%r)' % name

        def __reduce__(self):
            return (
             sentinel, (name, doc))

        def __deepcopy__(self, _memo):
            return self

        def __copy__(self):
            return self

    cls = type(Sentinel)
    try:
        cls.__module__ = sys._getframe(1).f_globals['__name__']
    except (ValueError, KeyError):
        cls.__module__ = None

    sentinel._cache[name] = Sentinel
    return Sentinel


sentinel._cache = {}