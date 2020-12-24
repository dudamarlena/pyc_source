# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/data/uv1d/regress.py
# Compiled at: 2019-08-22 04:37:03
# Size of source mod 2**32: 1594 bytes
import os, numpy as np
from .. import _base

class SimulatedPataky2015c(_base.DatasetRegress, _base.Dataset1D):

    def _set_values(self):
        self.cite = 'Pataky, T. C., Vanrenterghem, J., & Robinson, M. A. (2015). Zero- vs. one-dimensional, parametric vs. non-parametric, and confidence interval vs. hypothesis testing procedures in one-dimensional biomechanical trajectory analysis. Journal of Biomechanics, 1–9. http://doi.org/10.1016/j.jbiomech.2015.02.051'
        self.datafile = os.path.join(_base.get_datafilepath(), 'simscalar_datasetC.npy')
        self.Y = np.load(self.datafile)
        self.x = np.arange(self.Y.shape[0])
        self.z = None
        self.r = None
        self.df = None
        self.p = None


class SpeedGRF(_base.DatasetRegress, _base.Dataset1D):

    def __init__(self, subj=0):
        self.subj = int(subj)
        super(SpeedGRF, self).__init__()

    def _set_values(self):
        self.cite = 'Pataky, T. C., Caravaggi, P., Savage, R., Parker, D., Goulermas, J., Sellers, W., & Crompton, R. (2008). New insights into the plantar pressure correlates of walking speed using pedobarographic statistical parametric mapping (pSPM). Journal of Biomechanics, 41(9), 1987–1994.'
        fnameY = os.path.join(_base.get_datafilepath(), 'ex_grf_subj%03d.npy' % self.subj)
        fnameX = os.path.join(_base.get_datafilepath(), 'ex_grf_speeds.npy')
        self.datafile = fnameY
        self.Y = np.load(fnameY)
        self.x = np.load(fnameX)[:, self.subj]
        self.z = None
        self.r = None
        self.df = None
        self.p = None