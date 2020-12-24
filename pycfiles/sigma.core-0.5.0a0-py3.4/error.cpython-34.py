# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sigma/core/error.py
# Compiled at: 2016-01-23 17:25:07
# Size of source mod 2**32: 1940 bytes
"""
"""
from collections import UserDict

class SigmaError(Exception):
    __doc__ = "Generic Error Class.\n    All sigma's error classes are this subclasses.\n    "


class ErrorContainer(UserDict, SigmaError):
    __doc__ = ' Contain multiple errors.\n\n    key: A field name.\n    value: A SigmaError instance.\n\n    Example:\n      from sigma.core import Model, ErrorContainer\n      from sigma.standard import Field\n\n      class User(Model):\n          id = Field(type=int)\n          name = Field(length=(3, None))\n\n      try:\n          user = User(id="foo", name="12")\n      except ErrorContainer as errors:\n          for key, error in errors.items():\n              print(key, type(error))\n              # id, InvalidTypeError\n              # name, TooShortError\n    '

    def __init__(self, **kwargs):
        """
        """
        UserDict.__init__(self, **kwargs)

    def __str__(self):
        return 'The following Errors have raised!\n\n{}'.format('\n\n'.join('{}\n{}'.format(key, val) for key, val in self.items()))


class UnitError(SigmaError):
    __doc__ = '\n    Attributes:\n      field: A Field instance.\n      option: A option instance.\n      value: A value tried to set.\n      model_name: A Model name.\n    '

    def __init__(self, field, option, value):
        """
        Args:
          field: A Field instance.
          option: A option instance.
          value: A value tried to set.
        """
        self.field = field
        self.option = option
        self.value = value
        self.model_name = field.__model_name__
        super(UnitError, self).__init__()

    def __str__(self):
        return '{}!\nModel: {}\nField: {}\noption: {}\nvalue: {}'.format(self.__class__.__name__, self.model_name, self.field._name, self.option.name, self.value)