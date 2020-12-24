# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/hydro/hydro_cluster.py
# Compiled at: 2016-03-22 15:09:41
from hydro.topology_base import Topology
from hydro.exceptions import HydroException
from copy import deepcopy
__author__ = 'moshebasanchig'

class ResultSet(object):

    def __init__(self, plan, stream):
        self.stream = stream
        self.plan = plan


class HydroBase(object):
    """
    this class will be used
    """

    def __init__(self):
        self._topologies = dict()

    def return_topology_callback_if_exist(self, topology):
        if topology in self._topologies:
            return self._topologies[topology].submit
        else:
            return

    def register(self, name, obj):
        if not isinstance(obj, Topology):
            raise HydroException('Not a Topology instance')
        self._topologies[name] = obj

    def submit(self, name, params=None):
        topology = self._topologies.get(name, None)
        if not topology:
            raise HydroException("Topology doesn't exist")
        topology.query_engine.set_topology_lookup_callback(self.return_topology_callback_if_exist)
        topology.query_engine.set_topology_cache_ttl_callback(topology.topology_cache_ttl_callback)
        data = topology.submit(deepcopy(params))
        execution_plan = topology.get_execution_plan()
        return ResultSet(execution_plan, data)


class LocalHydro(HydroBase):
    """
    creating a hook for local mocking
    """
    pass