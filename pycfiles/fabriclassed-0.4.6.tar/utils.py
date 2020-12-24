# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: fabriclassed/utils.py
# Compiled at: 2015-02-27 04:15:18
import inspect, sys

def add_class_methods_as_module_level_functions_for_fabric(instance, module_name):
    """
    Utility to take the methods with prefix 'fab_' of the class instance `instance`,
    and add them as functions to a module `module_name`, so that Fabric
    can find and call them. Call this at the bottom of a module after
    the class definition. Returns a list of method for __all__ variable,
    otherwise command 'fab -l' will show extra commands.
    """
    module_obj = sys.modules[module_name]
    method_names_list = []
    for method in inspect.getmembers(instance, predicate=inspect.ismethod):
        method_name = method[0]
        if method_name.startswith('fab_'):
            func = getattr(instance, method_name)
            method_name = method_name.replace('fab_', '')
            setattr(module_obj, method_name, func)
            method_names_list += [method_name]

    return method_names_list