# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/runner/runners/2.169.1/work/MetaWards/MetaWards/tests/../build/lib.macosx-10.14-x86_64-3.7/metawards/_workspace.py
# Compiled at: 2020-05-11 13:26:49
# Size of source mod 2**32: 4035 bytes
from dataclasses import dataclass as _dataclass
from typing import List as _List
from typing import Union as _Union
from ._network import Network
from ._networks import Networks
__all__ = [
 'Workspace']

@_dataclass
class Workspace:
    __doc__ = 'This class provides a workspace for the running calculation.\n       This pre-allocates all of the memory into arrays, which\n       can then be used via cython memory views\n    '
    n_inf_classes = 0
    n_inf_classes: int
    nnodes = 0
    nnodes: int
    inf_tot = None
    inf_tot: _List[int]
    pinf_tot = None
    pinf_tot: _List[int]
    n_inf_wards = None
    n_inf_wards: _List[int]
    total_inf_ward = None
    total_inf_ward: _List[int]
    total_new_inf_ward = None
    total_new_inf_ward: _List[int]
    incidence = None
    incidence: _List[int]
    S_in_wards = None
    S_in_wards: _List[int]
    E_in_wards = None
    E_in_wards: _List[int]
    I_in_wards = None
    I_in_wards: _List[int]
    R_in_wards = None
    R_in_wards: _List[int]
    subspaces = None

    @staticmethod
    def build(network: _Union[(Network, Networks)]):
        """Create the workspace needed to run the model for the
           passed network
        """
        params = network.params
        workspace = Workspace()
        if isinstance(network, Network):
            n_inf_classes = params.disease_params.N_INF_CLASSES()
            workspace.n_inf_classes = params.disease_params.N_INF_CLASSES()
            workspace.nnodes = network.nnodes
            size = workspace.nnodes + 1
            from utils._array import create_int_array
            workspace.inf_tot = create_int_array(n_inf_classes, 0)
            workspace.pinf_tot = create_int_array(n_inf_classes, 0)
            workspace.n_inf_wards = create_int_array(n_inf_classes, 0)
            workspace.total_inf_ward = create_int_array(size, 0)
            workspace.total_new_inf_ward = create_int_array(size, 0)
            workspace.incidence = create_int_array(size, 0)
            workspace.S_in_wards = create_int_array(size, 0)
            workspace.E_in_wards = create_int_array(size, 0)
            workspace.I_in_wards = create_int_array(size, 0)
            workspace.R_in_wards = create_int_array(size, 0)
        else:
            if isinstance(network, Networks):
                workspace = Workspace.build(network.overall)
                subspaces = []
                for subnet in network.subnets:
                    subspaces.append(Workspace.build(subnet))

                workspace.subspaces = subspaces
            return workspace

    def zero_all(self, zero_subspaces=True):
        """Reset the values of all of the arrays to zero.
           By default we zero the subspace networks
           (change this by setting zero_subspaces to False)
        """
        for i in range(0, self.n_inf_classes):
            self.inf_tot[i] = 0
            self.pinf_tot[i] = 0
            self.n_inf_wards[i] = 0

        for i in range(0, self.nnodes + 1):
            self.total_inf_ward[i] = 0
            self.total_new_inf_ward[i] = 0
            self.incidence[i] = 0
            self.S_in_wards[i] = 0
            self.E_in_wards[i] = 0
            self.I_in_wards[i] = 0
            self.R_in_wards[i] = 0

        if zero_subspaces:
            if self.subspaces is not None:
                for subspace in self.subspaces:
                    subspace.zero_all()