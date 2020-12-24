# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\despres\Desktop\reaper\scripts\reapy\reapy\tools\program.py
# Compiled at: 2019-09-02 07:23:31
# Size of source mod 2**32: 5063 bytes
"""
Define base Program class.

Notes
-----
Runing ``from reapy.tools import Program`` only imports this
``Program`` class if called from inside REAPER. If not, then the
subclass ``reapy.tools.dist_program.Program``, which overrides
``Program.run``, is imported.
"""
import importlib, operator, sys, reapy
from reapy import reascript_api as RPR

class FunctionsCache(dict):
    __doc__ = 'Caching dict-like class that imports module lazily on demand\n        and stores\n    '

    def __missing__(self, module_name):
        if module_name == 'RPR':
            module = RPR
        else:
            module = importlib.import_module(module_name)
        self[module_name] = module.__dict__
        return self[module_name]


_FUNCTIONS_CACHE = FunctionsCache()

class Program:
    _func = None

    def __init__(self, code, *output):
        """
        Build program.

        Parameters
        ----------
        code : str or function object or tuple of two strings
            Code to execute. Note that if all lines except the empty first ones
            have constant indentation, this indentation is removed (allows for
            docstring code).
            Can only be a function object if wrapped with Program.run_inside
            and then called outside.
            Can only be a tuple of strings if received from external code.
        output : iterable (contains strings or single None)
            Variable names for which values at the end of the program are
            returned after execution.
            If output contains single value which is None it means external code
                wants to create Program instance with link to reapy function
        """
        if output and output[(-1)] is None:
            self._code = self.parse_func(code)
        else:
            self._code = self.parse_code(code)
        self._output = tuple(output)

    def to_dict(self):
        """
        Return dict representation of program.

        Returns
        -------
        rep : dict
            dict representation of program. A new program with same state can
            be created from `rep` with `Program(**rep)`.
        """
        return (
         self._code,) + self._output

    def parse_func(self, func_obj):
        module_name, qualname = func_obj
        if module_name == 'RPR':
            module_name = 'reapy.reascript_api'
        try:
            module = sys.modules[module_name]
        except KeyError:
            module = importlib.import_module(module_name)

        self._func = operator.attrgetter(qualname)(sys.modules[module_name])

    def parse_code(self, code):
        """
        Return code with correct indentation.

        Parameters
        ----------
        code : str
            Code to be parsed.

        Returns
        -------
        code : str
            Parsed code.
        """
        code = code.replace('\t', '    ')
        lines = code.split('\n')
        while lines[0] == '':
            lines.pop(0)

        indentation = len(lines[0]) - len(lines[0].lstrip(' '))
        lines = [line[indentation:] for line in lines]
        code = '\n'.join(lines)
        return code

    def run(self, **input):
        """
        Run program and return output.

        Parameters
        ----------
        input : dict
            Dictionary with variable names as keys variables values as values.
            Passed as input to the program when running.

            If program was created within Program.run_inside decorator
            then input is {'args': args_tuple, 'kwargs': kwargs_dict}

            If program was created within Program.property decorator then it is
            {'args': args_tuple, 'kwargs': kwargs_dict, 'property_method': str}

        Returns
        -------
        output : tuple
            Output values.
        """
        if self._func is not None:
            if 'property_method' in input:
                _func = getattr(self._func, input['property_method'])
            else:
                _func = self._func
            reapy.print(_func)
            return _func(*input['args'], **input['kwargs'])
        input.update({'RPR':RPR,  'reapy':reapy})
        exec(self._code, input)
        output = tuple((input[o] for o in self._output))
        return output

    @staticmethod
    def run_inside(func):
        return func

    @staticmethod
    def property(func):
        return __builtins__['property'](func)