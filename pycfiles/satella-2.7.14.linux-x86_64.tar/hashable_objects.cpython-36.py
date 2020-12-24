# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.6.7/lib/python3.6/site-packages/satella/coding/structures/hashable_objects.py
# Compiled at: 2020-04-25 10:46:39
# Size of source mod 2**32: 507 bytes
from .proxy import Proxy

class HashableWrapper(Proxy):
    __doc__ = '\n    A class that makes given objects hashable by their id.\n\n    Note that this class will return a proxy to the object, and not the object itself.\n\n    Use like:\n\n    >>> class NotHashable:\n    >>>     def __init__(self, a):\n    >>>         self.a = a\n    >>> a = HashableWrapper(NotHashable(5))\n    >>> assert a.a == 5\n    >>> a.a = 4\n    >>> assert a.a == 4\n    '
    __slots__ = ()

    def __hash__(self):
        return hash(id(self))