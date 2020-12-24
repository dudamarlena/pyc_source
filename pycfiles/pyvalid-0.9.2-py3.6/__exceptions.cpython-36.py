# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pyvalid/__exceptions.py
# Compiled at: 2018-06-02 14:20:59
# Size of source mod 2**32: 1077 bytes


class InvalidArgumentNumberError(ValueError):
    __doc__ = 'Raised when the number or position of arguments supplied to a function\n    is incorrect.\n    '

    def __init__(self, func_name):
        self.error = 'Invalid number or position of arguments for {}()'.format(func_name)

    def __str__(self):
        return self.error


class ArgumentValidationError(ValueError):
    __doc__ = 'Raised when the type of an argument to a function is not what it\n    should be.\n    '

    def __init__(self, arg_num, func_name, actual_value, accepted_arg_values):
        self.error = 'The {} argument of {}() is {} and not in a {}'.format(arg_num, func_name, actual_value, accepted_arg_values)

    def __str__(self):
        return self.error


class InvalidReturnType(ValueError):
    __doc__ = 'Raised when the return value is the wrong type.\n    '

    def __init__(self, return_type, func_name):
        self.error = 'Invalid return type {} for {}()'.format(return_type, func_name)

    def __str__(self):
        return self.error