# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Repos\Libraries\dynamicmethod\dynamicmethod\custom_class_method.py
# Compiled at: 2018-03-12 21:31:02
# Size of source mod 2**32: 1064 bytes
"""
Class decorator that can also use instance values.

Example:

        ..code-block :: python

            >>> import dynamicmethod
            >>> class Example(object):
            >>>     x = 0
            >>>
            >>>     def __init__(self, x=0):
            >>>         self.x = x
            >>>
            >>>     @dynamicmethod
            >>>     def get_x(self):
            >>>         return self.x
            >>>
            >>> print(Example.get_x())
            >>> ex = Example()
            >>> ex.x = 5
            >>> print(ex.get_x())

"""

class dynamicmethod(object):
    __doc__ = 'Decorator to create a class method that will also be an instance method.'

    def __init__(self, func):
        self.__func__ = func

    def __get__(self, inst, cls):
        if inst is not None:
            bound_method = self.__func__.__get__(inst, cls)
            return bound_method
        else:
            return self.__func__.__get__(cls, cls)