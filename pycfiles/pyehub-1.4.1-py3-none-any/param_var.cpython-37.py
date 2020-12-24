# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/juancomish/miniconda3/lib/python3.7/site-packages/pyehub/energy_hub/param_var.py
# Compiled at: 2019-07-03 19:21:52
# Size of source mod 2**32: 1631 bytes
__doc__ = '\nProvides a class that can either be a reference to a value or to a variable.\n'
from typing import List, Dict

class ConstantOrVar:
    """ConstantOrVar"""

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
            elif hasattr(value, 'value'):
                value = value.name
            matrix[key] = value

        return matrix

    @property
    def values(self):
        """Return the values."""
        return self._get_values(self._values)