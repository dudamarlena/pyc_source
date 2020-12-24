# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/utility/reflection.py
# Compiled at: 2007-12-02 16:26:55
from salamoia.utility.cache import Cache
import sys

class ClassNamed(object):
    """
    Helper class which can return a class object
    from a string and compute a string from the class name
    hiding the difference between old-style and new-style
    python classes.
    """
    __module__ = __name__
    namedCache = Cache()

    def __new__(cls, name):
        """
        When a ClassNamed object is istantiated
        the real object returned is a the class object
        matching the argument.

        ClassNamed('h2o.user.User')(arg1, arg2, arg3)

        returns a User object construted with arg1, arg2, arg3
        arguments
        """
        if name not in cls.namedCache:
            c = cls._findClass(name)
            cls.namedCache[name] = c
            return c
        return cls.namedCache[name]

    @classmethod
    def _findClass(cls, name):
        name = cls.classFullName(name)
        modulePath = name.split('.')
        moduleName = ('.').join(modulePath[0:-1])
        className = modulePath[(-1)]
        if moduleName:
            __import__(moduleName)
            return getattr(sys.modules[moduleName], className)
        else:
            return getattr(sys.modules['__builtin__'], className)

    @classmethod
    def classFullName(self, cls):
        """
        return the class name from a class hiding the
        difference between old-style and new-style python classes.

        the class full name is composed of it's package and
        module name.
        """
        name = str(cls)
        if name.startswith('<class'):
            name = name.split("'")[1]
        return name

    @classmethod
    def className(self, cls):
        """
        return only the class name, stripping all package and module
        information
        """
        full = self.classFullName(cls)
        return full.split('.')[(-1)]


from salamoia.tests import *
runDocTests()