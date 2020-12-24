# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/quantecon/ecdf.py
# Compiled at: 2018-05-14 00:27:06
# Size of source mod 2**32: 1028 bytes
"""
Implements the empirical cumulative distribution function given an array
of observations.

"""
import numpy as np

class ECDF:
    __doc__ = '\n    One-dimensional empirical distribution function given a vector of\n    observations.\n\n    Parameters\n    ----------\n    observations : array_like\n        An array of observations\n\n    Attributes\n    ----------\n    observations : see Parameters\n\n    '

    def __init__(self, observations):
        self.observations = np.asarray(observations)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        m = 'Empirical CDF:\n  - number of observations: {n}'
        return m.format(n=(self.observations.size))

    def __call__(self, x):
        """
        Evaluates the ecdf at x

        Parameters
        ----------
        x : scalar(float)
            The x at which the ecdf is evaluated

        Returns
        -------
        scalar(float)
            Fraction of the sample less than x

        """
        return np.mean(self.observations <= x)