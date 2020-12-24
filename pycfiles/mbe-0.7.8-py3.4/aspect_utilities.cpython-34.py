# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mbe/misc/aspect_utilities.py
# Compiled at: 2015-03-23 03:26:36
# Size of source mod 2**32: 1153 bytes
"""
Created on Nov 6, 2012

@author: Nicklas Börjesson
@node: Utilities to help creating aspects in AOP.
"""
from inspect import getfullargspec

def alter_function_parameter_and_call(function_object, args, kwargs, name, value, err_if_not_set=None):
    """Changes or sets the value of an argument, if present, and calls the function.

    :param function_object: An instance of the called function
    :param args: A list of arguments
    :param kwargs: A dict of keyword arguments
    :param name: Name of the parameter that should be set
    :param value: Value to set that parameter to
    :param err_if_not_set: If is set, raise as error if the argument isn't present.
    :return: The return value of the called function

    """
    argspec = getfullargspec(function_object)
    if name in argspec.args:
        arg_idx = argspec.args.index(name)
        largs = list(args)
        largs.pop(arg_idx)
        largs.insert(arg_idx, value)
        new_args = tuple(largs)
        return function_object(*new_args, **kwargs)
    if err_if_not_set is not None:
        raise Exception(err_if_not_set)
    return function_object(args, kwargs)