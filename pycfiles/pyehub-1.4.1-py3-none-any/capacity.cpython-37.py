# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/juancomish/miniconda3/lib/python3.7/site-packages/pyehub/data_formats/request_format/capacity.py
# Compiled at: 2019-07-03 19:21:52
# Size of source mod 2**32: 1260 bytes
__doc__ = '\nProvides functionality for handling a request format capacity.\n'
from typing import Optional

class Capacity:
    """Capacity"""

    def __init__(self, capacity_request: dict) -> None:
        """
        Create a new wrapper.

        Args:
            capacity_request: The capacity in the capacities section of the
                request format
        """
        self._capacity = capacity_request

    @property
    def name(self) -> str:
        """The name of the capacity."""
        return self._capacity['name']

    @property
    def domain(self):
        """The domain of the capacity."""
        return self._capacity['type']

    @property
    def lower_bound(self) -> Optional[float]:
        """The lower bound of the capacity as a float."""
        if 'bounds' in self._capacity:
            if 'lower' in self._capacity['bounds']:
                return self._capacity['bounds']['lower']

    @property
    def upper_bound(self) -> Optional[float]:
        """The lower bound of the capacity as a float."""
        if 'bounds' in self._capacity:
            if 'upper' in self._capacity['bounds']:
                return self._capacity['bounds']['upper']