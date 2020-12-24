# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/keyring/keyring/util/properties.py
# Compiled at: 2020-01-10 16:25:34
# Size of source mod 2**32: 1347 bytes
from collections import abc
__metaclass__ = type

class ClassProperty(property):
    __doc__ = "\n    An implementation of a property callable on a class. Used to decorate a\n    classmethod but to then treat it like a property.\n\n    Example:\n\n    >>> class MyClass:\n    ...    @ClassProperty\n    ...    @classmethod\n    ...    def skillz(cls):\n    ...        return cls.__name__.startswith('My')\n    >>> MyClass.skillz\n    True\n    >>> class YourClass(MyClass): pass\n    >>> YourClass.skillz\n    False\n    "

    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()


class NonDataProperty:
    __doc__ = 'Much like the property builtin, but only implements __get__,\n    making it a non-data property, and can be subsequently reset.\n\n    See http://users.rcn.com/python/download/Descriptor.htm for more\n    information.\n\n    >>> class X:\n    ...   @NonDataProperty\n    ...   def foo(self):\n    ...     return 3\n    >>> x = X()\n    >>> x.foo\n    3\n    >>> x.foo = 4\n    >>> x.foo\n    4\n    '

    def __init__(self, fget):
        if not fget is not None:
            raise AssertionError('fget cannot be none')
        elif not isinstance(fget, abc.Callable):
            raise AssertionError('fget must be callable')
        self.fget = fget

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        else:
            return self.fget(obj)