# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/app/gsitk/preprocess/__init__.py
# Compiled at: 2018-06-29 11:11:43
# Size of source mod 2**32: 423 bytes
from sklearn.base import TransformerMixin
import numpy as np

class Preprocesser(TransformerMixin):

    def __init__(self, preprocessor):
        self.preprocessor = preprocessor

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X_trans = []
        for i, x_i in enumerate(X):
            X_trans.append(self.preprocessor.preprocess(x_i))

        return np.array(X_trans)