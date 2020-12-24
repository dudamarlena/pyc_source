# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jess/.local/conda/lib/python3.6/site-packages/earthchem/transform/barycentric.py
# Compiled at: 2018-06-24 21:43:54
# Size of source mod 2**32: 1190 bytes
""" file:   barycentric.py
    author: Jess Robertson
            CSIRO Mineral Resources
    date:   January 2017 (happy new year!)

    description: barycentric transform for pipelines
"""
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class BarycentricTransform(BaseEstimator, TransformerMixin):
    __doc__ = ' A custom sklearn transformer which implements a barycentric \n        transformation for 3D compositional data\n    '

    def fit(self, X, y=None):
        """
        Fit does nothing
        """
        return self

    def transform(self, X):
        """ 
        Returns the barycentric transform of the given composition vectors X

        Parameters:
            X - a Nx3 array containing the data to transform into barycentric 
                coordinates

        Returns:
            the barycentric-transformed data
        """
        X = np.asarray(X)
        if X.shape[(-1)] != 3:
            raise ValueError('X has wrong dimension for barycentric coords')
        x0, x1, x2 = X.transpose()
        denom = np.asarray((2 * (x0 + x1 + x2)), dtype=(np.float))
        return np.array([(2 * x1 + x2) / denom, np.sqrt(3) * x2 / denom]).T