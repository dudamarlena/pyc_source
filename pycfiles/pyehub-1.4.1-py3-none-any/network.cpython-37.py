# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/juancomish/miniconda3/lib/python3.7/site-packages/pyehub/data_formats/request_format/network.py
# Compiled at: 2019-07-30 13:57:16
# Size of source mod 2**32: 2046 bytes
__doc__ = '\nProvides functionality for handling a request format network_links.\n'
from typing import Union

class Network_links:
    """Network_links"""

    def __init__(self, network_links_request: dict, capacity_link: dict) -> None:
        """Create a new wrapper for a network links.

        Args:
            network_links_request: the request format network links
            capacity_link:
        """
        self._links = network_links_request
        self._capacity = capacity_link

    @property
    def link_id(self) -> int:
        """return network link id"""
        return self._links['id']

    @property
    def start_id(self) -> int:
        """return start node id"""
        return self._links['start_id']

    @property
    def end_id(self) -> int:
        """return end node id"""
        return self._links['end_id']

    @property
    def length(self) -> float:
        """return the length of the link"""
        return self._links['length']

    @property
    def total_thermal_loss(self) -> float:
        """return the thermal loss of the connection"""
        return self._links['total_thermal_loss']

    @property
    def total_pressure_loss(self) -> float:
        """return the pressure loss of the connection"""
        return self._links['total_pressure_loss']

    @property
    def link_capacity(self) -> Union[(float, str)]:
        """return the capacity of the connection"""
        return self._links['capacity']

    @property
    def link_type(self) -> str:
        """return the type of the connection"""
        return self._links['type']

    @property
    def link_reactance(self) -> float:
        """return the reactance across the connection"""
        return self._links['reactance']

    @property
    def link_cost(self) -> float:
        """return the cost of the connection"""
        return self._links['link_cost']