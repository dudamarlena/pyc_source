# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/runner/runners/2.169.1/work/MetaWards/MetaWards/tests/../build/lib.macosx-10.14-x86_64-3.7/metawards/_demographic.py
# Compiled at: 2020-05-11 13:26:49
# Size of source mod 2**32: 3341 bytes
from dataclasses import dataclass as _dataclass
from ._variableset import VariableSet
from ._network import Network
__all__ = [
 'Demographic']

@_dataclass
class Demographic:
    __doc__ = 'This class represents a single demographic'
    name = None
    name: str
    work_ratio = 0.0
    work_ratio: float
    play_ratio = 0.0
    play_ratio: float
    adjustment = None
    adjustment: VariableSet

    def specialise(self, network: Network, profiler=None, nthreads: int=1):
        """Return a copy of the passed network that has been specialised
           for this demographic. The returned network will
           contain only members of this demographic, with the
           parameters of the network adjusted according to the rules
           of this demographic

           Parameters
           ----------
           network: Network
             The network to be specialised

           Returns
           -------
           network: Network
             The specialised network
        """
        import copy
        subnet = copy.copy(network)
        subnet.nodes = network.nodes.copy()
        subnet.links = network.links.copy()
        subnet.play = network.play.copy()
        subnet.scale_susceptibles(work_ratio=(self.work_ratio), play_ratio=(self.play_ratio))
        if self.adjustment is not None:
            subnet.params = network.params.set_variables(self.adjustment)
        subnet.name = self.name
        return subnet