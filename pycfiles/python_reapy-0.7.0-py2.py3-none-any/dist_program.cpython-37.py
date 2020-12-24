# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\despres\Desktop\reaper\scripts\reapy\reapy\tools\dist_program.py
# Compiled at: 2019-09-02 07:25:44
# Size of source mod 2**32: 3233 bytes
"""Define distant Program class."""
import functools, reapy
from . import program

class Property(property):
    __doc__ = 'Custom property class which executes property methods inside Reaper.\n    '

    def __init__(self, func, *args, **kwargs):
        (super().__init__)(self._wrapper(func, 'fget'), *args, **kwargs)

    def getter(self, func):
        super().__init__(self._wrapper(func, 'fget'))
        return self

    def setter(self, func):
        super().__init__(self.fget, self._wrapper(func, 'fset'))
        return self

    def deleter(self, func):
        super().__init__(self.fget, self.fset, self._wrapper(func, 'fdel'))
        return self

    @staticmethod
    def _wrapper(func, method_name):

        @functools.wraps(func)
        def _wrap(*args, **kwargs):
            program = Program(func, None)
            return program.run(args=args,
              kwargs=kwargs,
              property_method=method_name)

        return _wrap


class Program(program.Program):

    @staticmethod
    def from_function(function_name):
        program = RPRProgram((None, function_name), None)

        def g(*args, **kwargs):
            return program.run(args=args, kwargs=kwargs)

        return g

    def parse_func(self, func_obj):
        res = (
         func_obj.__module__, func_obj.__qualname__)
        print(res)
        return res

    def run(self, **input):
        return CLIENT.run_program(self, input)

    @staticmethod
    def run_inside(func):
        """Decorator to make a function/method executable inside Reaper
            when called from an external app.

            Should only be able to be called from outside Reaper.
            Parent class' method does not actually decorate `func`.

            NOTE: to optimize a property use @Program.property instead.
        """
        func_module = func.__module__
        if func_module != 'reapy':
            if not func_module.startswith('reapy.'):
                raise RuntimeError('Cannot decorate non-reapy function/method!')

        @functools.wraps(func)
        def _wrap(*args, **kwargs):
            program = Program(func, None)
            return program.run(args=args, kwargs=kwargs)

        return _wrap

    @staticmethod
    def property(func):
        """Decorator to make property getter/setter/deleter executable
            inside Reaper when called from an external app.

            Should only be able to be called from outside Reaper.
            Parent class' method does not actually decorate `func`.
        """
        func_module = func.__module__
        if func_module != 'reapy':
            if not func_module.startswith('reapy.'):
                raise RuntimeError('Cannot decorate non-reapy class property!')
        return Property(func)


class RPRProgram(Program):

    def parse_func(self, func_obj):
        return func_obj[1].rsplit('.', 1)