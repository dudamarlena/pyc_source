# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sigma/core/field.py
# Compiled at: 2016-01-24 18:35:01
# Size of source mod 2**32: 3791 bytes
from collections import OrderedDict
from types import FunctionType
from .validator import FieldValidator

class option(object):
    __doc__ = '\n    Attrs:\n      name: The option name (Default is "").\n      func: The validation function.\n      kwargs: The keyword arguments of the constructor.\n      required: Whether this option is required (Default is False).\n      value: The option\'s setting value (Default is None).\n      default(option):\n        The option\'s default setting value.\n        This attribute is created when "default" keyword argument\n        is passed to the constructor.\n    '

    def __init__(self, **kwargs):
        """
        Args:
          **kwargs:
            required: Whether this option is required (Default is False).
            default: The option's default setting value.
        """
        self.name = ''
        self.kwargs = kwargs
        self.required = kwargs.get('required', False)
        self.value = None
        if 'default' in kwargs:
            self.default = kwargs['default']

    def __call__(self, func):
        """
        Args:
          name: The option name.
          func: The validation function.
        Returns:
          self
        """
        self.name = func.__name__
        self.func = func
        return self


class FieldMeta(type):
    __doc__ = ' The Meta Class of Field Class.\n    Attrs:\n    '

    @classmethod
    def __prepare__(cls, name, bases, **kwds):
        return OrderedDict()

    def __new__(cls, classname, bases, namespace, **kwargs):
        options = {}
        for key, func in namespace.items():
            if key.startswith('_'):
                continue
            if isinstance(func, option):
                options[key] = func
            if isinstance(func, FunctionType):
                options[key] = option()(func)
                continue

        namespace['__options__'] = options
        namespace.setdefault('__order__', list(options.keys()))
        return type.__new__(cls, classname, bases, namespace, **kwargs)


class Field(object, metaclass=FieldMeta):
    __doc__ = '\n    Attrs:\n      __order__:\n        The list of option names.\n        Validation functions is executed in order of this list.\n      __options__: The list of option instances.\n      __Validator__:\n        A FieldValidator class.\n      __validator__:\n        A __Validator__ instance.\n      __model_name__: A Model name.\n    '
    __Validator__ = FieldValidator

    def __init__(self, *args, **kwargs):
        """
        Args:
          *args:
            args[0]: A field name or list of option names.
            args[1]: A list of option names.
          *kwargs:
            key: An option name.
            value: An option's setting value.
        """
        length = len(args)
        validate_names = []
        if not length:
            self._name = ''
        else:
            if length == 1:
                arg = args[0]
                if isinstance(arg, str):
                    self._name = arg
                else:
                    validate_names = arg
                    self._name = ''
            else:
                self._name = args[0]
                validate_names = args[1]
        self.__args__ = args
        self.__kwargs__ = kwargs
        self._value = None
        self.__model_name__ = ''
        self.__model__ = None
        self.__validator__ = self.__Validator__(self, *validate_names, **kwargs)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = self.__validator__.validate(val)

    def __get__(self, instance, owner):
        if instance:
            return instance.__values__[self._name]
        else:
            return self

    def __set__(self, instance, value):
        instance.__values__[self._name] = self.__validator__.validate(value)