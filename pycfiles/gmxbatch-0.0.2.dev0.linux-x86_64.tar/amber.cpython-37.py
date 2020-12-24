# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/miniconda3/envs/gmxbatch/lib/python3.7/site-packages/gmxbatch/forcefields/amber.py
# Compiled at: 2020-03-10 07:08:10
# Size of source mod 2**32: 1768 bytes
from typing import Union
from .forcefield import ForceField
from ..mdp import *

class Amber(ForceField):
    __doc__ = 'Subclass for the AMBER force field.\n\n    MDP parameters were taken from the work of Stachura, Malajczuk and Mancera\n    (DOI: 10.1007/s00894-018-3720-x)\n    http://manual.gromacs.org/documentation/2018/user-guide/force-fields.html\n    '
    name = 'Amber'

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
          nstcomm=100),
          neighboursearch=NeighbourSearch(cutoff_scheme='Verlet',
          nstlist=20,
          ns_type='grid',
          rlist=0.8,
          pbc='xyz'),
          electrostatics=ElectroStatics(coulombtype='PME',
          pme_order=4,
          fourierspacing=0.16,
          rcoulomb=0.8),
          vanderwaals=VanderWaals(vdwtype='cutoff',
          vdw_modifier='none',
          rvdw_switch=0.0,
          rvdw=0.8,
          DispCorr='no'),
          constraints=Constraints(constraints='h-bonds',
          constraint_algorithm='lincs',
          lincs_iter=1,
          lincs_order=4))