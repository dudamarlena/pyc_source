# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eddington/app_util.py
# Compiled at: 2020-04-04 13:10:47
# Size of source mod 2**32: 564 bytes
from eddington_core import linear, FitFunctionsRegistry, FitFunction

def split_function_and_parameters(func):
    if func is None:
        return (
         None, [])
    if isinstance(func, str):
        return (
         func, [])
    if len(func) == 0:
        return (
         None, [])
    return (
     func[0], func[1:])


def load_func(func_name, func_parameters, costumed):
    if func_name is not None:
        return (FitFunctionsRegistry.load)(func_name, *func_parameters)
    if costumed is not None:
        return FitFunction.from_string(syntax_string=costumed, save=False)
    return linear