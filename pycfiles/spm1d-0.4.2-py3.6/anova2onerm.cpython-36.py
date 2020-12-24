# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/data/uv1d/anova2onerm.py
# Compiled at: 2019-08-22 04:37:03
# Size of source mod 2**32: 1484 bytes
import os, numpy as np
from .. import _base

class _SPM1D_ANOVA2ONERM_DATASET(_base.DatasetANOVA2rm, _base.Dataset1D):

    def _set_values(self):
        self._set_datafile()
        Z = np.load(self.datafile)
        self.Y, self.A, self.B, self.SUBJ = (Z['Y'], Z['A'], Z['B'], Z['SUBJ'])
        Z.close()


class SPM1D_ANOVA2ONERM_2x2(_SPM1D_ANOVA2ONERM_DATASET):

    def _set_datafile(self):
        self.datafile = os.path.join(_base.get_datafilepath(), 'spm1d_anova2onerm_2x2.npz')


class SPM1D_ANOVA2ONERM_2x3(_SPM1D_ANOVA2ONERM_DATASET):

    def _set_datafile(self):
        self.datafile = os.path.join(_base.get_datafilepath(), 'spm1d_anova2onerm_2x3.npz')


class SPM1D_ANOVA2ONERM_3x3(_SPM1D_ANOVA2ONERM_DATASET):

    def _set_datafile(self):
        self.datafile = os.path.join(_base.get_datafilepath(), 'spm1d_anova2onerm_3x3.npz')


class SPM1D_ANOVA2ONERM_3x4(_SPM1D_ANOVA2ONERM_DATASET):

    def _set_datafile(self):
        self.datafile = os.path.join(_base.get_datafilepath(), 'spm1d_anova2onerm_3x4.npz')


class SPM1D_ANOVA2ONERM_3x5(_SPM1D_ANOVA2ONERM_DATASET):

    def _set_datafile(self):
        self.datafile = os.path.join(_base.get_datafilepath(), 'spm1d_anova2onerm_3x5.npz')


class SPM1D_ANOVA2ONERM_4x4(_SPM1D_ANOVA2ONERM_DATASET):

    def _set_datafile(self):
        self.datafile = os.path.join(_base.get_datafilepath(), 'spm1d_anova2onerm_4x4.npz')


class SPM1D_ANOVA2ONERM_4x5(_SPM1D_ANOVA2ONERM_DATASET):

    def _set_datafile(self):
        self.datafile = os.path.join(_base.get_datafilepath(), 'spm1d_anova2onerm_4x5.npz')