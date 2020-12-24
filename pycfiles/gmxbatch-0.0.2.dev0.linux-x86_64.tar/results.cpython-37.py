# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/miniconda3/envs/gmxbatch/lib/python3.7/site-packages/gmxbatch/simulation/results.py
# Compiled at: 2020-03-12 09:46:09
# Size of source mod 2**32: 518 bytes
from typing import Dict
from ..conffiles import Coordinates
from ..trajectory import Trajectory
from ..xvgfile import XVGFile

class Results:
    __doc__ = 'Container class for simulation results'
    conf: Coordinates
    energy: Dict[(str, XVGFile)]
    trajectory: Trajectory
    deffnm: str

    def __init__(self, deffnm: str, conf: Coordinates, energy: Dict[(str, XVGFile)], trajectory: Trajectory):
        self.conf = conf
        self.energy = energy
        self.trajectory = trajectory
        self.deffnm = deffnm