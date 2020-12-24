# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/satella/coding/structures/hashable_objects.py
# Compiled at: 2020-04-29 12:14:00
# Size of source mod 2**32: 380 bytes
from .proxy import Proxy

class HashableWrapper(Proxy):
    __doc__ = '\n    A class that makes given objects hashable by their id.\n\n    Note that this class will return a proxy to the object, and not the object itself.\n\n    Use like:\n\n    >>> a = {1:2, 3:4}\n    >>> a = HashableWrapper(a)\n    >>> hash(a)\n    '
    __slots__ = ()

    def __hash__(self):
        return hash(id(self))