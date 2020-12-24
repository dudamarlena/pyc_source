# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/apogee/factors/discrete/estimator.py
# Compiled at: 2019-06-15 16:42:10
# Size of source mod 2**32: 594 bytes
import numpy as np
from .factor import DiscreteFactor

class ClassifierFactor(DiscreteFactor):

    def __init__(self, scope, cards, estimator, **kwargs):
        self.estimator = estimator(**kwargs)
        super().__init__(scope, cards)

    def fit(self, x, y=None):
        self.estimator.fit(x, y)
        return self

    def predict(self, x):
        return self.estimator.predict(x)

    def reduce(self, *evidence):
        self._parameters = self.estimator.predict_proba(evidence[0].reshape(1, -1))[0]

    def refresh(self):
        self._parameters = np.ones_like(self.parameters)