# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eddington_core/fit_functions/fit_function_generator.py
# Compiled at: 2020-04-04 11:50:41
# Size of source mod 2**32: 1427 bytes
from eddington_core.fit_functions.fit_functions_registry import FitFunctionsRegistry

class FitFunctionGenerator:

    def __init__(self, generator_func, name, syntax=None, parameters=None):
        self._FitFunctionGenerator__generator_func = generator_func
        self._FitFunctionGenerator__name = name
        self._FitFunctionGenerator__syntax = syntax
        self._FitFunctionGenerator__parameters = parameters
        self._FitFunctionGenerator__signature = f"{name}({FitFunctionGenerator._FitFunctionGenerator__param_string(parameters)})"
        FitFunctionsRegistry.add(self)

    def __call__(self, *args, **kwargs):
        return (self._FitFunctionGenerator__generator_func)(*args, **kwargs)

    @property
    def name(self):
        return self._FitFunctionGenerator__name

    @property
    def syntax(self):
        return self._FitFunctionGenerator__syntax

    @property
    def parameters(self):
        return self._FitFunctionGenerator__parameters

    @property
    def signature(self):
        return self._FitFunctionGenerator__signature

    @classmethod
    def is_generator(cls):
        return True

    @classmethod
    def __param_string(cls, parameters):
        if isinstance(parameters, str):
            return parameters
        return ', '.join(parameters)


def fit_function_generator(parameters, name=None, syntax=None):

    def wrapper(generator):
        generator_name = generator.__name__ if name is None else name
        return FitFunctionGenerator(generator_func=generator,
          name=generator_name,
          syntax=syntax,
          parameters=parameters)

    return wrapper