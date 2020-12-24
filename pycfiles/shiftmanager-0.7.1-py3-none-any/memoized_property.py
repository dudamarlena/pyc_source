# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mikenawood/Code/shiftmanager/build/lib/shiftmanager/memoized_property.py
# Compiled at: 2017-11-07 15:04:11
from functools import wraps

def memoized_property(fget):
    """
    Return a property attribute for new-style classes
    that only calls its getter on the first access.
    The result is stored and on subsequent accesses is returned,
    preventing the need to call the getter any more.

    Example::
        >>> class C(object):
        ...     load_name_count = 0
        ...     @memoized_property
        ...     def name(self):
        ...         "name's docstring"
        ...         self.load_name_count += 1
        ...         return "the name"
        >>> c = C()
        >>> c.load_name_count
        0
        >>> c.name
        'the name'
        >>> c.load_name_count
        1
        >>> c.name
        'the name'
        >>> c.load_name_count
        1
    """
    attr_name = ('_{0}').format(fget.__name__)

    @wraps(fget)
    def fget_memoized(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fget(self))
        return getattr(self, attr_name)

    return property(fget_memoized)