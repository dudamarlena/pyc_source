# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xix/utils/container.py
# Compiled at: 2006-04-15 16:22:15
"""container - base implementation of IContainer -
a dictionaryish object with ordered entries.
"""
from UserDict import UserDict
from zope.interface import implements
from xix.utils.interfaces import IContainer

class Container(UserDict):
    """Container is a simple provider of IContainer:

    >>> from zope.interface.verify import verifyClass, verifyObject
    >>> verifyClass(IContainer, Container)
    True

    Creating a Container:

    >>> container = Container()
    >>> verifyObject(IContainer, container)
    True
    """
    __module__ = __name__
    implements(IContainer)

    def __init__(self):
        UserDict.__init__(self)
        self.entries = []

    def __setitem__(self, key, value):
        """Example:

        >>> container = Container()
        >>> container['a'] = 1 # first in order
        >>> container['b'] = 2 # ...
        >>> container['c'] = 3 # last in order
        >>> container.entries
        [('a', 1), ('b', 2), ('c', 3)]

        >>> container['b'] = 5
        >>> container.entries # should retain order
        [('a', 1), ('b', 5), ('c', 3)]
        """
        entries = self.entries
        if not self.data.has_key(key):
            entries.append((key, value))
        else:
            entry = [ kv for kv in entries if kv[0] == key ][0]
            entries[entries.index(entry)] = (
             key, value)
        UserDict.__setitem__(self, key, value)

    def __iter__(self):
        """Example:

        >>> container = Container()
        >>> for c in 'a', 'b', 'c':
        ...    container[c] = ord(c)
        ...
        >>> for entry in container:
        ...    print entry,
        ...
        ('a', 97) ('b', 98) ('c', 99)
        """
        return iter(self.entries)