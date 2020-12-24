# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sigma/core/model.py
# Compiled at: 2016-01-24 09:28:04
# Size of source mod 2**32: 1853 bytes
from .error import ErrorContainer, UnitError
from .field import Field

class ModelMeta(type):
    __doc__ = ' A Model Meta Class.\n    '

    def __new__(cls, classname, bases, namespace, **kwargs):
        fields = {}
        result = type.__new__(cls, classname, bases, namespace, **kwargs)
        for key, field in namespace.items():
            if key.startswith('_'):
                continue
            if isinstance(field, Field):
                fields[key] = field
                field.__Model__ = result
                field.__model__ = None
                field.__model_name__ = classname
                if not field._name:
                    field._name = key
                else:
                    continue

        result.__fields__ = fields
        return result


class Model(object, metaclass=ModelMeta):
    __doc__ = '\n    Attrs:\n      __fields__: A list of Field instances.\n    '

    def __init__(self, *args, **kwargs):
        """
        Args:
          *args:
            arg[0]: True or False.
          **kwargs:
            key: An option name.
            value: An option's setting value.
        """
        self.__values__ = dict((key, None) for key in self.__fields__)
        for key, field in self.__fields__.items():
            field.__model__ = self

        if args and args[0]:
            for key, value in kwargs.items():
                setattr(self, key, value)

        else:
            errors = ErrorContainer()
            for key, value in kwargs.items():
                try:
                    setattr(self, key, value)
                except UnitError as e:
                    errors[key] = e

        if errors:
            raise errors

    def __call__(self, *args, **kwargs):
        """
        Args:
          Equal to __init__ constructor.
        Returns:
          self
        """
        self.__init__(*args, **kwargs)
        return self