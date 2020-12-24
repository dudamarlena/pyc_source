# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/apryor/projects/flaskerize/flaskerize/custom_functions.py
# Compiled at: 2019-08-17 08:28:56
# Size of source mod 2**32: 446 bytes
from typing import List, Callable, Any

def make_register_custom_function() -> Callable:
    funcs = []

    def register_custom_function(func):
        funcs.append(func)
        return func

    register_custom_function.funcs = funcs
    return register_custom_function


register_custom_function = make_register_custom_function()
registered_funcs = register_custom_function.funcs