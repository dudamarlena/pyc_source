# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ube/concerns/aspect_utilities.py
# Compiled at: 2013-08-25 16:07:25
"""
Created on Nov 6, 2012

@author: Nicklas Boerjesson
"""
from inspect import getfullargspec

def alter_function_parameter_and_call(function_object, args, kwargs, name, value, err_if_not_set):
    """changes an argument value of a given function and call said function"""
    argspec = getfullargspec(function_object)
    try:
        arg_idx = argspec.args.index(name)
    except:
        raise Exception(err_if_not_set)

    largs = list(args)
    largs.pop(arg_idx)
    largs.insert(arg_idx, value)
    new_args = tuple(largs)
    return function_object(*new_args, **kwargs)