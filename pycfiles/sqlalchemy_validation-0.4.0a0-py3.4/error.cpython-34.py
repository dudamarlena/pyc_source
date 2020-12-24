# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sqlalchemy_validation/error.py
# Compiled at: 2015-12-31 01:46:45
# Size of source mod 2**32: 4652 bytes
"""
"""
from collections import UserDict

class BaseValidationError(Exception):
    __doc__ = 'Generic Error Class.\n    '


class ValidationError(UserDict, BaseValidationError):
    __doc__ = '\n    key: A tuple of column names.\n    value: A BaseValidationError instance.\n    '

    def __init__(self, *args, **kwargs):
        """
        """
        init_dict = kwargs.pop('init_dict_', {})
        UserDict.__init__(self, dict=init_dict, **kwargs)
        BaseValidationError.__init__(self, *args)

    def __str__(self):
        return 'The following Errors have raised!\n\n{}'.format('\n\n'.join('{}\n{}'.format(key, val) for key, val in self.items()))


class ValidatesError(BaseValidationError):
    __doc__ = '\n    Attributes:\n      model: A Model instance.\n      column: A Column instance.\n      value: A value tried to set.\n      model_name: A Model name.\n    '

    def __init__(self, model, column, value):
        """
        Args:
          model: A Model instance.
          column: A Column instance.
          value: A value tried to set.
          model_name: A Model name.
        """
        self.model = model
        self.column = column
        self.value = value
        self.model_name = model.__class__.__name__
        super(ValidatesError, self).__init__()


class EnumError(ValidatesError):
    __doc__ = 'Enum Constraint.\n    '

    def __str__(self):
        return 'EnumError!\nTable.column: {}.{}\nEnum: {}\nvalue: {}'.format(self.model_name, self.column.name, self.column.type.enums, self.value)


class TooShortError(ValidatesError):
    __doc__ = 'Length Constraint.\n    '

    def __str__(self):
        return 'TooShortError!\nTable.column: {}.{}\nlength limitation: {}\nvalue(length): {}({})'.format(self.model_name, self.column.name, self.column.length, self.value, len(self.value))


class TooLongError(ValidatesError):
    __doc__ = 'Length Constraint.\n    '

    def __str__(self):
        return 'TooLongError!\nTable.column: {}.{}\nlength limitation: {}\nvalue(length): {}({})'.format(self.model_name, self.column.name, self.column.length, self.value, len(self.value))


class OverMaxError(ValidatesError):
    __doc__ = 'Size Constraint.\n    '

    def __str__(self):
        return 'OverMaxError!\nTable.column: {}.{}\nsize limitation: {}\nvalue: {}'.format(self.model_name, self.column.name, self.column.size, self.value)


class OverMinError(ValidatesError):
    __doc__ = 'Size Constraint.\n    '

    def __str__(self):
        value = getattr(self.model, self.column.name)
        return 'OverMinError!\nTable.column: {}.{}\nsize limitation: {}\nvalue: {}'.format(self.model_name, self.column.name, self.column.size, self.value)


class NotNullError(ValidatesError):
    __doc__ = 'Not Null Constraint.\n\n    Attributes:\n      model: A Model instance.\n      column: A Column instance.\n      model_name: A Model name.\n    '

    def __init__(self, model, column):
        """
        Args:
          model: A Model instance.
          column: A Column instance.
          model_name: A Model name.
        """
        super(NotNullError, self).__init__(model, column, None)

    def __str__(self):
        return "NotNullError!\n{}.{} can't be None.".format(self.model_name, self.column.name)


class InvalidTypeError(ValidatesError):
    __doc__ = 'Type Constraint.\n    '

    def __str__(self):
        return 'InvalidTypeError!\nTable.column: {}.{}\nexpected type: {}\nvalue(type): {}({})'.format(self.model_name, self.column.name, self.column.type.python_type, self.value, type(self.value))


class EmailError(ValidatesError):
    __doc__ = 'Email Format Constraint.\n    '

    def __str__(self):
        return 'EmailError!\nTable.column: {}.{}\nvalue: {}'.format(self.model_name, self.column.name, self.value)


class RegExpError(ValidatesError):
    __doc__ = 'RegExp Constraint.\n    '

    def __str__(self):
        return 'RegExpError!\nTable.column: {}.{}\nRegExp: {}\nvalue: {}'.format(self.model_name, self.column.name, self.column.regexp, self.value)