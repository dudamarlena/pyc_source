# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Alister/miniconda3/envs/obsea/lib/python3.7/site-packages/obsea/station.py
# Compiled at: 2019-07-10 06:05:58
# Size of source mod 2**32: 732 bytes
"""Station module."""
from obspy.core.inventory import Inventory, Network

def select_stations(inventory, station_list):
    """
    Select station within an Inventory according to a list.

    Parameters
    ----------
    inventory : obspy.Inventory
        The inventory.
    station_list : TYPE
        The station list.

    Returns
    -------
    obspy.Inventory
        An inventory only containing stations in station_list.

    """
    if station_list is None:
        return inventory
    network, = inventory
    stations = [station for station in network if station.code in station_list]
    network = Network(code='YV', stations=stations)
    inventory = Inventory(networks=[network], source='')
    return inventory