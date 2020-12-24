# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/property.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 4485 bytes
__doc__ = 'PyAMS_utils.property module\n\nThis module is used to define:\n - a cached property; this read-only property is evaluated only once; it\'s value is stored into\n   object\'s attributes, and so should be freed with the object (so it should behave like a\n   Pyramid\'s "reify" decorator, but we have kept it for compatibility of existing code)\n - a class property; this decorator is working like a classic property, but can be assigned to a\n   class; to support class properties, this class also have to decorated with the\n   "classproperty_support" decorator\n\n    >>> from pyams_utils.property import cached_property\n\n    >>> class ClassWithCache:\n    ...     \'\'\'Class with cache\'\'\'\n    ...     @cached_property\n    ...     def cached_value(self):\n    ...         print("This is a cached value")\n    ...         return 1\n\n    >>> obj = ClassWithCache()\n    >>> obj.cached_value\n    This is a cached value\n    1\n\nOn following calls, cached property method shouldn\'t be called again:\n\n    >>> obj.cached_value\n    1\n\nClass properties are used to define properties on class level:\n\n    >>> from pyams_utils.property import classproperty, classproperty_support\n\n    >>> @classproperty_support\n    ... class ClassWithProperties:\n    ...     \'\'\'Class with class properties\'\'\'\n    ...\n    ...     class_attribute = 1\n    ...\n    ...     @classproperty\n    ...     def my_class_property(cls):\n    ...         return cls.class_attribute\n\n    >>> ClassWithProperties.my_class_property\n    1\n'
__docformat__ = 'restructuredtext'

class cached_property:
    """cached_property"""

    def __init__(self, fget, doc=None):
        self.fget = fget
        self.__doc__ = doc or fget.__doc__
        self.__name__ = fget.__name__
        self.__module__ = fget.__module__

    def __get__(self, obj, cls):
        if obj is None:
            return self
        obj.__dict__[self.__name__] = result = self.fget(obj)
        return result


class classproperty:
    """classproperty"""

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        if doc is None and fget is not None:
            doc = fget.__doc__
        self.__doc__ = doc

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError('Unreadable attribute')
        return self.fget(obj.__class__)

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("Can't set attribute")
        self.fset(obj.__class__, value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("Can't delete attribute")
        self.fdel(obj.__class__)

    def getter(self, fget):
        """Property getter"""
        return type(self)(fget, self.fset, self.fdel, self.__doc__)

    def setter(self, fset):
        """Property setter"""
        return type(self)(self.fget, fset, self.fdel, self.__doc__)

    def deleter(self, fdel):
        """Property deleter"""
        return type(self)(self.fget, self.fset, fdel, self.__doc__)


def classproperty_support(cls):
    """Class decorator to add metaclass to a class.

    Metaclass uses to add descriptors to class attributes
    """

    class Meta(type):
        """classproperty_support.<locals>.Meta"""
        pass

    for name, obj in vars(cls).items():
        if isinstance(obj, classproperty):
            setattr(Meta, name, property(obj.fget, obj.fset, obj.fdel))

    class Wrapper(cls, metaclass=Meta):
        """classproperty_support.<locals>.Wrapper"""
        pass

    return Wrapper