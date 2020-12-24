# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/data/uv1d/anova1rm.py
# Compiled at: 2019-08-22 04:37:03
# Size of source mod 2**32: 748 bytes
import os, numpy as np
from .. import _base

class SpeedGRFcategoricalRM(_base.DatasetANOVA1rm, _base.Dataset1D):

    def _set_values(self):
        self.cite = 'Pataky, T. C., Caravaggi, P., Savage, R., Parker, D., Goulermas, J., Sellers, W., & Crompton, R. (2008). New insights into the plantar pressure correlates of walking speed using pedobarographic statistical parametric mapping (pSPM). Journal of Biomechanics, 41(9), 1987–1994.'
        self.datafile = os.path.join(_base.get_datafilepath(), 'ex_grf_means.npz')
        Z = np.load(self.datafile)
        self.Y = Z['Y']
        self.A = Z['SPEED']
        self.SUBJ = Z['SUBJ']
        Z.close()
        self.z = None
        self.df = None
        self.p = None