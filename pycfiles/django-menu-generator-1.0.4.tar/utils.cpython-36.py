# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/miltonln/Proyectos/django-menu-generator/menu_generator/utils.py
# Compiled at: 2018-01-31 09:25:36
# Size of source mod 2**32: 420 bytes
from importlib import import_module

def get_callable(func_or_path):
    """
    Receives a dotted path or a callable, Returns a callable or None
    """
    if callable(func_or_path):
        return func_or_path
    else:
        module_name = '.'.join(func_or_path.split('.')[:-1])
        function_name = func_or_path.split('.')[(-1)]
        _module = import_module(module_name)
        func = getattr(_module, function_name)
        return func