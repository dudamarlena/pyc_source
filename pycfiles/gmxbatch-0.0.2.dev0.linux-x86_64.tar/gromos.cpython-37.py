# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/miniconda3/envs/gmxbatch/lib/python3.7/site-packages/gmxbatch/forcefields/gromos.py
# Compiled at: 2020-02-28 01:14:06
# Size of source mod 2**32: 1686 bytes
from typing import Union
from .forcefield import ForceField
from ..mdp import *

class GROMOS(ForceField):
    __doc__ = 'Subclass for the GROMOS force field.\n\n    MDP parameters were taken from the Umbrella Sampling tutorial by Justin A. Lemkul\n    '
    name = 'GROMOS'

    def __init__(self, itp, moltypespath):
        """Create a new force field instance

        :param itp: include topology file name (e.g. charmm36m.ff/forcefield.itp)
        :type itp: str
        :param moltypespath: molecule types lookup directories
        :type moltypespath: list of strings (or a single string)
        """
        super().__init__(itp, moltypespath)
        self.mdp = MDP(runcontrol=RunControl(dt=0.002,
          comm_mode='Linear',
          nstcomm=10),
          neighboursearch=NeighbourSearch(cutoff_scheme='Verlet',
          nstlist=5,
          ns_type='grid',
          rlist=1.4,
          pbc='xyz'),
          electrostatics=ElectroStatics(coulombtype='PME',
          pme_order=4,
          fourierspacing=0.16,
          rcoulomb=1.4),
          vanderwaals=VanderWaals(vdwtype='Cut-off',
          vdw_modifier='Potential-shift-Verlet',
          rvdw_switch=0,
          rvdw=1.4,
          DispCorr='EnerPres'),
          constraints=Constraints(constraints='all-bonds',
          constraint_algorithm='lincs',
          lincs_iter=1,
          lincs_order=4))