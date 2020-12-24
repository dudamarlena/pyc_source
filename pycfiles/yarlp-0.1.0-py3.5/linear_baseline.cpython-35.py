# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yarlp/model/linear_baseline.py
# Compiled at: 2018-04-01 15:02:11
# Size of source mod 2**32: 1140 bytes
import numpy as np

class LinearFeatureBaseline:
    __doc__ = '\n    Value-function baseline from rllab,\n    linear model with some polynomial features on states\n    '

    def __init__(self, reg_coeff=1e-05):
        self._coeffs = None
        self._reg_coeff = reg_coeff

    def _features(self, states):
        o = np.clip(states, -10, 10)
        n = states.shape[0]
        al = np.arange(n).reshape(-1, 1) / 100.0
        return np.concatenate([
         o, o ** 2, al, al ** 2, al ** 3, np.ones((n, 1))], axis=1)

    def fit(self, states, returns):
        featmat = self._features(states)
        reg_coeff = self._reg_coeff
        for _ in range(5):
            self._coeffs = np.linalg.lstsq(featmat.T.dot(featmat) + reg_coeff * np.identity(featmat.shape[1]), featmat.T.dot(returns), rcond=None)[0]
            if not np.any(np.isnan(self._coeffs)):
                break
            reg_coeff *= 10

    def predict(self, states):
        if self._coeffs is None:
            return np.zeros(states.shape[0])
        return self._features(states).dot(self._coeffs)