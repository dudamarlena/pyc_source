# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jess/.local/conda/lib/python3.6/site-packages/earthchem/transform/centered.py
# Compiled at: 2018-06-24 21:43:54
# Size of source mod 2**32: 1895 bytes
""" file:   centered.py
    author: Jess Robertson
            CSIRO Mineral Resources
    date:   January 2017 (happy new year!)

    description: Centered log transform for pipelines
"""
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class CenteredLogTransformPandas(BaseEstimator, TransformerMixin):
    __doc__ = ' A custom sklearn transformer which implements centered-log scaling\n        for compositional data\n\n        Works with Pandas DataFrames\n    '

    def fit(self, X, y=None):
        """Fit does nothing"""
        return self

    def transform(self, X):
        pass

    def inverse_transform(self, X):
        pass


class CenteredLogTransform(BaseEstimator, TransformerMixin):
    __doc__ = ' A custom sklearn transformer which implements centered-log scaling\n        for compositional data\n    '

    def fit(self, X, y=None):
        """Fit does nothing"""
        return self

    def transform(self, X):
        """ Returns the centered log ratio of the given composition vectors X
    
            Parameters:
                X - an array of composition vectors. An (n, m) array where n 
                    is the number of samples, and m is the number of 
                    compositional species.

            Returns:
                the CLR-transformed data
        """
        X = np.asarray(X)
        geometric_mean = np.product(X, axis=1)[:, np.newaxis] ** (1.0 / float(X.shape[1]))
        return np.log(X / geometric_mean)

    def inverse_transform(self, X):
        """ Returns the inverse centered log ratio for the given CLR transformed vector
    
            Parameters:
                X - an array of CLR-transformed composition vectors. 
            
            Returns:
                the inverted data
        """
        ratio = np.exp(X)
        return ratio / ratio.sum(axis=1)[:, np.newaxis]