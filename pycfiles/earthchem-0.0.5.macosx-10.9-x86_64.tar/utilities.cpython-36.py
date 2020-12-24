# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jess/.local/conda/lib/python3.6/site-packages/earthchem/transform/utilities.py
# Compiled at: 2018-06-24 21:43:54
# Size of source mod 2**32: 1496 bytes
""" file:   utilities.py
    author: Jess Robertson
            CSIRO Mineral Resources
    date:   January 2017 (happy new year!)

    description: Utilities for transforms
"""
import numpy as np

def closure(X, total=1):
    """ 
    The closure operator: scale X so that everything sums to unity.
    
    Parameters:
        X - a (n_points, n_dim) array of compositional values
        total - the total that things should sum to. Optional, defaults
            to unity
    
    Returns:
        an (n_points, n_dim) array where each row sums to unity
    """
    X = np.asarray(X)
    return (total * X.T / X.sum(axis=1)).T


def pd_closure(df, constant=1):
    """
    Push dataframe through closure operation
    
    Parameters:
        df - the data to close over
    
    Returns:
        a dataframe with closed data (all features sum to a constant)
    """
    return df.apply(lambda x: constant * x / df.sum(axis=1))


def basis_matrix(n_dimensions):
    """
    Return the ILR basis matrix for the given number of dimensions

    Parameters:
        n_dimensions - the number of dimensions

    Returns:
        the basis matrix V for the ILR
    """
    D = n_dimensions
    Psi = np.zeros((D - 1, D))
    for i in range(1, D):
        for j in range(1, D + 1):
            if j <= D - i:
                Psi[(i - 1, j - 1)] = np.sqrt(1 / ((D - i) * (D - i + 1)))
            else:
                if j == D - i + 1:
                    Psi[(i - 1, j - 1)] = -np.sqrt((D - i) / (D - i + 1))

    return Psi