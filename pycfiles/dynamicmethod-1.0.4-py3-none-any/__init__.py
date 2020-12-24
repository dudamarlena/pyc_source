# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Repos\Libraries\dynamicmethod\dynamicmethod\__init__.py
# Compiled at: 2018-03-12 21:44:54
import sys, types
from .custom_class_method import dynamicmethod

class DynamicModule(types.ModuleType):
    """Custom callable module.

    This can be called by the following example.

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

    This class module is implemented so you don't have to call
    ..code-block :: python

        >>> import dynamicmethod
        >>> dynamicmethod.dynamicmethod

    """
    dynamicmethod = dynamicmethod

    def __call__(self, function):
        return self.dynamicmethod(function)


sys.modules[__name__] = DynamicModule(__name__)