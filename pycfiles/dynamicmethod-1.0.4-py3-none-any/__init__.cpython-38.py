# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Repos\Libraries\dynamicmethod\dynamicmethod\__init__.py
# Compiled at: 2020-05-03 23:05:00
# Size of source mod 2**32: 1200 bytes
from .__meta__ import version as __version__
import sys, types
from .custom_class_method import dynamicmethod

class DynamicModule(types.ModuleType):
    __doc__ = "Custom callable module.\n\n    This can be called by the following example.\n\n    Example:\n\n        ..code-block :: python\n\n            >>> import dynamicmethod\n            >>> class Example(object):\n            >>>     x = 0\n            >>>\n            >>>     def __init__(self, x=0):\n            >>>         self.x = x\n            >>>\n            >>>     @dynamicmethod\n            >>>     def get_x(self):\n            >>>         return self.x\n            >>>\n            >>> print(Example.get_x())\n            >>> ex = Example()\n            >>> ex.x = 5\n            >>> print(ex.get_x())\n\n    This class module is implemented so you don't have to call\n    ..code-block :: python\n\n        >>> import dynamicmethod\n        >>> dynamicmethod.dynamicmethod\n\n    "
    __version__ = __version__
    dynamicmethod = dynamicmethod

    def __call__(self, function):
        return self.dynamicmethod(function)


sys.modules[__name__] = DynamicModule(__name__)