# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/runner/runners/2.169.1/work/MetaWards/MetaWards/tests/../build/lib.macosx-10.14-x86_64-3.7/metawards/_infections.py
# Compiled at: 2020-05-11 13:26:49
# Size of source mod 2**32: 5017 bytes
from dataclasses import dataclass as _dataclass
from typing import Union as _Union
from ._network import Network
from ._networks import Networks
__all__ = [
 'Infections']

@_dataclass
class Infections:
    __doc__ = 'This class holds the arrays that record the infections as they\n       are occuring during the outbreak\n    '
    work = None
    play = None
    subinfs = None
    _work_index = None

    @property
    def N_INF_CLASSES(self) -> int:
        """The total number of stages in the disease"""
        if self.work is not None:
            return len(self.work)
        return 0

    @property
    def nnodes(self) -> int:
        """The total number of nodes (wards)"""
        if self.play is not None:
            if len(self.play) > 0:
                return len(self.play[0]) - 1
        return 0

    @property
    def nlinks(self) -> int:
        """Return the number of work links"""
        if self.work is not None:
            if len(self.work) > 0:
                return len(self.work[0]) - 1
        return 0

    @property
    def nsubnets(self) -> int:
        """Return the number of demographic subnetworks"""
        if self.subinfs is not None:
            return len(self.subinfs)
        return 0

    @staticmethod
    def build(network: _Union[(Network, Networks)]=None):
        """Construct and return the Infections object that will track
           infections during a model run on the passed Network (or Networks)

           Parameters
           ----------
           network: Network or Networks
             The network or networks that will be run

           Returns
           -------
           infections: Infections
             The space for the work and play infections for the network
             (including space for all of the demographics)
        """
        from .utils import initialise_infections, initialise_play_infections
        if isinstance(network, Network):
            inf = Infections()
            inf.work = initialise_infections(network=network)
            inf.play = initialise_play_infections(network=network)
            inf._ifrom = network.links.ifrom
            inf._ito = network.links.ito
            return inf
        if isinstance(network, Networks):
            inf = Infections.build(network.overall)
            subinfs = []
            for subnet in network.subnets:
                subinfs.append(Infections.build(subnet))

            inf.subinfs = subinfs
            return inf

    def has_different_work_matrix(self):
        """Return whether or not the sub-network work matrix
           is different to that of the overall network
        """
        return self._work_index is not None

    def get_work_index(self):
        """Return the mapping from the index in this sub-networks work
           matrix to the mapping in the overall network's work matrix
        """
        if self.has_different_work_matrix():
            return self._work_index
        return range(1, self.nlinks + 1)

    def aggregate(self, profiler=None, nthreads: int=1) -> None:
        """Aggregate all of the infection data from the demographic
           sub-networks

           Parameters
           ----------
           network: Network
               Network that was used to initialise these infections
           profiler : Profiler, optional
               Profiler used to profile the calculation, by default None
           nthreads : int, optional
               Number of threads to use, by default 1
        """
        from utils._aggregate import aggregate_infections
        aggregate_infections(infections=self, profiler=profiler, nthreads=nthreads)

    def clear(self, nthreads: int=1):
        """Clear all of the infections (resets all to zero)

           Parameters
           ----------
           nthreads: int
             Optionally parallelise this reset by specifying the number
             of threads to use
        """
        from .utils import clear_all_infections
        clear_all_infections(infections=(self.work), play_infections=(self.play),
          nthreads=nthreads)
        if self.subinfs is not None:
            for subinf in self.subinfs:
                subinf.clear(nthreads=nthreads)