# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-4yaip7h6/keyring/keyring/util/properties.py
# Compiled at: 2016-12-29 05:40:26
# Size of source mod 2**32: 1337 bytes
from collections import Callable

class ClassProperty(property):
    __doc__ = "\n    An implementation of a property callable on a class. Used to decorate a\n    classmethod but to then treat it like a property.\n\n    Example:\n\n    >>> class MyClass:\n    ...    @ClassProperty\n    ...    @classmethod\n    ...    def skillz(cls):\n    ...        return cls.__name__.startswith('My')\n    >>> MyClass.skillz\n    True\n    >>> class YourClass(MyClass): pass\n    >>> YourClass.skillz\n    False\n    "

    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()


class NonDataProperty(object):
    __doc__ = 'Much like the property builtin, but only implements __get__,\n    making it a non-data property, and can be subsequently reset.\n\n    See http://users.rcn.com/python/download/Descriptor.htm for more\n    information.\n\n    >>> class X(object):\n    ...   @NonDataProperty\n    ...   def foo(self):\n    ...     return 3\n    >>> x = X()\n    >>> x.foo\n    3\n    >>> x.foo = 4\n    >>> x.foo\n    4\n    '

    def __init__(self, fget):
        assert fget is not None, 'fget cannot be none'
        assert isinstance(fget, Callable), 'fget must be callable'
        self.fget = fget

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return self.fget(obj)