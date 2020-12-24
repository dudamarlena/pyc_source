# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/juancomish/miniconda3/lib/python3.7/site-packages/pyehub/energy_hub/param_var.py
# Compiled at: 2019-07-03 19:21:52
# Size of source mod 2**32: 1631 bytes
"""
Provides a class that can either be a reference to a value or to a variable.
"""
from typing import List, Dict

class ConstantOrVar:
    __doc__ = '\n    Provides access to data that can either be a constant or a variable.\n\n    The values can either be a constant (like a float) or can be a str, which\n    is a reference to a variable in the model.\n    '

    def __init__(self, *indices: List, model=None, values: Dict=None) -> None:
        """
        Create a new class.

        Args:
            *indices: The indices of which to index by
            model: The model that holds the variables
            values: The dictionary to initialize the object. The keys are
                indexed by *indices and their values are either constants or
                strings that reference a variable.
        """
        if model is None or values is None:
            raise ValueError
        self._model = model
        self._indices = indices
        self._values = values

    def __getitem__(self, item):
        value = self._values[item]
        if isinstance(value, str):
            return getattr(self._model, value)
        return value

    def _get_values(self, matrix: Dict) -> Dict:
        for key, value in matrix.items():
            if isinstance(value, dict):
                value = self._get_values(value)
            else:
                if hasattr(value, 'value'):
                    value = value.name
            matrix[key] = value

        return matrix

    @property
    def values(self):
        """Return the values."""
        return self._get_values(self._values)