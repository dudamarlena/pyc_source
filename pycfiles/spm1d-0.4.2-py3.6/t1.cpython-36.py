# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/spm1d/data/uv1d/t1.py
# Compiled at: 2019-08-22 04:37:03
# Size of source mod 2**32: 1894 bytes
import os, numpy as np
from .. import _base

class Random(_base.DatasetT1, _base.Dataset1D):

    def _set_values(self):
        self.datafile = os.path.join(_base.get_datafilepath(), 'random.npy')
        self.Y = np.load(self.datafile)
        self.mu = 0
        self.z = None
        self.df = None
        self.p = None


class RandomRough(_base.DatasetT1, _base.Dataset1D):

    def _set_values(self):
        self.datafile = os.path.join(_base.get_datafilepath(), 'random_rough.npy')
        self.Y = np.load(self.datafile)
        self.mu = 0
        self.z = None
        self.df = None
        self.p = None


class SimulatedPataky2015a(_base.DatasetT1, _base.Dataset1D):

    def _set_values(self):
        self.cite = 'Pataky, T. C., Vanrenterghem, J., & Robinson, M. A. (2015). Zero- vs. one-dimensional, parametric vs. non-parametric, and confidence interval vs. hypothesis testing procedures in one-dimensional biomechanical trajectory analysis. Journal of Biomechanics, 1–9. http://doi.org/10.1016/j.jbiomech.2015.02.051'
        self.datafile = os.path.join(_base.get_datafilepath(), 'simscalar_datasetA.npy')
        self.Y = np.load(self.datafile)
        self.mu = 0
        self.z = None
        self.df = None
        self.p = None


class SimulatedPataky2015b(_base.DatasetT1, _base.Dataset1D):

    def _set_values(self):
        self.cite = 'Pataky, T. C., Vanrenterghem, J., & Robinson, M. A. (2015). Zero- vs. one-dimensional, parametric vs. non-parametric, and confidence interval vs. hypothesis testing procedures in one-dimensional biomechanical trajectory analysis. Journal of Biomechanics, 1–9. http://doi.org/10.1016/j.jbiomech.2015.02.051'
        self.datafile = os.path.join(_base.get_datafilepath(), 'simscalar_datasetB.npy')
        self.Y = np.load(self.datafile)
        self.mu = 0
        self.z = None
        self.df = None
        self.p = None