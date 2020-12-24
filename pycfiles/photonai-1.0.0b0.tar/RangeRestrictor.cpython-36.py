# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nwinter/PycharmProjects/photon_projects/photon_core/photonai/modelwrapper/RangeRestrictor.py
# Compiled at: 2019-09-11 10:06:06
# Size of source mod 2**32: 521 bytes
from sklearn.base import BaseEstimator, RegressorMixin
from typing import Union

class RangeRestrictor(BaseEstimator, RegressorMixin):

    def __init__(self, low: Union[(int, float)]=0, high: Union[(int, float)]=100):
        self.low = low
        self.high = high
        self.needs_y = False
        self.needs_covariates = True

    def fit(self, X, y=None, **kwargs):
        return self

    def predict(self, X, **kwargs):
        X[X > self.high] = self.high
        X[X < self.low] = self.low
        return X