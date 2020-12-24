# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.6.7/lib/python3.6/site-packages/satella/coding/structures/hashable_objects.py
# Compiled at: 2020-04-14 13:42:23
# Size of source mod 2**32: 421 bytes


def HashableWrapper(obj):
    """
    A decorator that makes given objects hashable by their id.

    Use like:

    >>> class NotHashable:
    >>>     def __init__(self, a):
    >>>         self.a = a
    >>> a = HashableWrapper(NotHashable(5))
    >>> assert a.a == 5
    >>> a.a = 4
    >>> assert a.a == 4
    """
    if not hasattr(obj, '__hash__'):
        obj.__hash__ = lambda self: hash(id(self))
    return obj