# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: E:\01_Work\15_PhD\11_Python_neural_mass_models\PyRates\pyrates\ir\operator.py
# Compiled at: 2020-01-06 14:08:19
# Size of source mod 2**32: 6775 bytes
__doc__ = '\n'
from collections import namedtuple as _namedtuple
from copy import deepcopy
from typing import List, Iterator
from pyrates.ir.abc import AbstractBaseIR
__author__ = 'Daniel Rose'
__status__ = 'Development'
Variable = _namedtuple('Variable', ['vtype', 'dtype', 'shape'])

class ProtectedVariableDict:
    """ProtectedVariableDict"""
    __slots__ = [
     '_hash', '_d', '_parsed']

    def __init__(self, variables: List[tuple]):
        variables = tuple(variables)
        self._hash = hash(variables)
        self._d = {vname:dict(vtype=vtype, dtype=dtype, shape=shape) for vname, vtype, dtype, shape in variables}

    def add_parsed_variable(self, key, props):
        """Add parsed representation to a variable from compilation."""
        self._parsed[key] = props

    def __iter__(self):
        return iter(self._d)

    def __len__(self):
        return len(self._d)

    def __getitem__(self, key):
        return self._d[key]

    def __hash__(self):
        return self._hash

    def items(self):
        return self._d.items()

    def keys(self):
        return self._d.keys()

    def values(self):
        return self._d.values()

    def to_dict(self):
        return deepcopy(self._d)


class OperatorIR(AbstractBaseIR):
    """OperatorIR"""
    __slots__ = [
     '_equations', '_variables', '_inputs', '_output']

    def __init__(self, equations, variables, inputs, output, template=None):
        super().__init__(template)
        self._equations = tuple(equations)
        self._variables = ProtectedVariableDict(variables)
        self._inputs = tuple(inputs)
        self._output = output
        self._h = hash((self._equations, self._variables, self._inputs, self._output))

    @property
    def variables(self):
        return self._variables

    @property
    def equations(self):
        return self._equations

    @property
    def inputs(self):
        return self._inputs

    @property
    def output(self):
        return self._output

    def getitem_from_iterator(self, key: str, key_iter: Iterator[str]):
        """
        Checks if a variable named by key exists in an equations.
        Parameters
        ----------
        key
        key_iter

        Returns
        -------
        key
        """
        for equation in self.equations:
            if key in equation:
                return key
        else:
            raise KeyError(f"Variable `{key}` not found in equations {self.equations}")

    def __str__(self):
        return f"<{self.__class__.__name__}({self.equations}), hash = {hash(self)} >"