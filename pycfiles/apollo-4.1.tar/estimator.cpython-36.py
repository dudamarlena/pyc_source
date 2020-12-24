# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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