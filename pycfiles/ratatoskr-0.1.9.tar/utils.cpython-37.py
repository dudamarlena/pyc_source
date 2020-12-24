# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ngergo/Workspaces/Nordcloud/ratatoskr/ratatoskr/utils.py
# Compiled at: 2019-03-20 06:58:46
# Size of source mod 2**32: 1404 bytes
import sys
from functools import wraps

def args_to_dict(func, args):
    """
        Returns argument names as values as key-value pairs.

        @input `func` that is a function object
        @input `args` argument list that the functions is called with
    """
    if sys.version_info >= (3, 0):
        arg_count = func.__code__.co_argcount
        arg_names = func.__code__.co_varnames[:arg_count]
    else:
        arg_count = func.func_code.co_argcount
        arg_names = func.func_code.co_varnames[:arg_count]
    arg_value_list = list(args)
    arguments = dict(((arg_name, arg_value_list[i]) for i, arg_name in enumerate(arg_names) if i < len(arg_value_list)))
    return arguments


def merge_args_with_kwargs(args_dict, kwargs_dict):
    """
        Merge args with kwargs.
    """
    ret = args_dict.copy()
    ret.update(kwargs_dict)
    return ret


def doublewrap(func):
    """
    a decorator decorator, allowing the decorator to be used as:
    @decorator(with, arguments, and=kwargs)
    or
    @decorator
    """

    @wraps(func)
    def new_dec(*args, **kwargs):
        if len(args) == 1:
            if len(kwargs) == 0:
                if callable(args[0]):
                    return func(args[0])
        return lambda realf: func(realf, *args, **kwargs)

    return new_dec