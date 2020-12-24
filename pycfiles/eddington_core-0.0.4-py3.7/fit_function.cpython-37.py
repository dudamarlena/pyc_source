# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eddington_core/fit_functions/fit_function.py
# Compiled at: 2020-04-04 11:50:41
# Size of source mod 2**32: 2998 bytes
import re, uuid
from typing import Callable
from dataclasses import dataclass, InitVar, field
import numpy as np, scipy
from eddington_core.exceptions import FitFunctionLoadError
from eddington_core.fit_functions.fit_functions_registry import FitFunctionsRegistry

@dataclass(repr=False, unsafe_hash=True)
class FitFunction:
    fit_func: Callable
    n: int
    name: str
    syntax: str
    a_derivative = field(default=None)
    a_derivative: np.ndarray
    x_derivative = field(default=None)
    x_derivative: np.ndarray
    title_name = field(init=False)
    title_name: str
    costumed = False
    costumed: InitVar[bool]
    save = True
    save: InitVar[bool]

    def __post_init__(self, costumed, save):
        self.title_name = self._FitFunction__get_title_name(costumed=costumed)
        self._FitFunction__costumed = costumed
        if save:
            FitFunctionsRegistry.add(self)

    def __get_title_name(self, costumed):
        if costumed:
            return 'Costumed Function'
        return self.name.title().replace('_', ' ')

    @classmethod
    def from_string(cls, syntax_string, name=None, save=True):
        if name is None:
            name = f"dummy-{uuid.uuid4()}"
        n = max([int(a) for a in re.findall('a\\[(\\d+?)\\]', syntax_string)]) + 1
        locals_dict = {}
        globals_dict = cls._FitFunction__get_costumed_globals()
        try:
            exec(f"func = lambda a, x: {syntax_string}", globals_dict, locals_dict)
        except SyntaxError:
            raise FitFunctionLoadError(f'"{syntax_string}" has invalid syntax')

        func = locals_dict['func']
        return FitFunction(fit_func=func,
          n=n,
          name=name,
          syntax=syntax_string,
          save=save,
          costumed=True)

    @classmethod
    def __get_costumed_globals(cls):
        globals_dict = globals().copy()
        globals_dict['math'] = np.math
        globals_dict['np'] = np
        globals_dict['numpy'] = np
        globals_dict.update(vars(np))
        globals_dict.update(vars(scipy.special))
        return globals_dict

    def __call__(self, a, x):
        a_length = len(a)
        if a_length != self.n:
            raise ValueError(f"input length should be {self.n}, got {a_length}")
        return self.fit_func(a, x)

    def assign(self, a):
        return lambda x: self(a, x)

    @classmethod
    def is_generator(cls):
        return False

    def is_costumed(self):
        return self._FitFunction__costumed

    @property
    def signature(self):
        return self.name

    def __repr__(self):
        return f"FitFunction(name={self.name})"


def fit_function(n, name=None, syntax=None, a_derivative=None, x_derivative=None, save=True):

    def wrapper(func):
        func_name = func.__name__ if name is None else name
        return FitFunction(fit_func=func,
          n=n,
          name=func_name,
          syntax=syntax,
          a_derivative=a_derivative,
          x_derivative=x_derivative,
          save=save)

    return wrapper