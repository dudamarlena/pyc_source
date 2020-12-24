# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eddington_core/fit_functions/fit_functions_registry.py
# Compiled at: 2020-04-04 11:50:41
# Size of source mod 2**32: 1758 bytes
from prettytable import PrettyTable
from eddington_core.exceptions import FitFunctionLoadError

class FitFunctionsRegistry:
    _FitFunctionsRegistry__name_to_func_dict = dict()

    @classmethod
    def add(cls, func):
        cls._FitFunctionsRegistry__name_to_func_dict[func.name] = func

    @classmethod
    def remove(cls, func_name):
        del cls._FitFunctionsRegistry__name_to_func_dict[func_name]

    @classmethod
    def clear(cls):
        cls._FitFunctionsRegistry__name_to_func_dict.clear()

    @classmethod
    def all(cls):
        return cls._FitFunctionsRegistry__name_to_func_dict.values()

    @classmethod
    def names(cls):
        return cls._FitFunctionsRegistry__name_to_func_dict.keys()

    @classmethod
    def get(cls, name):
        if not cls.exists(name):
            raise FitFunctionLoadError(f"No fit function or generator named {name}")
        return cls._FitFunctionsRegistry__name_to_func_dict[name]

    @classmethod
    def load(cls, name, *args):
        func = cls.get(name)
        if func.is_generator():
            return func(*args)
        if len(args) != 0:
            raise FitFunctionLoadError(f"{name} is not a generator and should not get parameters")
        return func

    @classmethod
    def exists(cls, func_name):
        return func_name in cls._FitFunctionsRegistry__name_to_func_dict

    @classmethod
    def list(cls):
        table = PrettyTable(field_names=['Function', 'Syntax'])
        for func in FitFunctionsRegistry.all():
            table.add_row([func.signature, func.syntax])

        return table

    @classmethod
    def syntax(cls, functions):
        table = PrettyTable(field_names=['Function', 'Syntax'])
        for func_name in functions:
            if cls.exists(func_name):
                func = cls.get(func_name)
                table.add_row([func.signature, func.syntax])

        return table