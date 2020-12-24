# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pyvalid/__returns.py
# Compiled at: 2018-06-02 17:58:45
# Size of source mod 2**32: 1779 bytes
from collections import Callable
from types import MethodType
from pyvalid.__exceptions import InvalidReturnType
from pyvalid.switch import is_enabled
from functools import wraps

class Returns(Callable):
    __doc__ = 'A decorator to validate the returns value of a given function.\n    '

    def __init__(self, *accepted_returns_values):
        self.accepted_returns_values = accepted_returns_values

    def __call__(self, func):

        @wraps(func)
        def decorator_wrapper(*func_args, **func_kwargs):
            from pyvalid.validators import Validator
            returns_val = func(*func_args, **func_kwargs)
            if is_enabled():
                if self.accepted_returns_values:
                    is_valid = False
                    for accepted_val in self.accepted_returns_values:
                        if isinstance(accepted_val, (Validator, MethodType)):
                            if isinstance(accepted_val, Validator):
                                is_valid = accepted_val(returns_val)
                            else:
                                if isinstance(accepted_val, MethodType):
                                    if hasattr(accepted_val, '__func__'):
                                        if isinstance(accepted_val.__func__, Validator):
                                            is_valid = accepted_val(returns_val)
                                else:
                                    if isinstance(accepted_val, type):
                                        is_valid = isinstance(returns_val, accepted_val)
                                    else:
                                        is_valid = returns_val == accepted_val
                                    if is_valid:
                                        break

                    if not is_valid:
                        raise InvalidReturnType(type(returns_val), func.__name__)
            return returns_val

        return decorator_wrapper