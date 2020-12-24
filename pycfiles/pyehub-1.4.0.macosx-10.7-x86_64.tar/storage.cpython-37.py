# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/juancomish/miniconda3/lib/python3.7/site-packages/pyehub/data_formats/request_format/storage.py
# Compiled at: 2019-07-03 19:21:52
# Size of source mod 2**32: 2599 bytes
"""
Provides functionality for handling a request format's storage.
"""
from typing import Union

class Storage:
    __doc__ = 'A wrapper for a request format storage.'

    def __init__(self, storage_request: dict, capacity_request: dict) -> None:
        """
        Create a new wrapper.

        Args:
            storage_request: The request format storage
            capacity_request: The request format capacity corresponding to the
                storage
        """
        self._storage = storage_request
        self._capacity = capacity_request

    @property
    def name(self) -> str:
        """Return the name of the storage."""
        return self._storage['name']

    @property
    def capacity(self) -> Union[(float, str)]:
        """Return the capacity of the storage."""
        return self._storage['capacity']

    @property
    def stream(self) -> str:
        """The stream that this storage holds."""
        return self._storage['stream']

    @property
    def min_state(self) -> float:
        """The minimum state of charge of the storage."""
        return self._storage['min_state']

    @property
    def discharge_efficiency(self) -> float:
        """The discharge efficiency of the storage."""
        return self._storage['discharge_efficiency']

    @property
    def charge_efficiency(self) -> float:
        """The charge efficiency of the storage."""
        return self._storage['charge_efficiency']

    @property
    def lifetime(self) -> float:
        """The life time in years of the storage."""
        return self._storage['lifetime']

    @property
    def cost(self) -> float:
        """The cost of the storage."""
        return self._storage['cost']

    @property
    def max_charge(self) -> float:
        """The maximum charge of the storage."""
        return self._storage['max_charge']

    @property
    def max_discharge(self) -> float:
        """The maximum discharge of the storage."""
        return self._storage['max_discharge']

    @property
    def decay(self) -> float:
        """The decay of the storage."""
        return self._storage['decay']

    @property
    def annual_maintenance_cost(self) -> float:
        """The annual maintenance cost of the storage"""
        if 'annual_maintenance_cost' in self._storage:
            return self._storage['annual_maintenance_cost']
        return 0

    @property
    def fixed_capital_cost(self) -> float:
        """The fixed capital cost of the storage"""
        if 'fixed_capital_cost' in self._storage:
            return self._storage['fixed_capital_cost']
        return 0