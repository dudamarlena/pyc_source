# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/data/uv1d/t2.py
# Compiled at: 2019-08-22 04:37:03
# Size of source mod 2**32: 1022 bytes
import os, numpy as np
from .. import _base

class PlantarArchAngle(_base.DatasetT2, _base.Dataset1D):

    def _set_values(self):
        self.datafile = os.path.join(_base.get_datafilepath(), 'ex_kinematics.npy')
        self.cite = 'Caravaggi, P., Pataky, T., Günther, M., Savage, R., & Crompton, R. (2010). Dynamics of longitudinal arch support in relation to walking speed: contribution of the plantar aponeurosis. Journal of Anatomy, 217(3), 254–261. http://doi.org/10.1111/j.1469-7580.2010.01261.x'
        Y = np.load(self.datafile)
        self.YA = Y[10:20]
        self.YB = Y[20:]
        self.z = None
        self.df = None
        self.p = None


class SimulatedTwoLocalMax(_base.DatasetT2, _base.Dataset1D):

    def _set_values(self):
        self.datafile = os.path.join(_base.get_datafilepath(), 'ex_sim_twolocalmax.npy')
        Y = np.load(self.datafile)
        self.YA = Y[:6]
        self.YB = Y[6:]
        self.z = None
        self.df = None
        self.p = None