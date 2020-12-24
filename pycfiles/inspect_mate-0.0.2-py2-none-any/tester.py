# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/inspect_mate-project/inspect_mate/tester.py
# Compiled at: 2018-09-06 20:36:09
"""
test it's either ``regular attribute``, ``property method``, ``regular method``, 
``static method`` or ``class method``. 
"""
import sys, inspect
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
if PY2:
    getfullargspec = inspect.getargspec
elif PY3:
    getfullargspec = inspect.getfullargspec
else:
    raise ValueError

def is_attribute(klass_or_instance, attr):
    """Test if a value of a class is attribute. (Not a @property style
    attribute)

    example::

        class MyClass(object):
            attribute1 = 1

            class __init__(self):
                self.attribute2 = 1

    :param klass_or_instance: the class
    :param attr: attribute name
    :param value: attribute value
    """
    value = getattr(klass_or_instance, attr)
    if inspect.isroutine(value):
        return False
    else:
        if is_property_method(klass_or_instance, attr):
            return False
        return True


def is_property_method(klass_or_instance, attr):
    """Test if a value of a class is @property style attribute.

    example::

        class MyClass(object):
            @property
            def value(self):
                return 0

    :param klass_or_instance: the class
    :param attr: attribute name
    :param value: attribute value
    """
    if inspect.isclass(klass_or_instance):
        value = getattr(klass_or_instance, attr)
        if inspect.isroutine(value):
            return False
        if isinstance(value, property):
            return True
        return False
    else:
        klass = klass_or_instance.__class__
        try:
            return is_property_method(klass, attr)
        except:
            return False


def is_regular_method(klass_or_instance, attr):
    """Test if a value of a class is regular method.

    example::

        class MyClass(object):
            def execute(self, input_data):
                ...

    :param klass_or_instance: the class
    :param attr: attribute name
    :param value: attribute value
    """
    value = getattr(klass_or_instance, attr)
    if inspect.isroutine(value):
        if isinstance(value, property):
            return False
        args = getfullargspec(value).args
        try:
            if args[0] == 'self':
                return True
        except:
            pass

    return False


def is_static_method(klass_or_instance, attr):
    """Test if a value of a class is static method.

    example::

        class MyClass(object):
            @staticmethod
            def add_two(a, b):
                return a + b

    :param klass_or_instance: the class
    :param attr: attribute name
    :param value: attribute value
    """
    value = getattr(klass_or_instance, attr)
    if inspect.isroutine(value):
        if isinstance(value, property):
            return False
        else:
            args = getfullargspec(value).args
            if len(args) == 0:
                return True
            if args[0] == 'self':
                return False
            return inspect.isfunction(value)

    return False


def is_class_method(klass_or_instance, attr):
    """Test if a value of a class is class method.

    example::

        class MyClass(object):
            @classmethod
            def add_two(cls, a, b):
                return a + b

    :param klass_or_instance: the class
    :param attr: attribute name
    :param value: attribute value
    """
    value = getattr(klass_or_instance, attr)
    if inspect.isroutine(value):
        if isinstance(value, property):
            return False
        else:
            args = getfullargspec(value).args
            if len(args) == 0:
                return inspect.ismethod(value)
            if args[0] == 'self':
                return False
            return inspect.ismethod(value)

    return False


__all__ = [
 'is_attribute',
 'is_property_method',
 'is_regular_method',
 'is_static_method',
 'is_class_method']
if __name__ == '__main__':
    from inspect_mate.tests import Klass, instance