# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/data/uv1d/anova3tworm.py
# Compiled at: 2019-08-22 04:37:03
# Size of source mod 2**32: 662 bytes
import os, numpy as np
from .. import _base

class _SPM1D_ANOVA3TWORM_DATASET(_base.DatasetANOVA3rm, _base.Dataset1D):

    def _set_values(self):
        self._set_datafile()
        Z = np.load(self.datafile)
        self.Y, self.A, self.B, self.C, self.SUBJ = (Z['Y'], Z['A'], Z['B'], Z['C'], Z['SUBJ'])
        Z.close()


class SPM1D_ANOVA3TWORM_2x2x2(_SPM1D_ANOVA3TWORM_DATASET):

    def _set_datafile(self):
        self.datafile = os.path.join(_base.get_datafilepath(), 'spm1d_anova3tworm_2x2x2.npz')


class SPM1D_ANOVA3TWORM_2x3x4(_SPM1D_ANOVA3TWORM_DATASET):

    def _set_datafile(self):
        self.datafile = os.path.join(_base.get_datafilepath(), 'spm1d_anova3tworm_2x3x4.npz')