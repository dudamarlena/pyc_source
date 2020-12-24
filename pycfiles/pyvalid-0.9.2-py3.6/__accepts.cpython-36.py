# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pyvalid/__accepts.py
# Compiled at: 2018-06-02 18:05:00
# Size of source mod 2**32: 6217 bytes
from collections import Callable
from types import MethodType
from functools import wraps
import sys
if sys.version_info < (3, 0, 0):
    from inspect import getargspec
else:
    from inspect import getfullargspec as getargspec
from pyvalid.__exceptions import InvalidArgumentNumberError, ArgumentValidationError
from pyvalid.switch import is_enabled

class Accepts(Callable):
    __doc__ = 'A decorator to validate types of input parameters for a given function.\n    '

    def __init__(self, *accepted_arg_values, **accepted_kwargs_values):
        self.accepted_arg_values = accepted_arg_values
        self.accepted_kwargs_values = accepted_kwargs_values
        self.accepted_args = list()
        self.optional_args = list()

    def __call__(self, func):

        @wraps(func)
        def decorator_wrapper(*func_args, **func_kwargs):
            perform_validation = all((
             is_enabled(),
             self.accepted_arg_values or self.accepted_kwargs_values))
            if perform_validation:
                self.accepted_args[:] = list()
                self.optional_args[:] = list()
                args_info = getargspec(func)
                self._Accepts__scan_func(args_info)
                self._Accepts__validate_args(func.__name__, func_args, func_kwargs)
            return func(*func_args, **func_kwargs)

        return decorator_wrapper

    def __wrap_accepted_val(self, value):
        """Wrap accepted value in the list if yet not wrapped.
        """
        if isinstance(value, tuple):
            value = list(value)
        else:
            if not isinstance(value, list):
                value = [
                 value]
        return value

    def __scan_func(self, args_info):
        """Collect information about accepted arguments in following format:
            (
                (<argument name>, <accepted types and values>),
                (<argument name>, <accepted types and values>),
                ...
            )

        Args:
            args_info (inspect.FullArgSpec): Information about function
                arguments.
        """
        for i, accepted_arg_vals in enumerate(self.accepted_arg_values):
            accepted_arg_vals = self._Accepts__wrap_accepted_val(accepted_arg_vals)
            if args_info.defaults:
                def_range = len(args_info.defaults) - len(args_info.args[i:])
                if def_range >= 0:
                    self.optional_args.append(i)
                    accepted_value = args_info.defaults[def_range]
                    accepted_arg_vals.append(accepted_value)
            if len(args_info.args) > i:
                arg_name = args_info.args[i]
            else:
                arg_name = None
                self.optional_args.append(i)
            self.accepted_args.append((arg_name, accepted_arg_vals))

        for arg_name, accepted_arg_vals in self.accepted_kwargs_values.items():
            accepted_arg_vals = self._Accepts__wrap_accepted_val(accepted_arg_vals)
            i = len(self.accepted_args)
            self.optional_args.append(i)
            self.accepted_args.append((arg_name, accepted_arg_vals))

    def __validate_args(self, func_name, args, kwargs):
        """Compare value of each required argument with list of
        accepted values.

        Args:
            func_name (str): Function name.
            args (list): Collection of the position arguments.
            kwargs (dict): Collection of the keyword arguments.

        Raises:
            InvalidArgumentNumberError: When position or count of the arguments
                is incorrect.
            ArgumentValidationError: When encountered unexpected argument
                value.
        """
        from pyvalid.validators import Validator
        for i, (arg_name, accepted_values) in enumerate(self.accepted_args):
            if i < len(args):
                value = args[i]
            else:
                if arg_name in kwargs:
                    value = kwargs[arg_name]
                else:
                    if i in self.optional_args:
                        continue
                    else:
                        raise InvalidArgumentNumberError(func_name)
            is_valid = False
            for accepted_val in accepted_values:
                is_validator = isinstance(accepted_val, Validator) or isinstance(accepted_val, MethodType) and hasattr(accepted_val, '__func__') and isinstance(accepted_val.__func__, Validator)
                if is_validator:
                    is_valid = accepted_val(value)
                else:
                    if isinstance(accepted_val, type):
                        is_valid = isinstance(value, accepted_val)
                    else:
                        is_valid = value == accepted_val
                    if is_valid:
                        break

            if not is_valid:
                ord_num = self._Accepts__ordinal(i + 1)
                raise ArgumentValidationError(ord_num, func_name, value, accepted_values)

    def __ordinal(self, num):
        """Returns the ordinal number of a given integer, as a string.
        eg. 1 -> 1st, 2 -> 2nd, 3 -> 3rd, etc.
        """
        if 10 <= num % 100 < 20:
            return str(num) + 'th'
        else:
            ord_info = {1:'st', 
             2:'nd',  3:'rd'}.get(num % 10, 'th')
            return '{}{}'.format(num, ord_info)