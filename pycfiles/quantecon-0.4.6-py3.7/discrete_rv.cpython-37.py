# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/quantecon/discrete_rv.py
# Compiled at: 2018-12-17 00:08:05
# Size of source mod 2**32: 1937 bytes
"""
Generates an array of draws from a discrete random variable with a
specified vector of probabilities.

"""
import numpy as np
from numpy import cumsum
from .util import check_random_state

class DiscreteRV:
    __doc__ = '\n    Generates an array of draws from a discrete random variable with\n    vector of probabilities given by q.\n\n    Parameters\n    ----------\n    q : array_like(float)\n        Nonnegative numbers that sum to 1.\n\n    Attributes\n    ----------\n    q : see Parameters.\n    Q : array_like(float)\n        The cumulative sum of q.\n\n    '

    def __init__(self, q):
        self._q = np.asarray(q)
        self.Q = cumsum(q)

    def __repr__(self):
        return 'DiscreteRV with {n} elements'.format(n=(self._q.size))

    def __str__(self):
        return self.__repr__()

    @property
    def q(self):
        """
        Getter method for q.

        """
        return self._q

    @q.setter
    def q(self, val):
        """
        Setter method for q.

        """
        self._q = np.asarray(val)
        self.Q = cumsum(val)

    def draw(self, k=1, random_state=None):
        """
        Returns k draws from q.

        For each such draw, the value i is returned with probability
        q[i].

        Parameters
        -----------
        k : scalar(int), optional
            Number of draws to be returned

        random_state : int or np.random.RandomState, optional
            Random seed (integer) or np.random.RandomState instance to set
            the initial state of the random number generator for
            reproducibility. If None, a randomly initialized RandomState is
            used.

        Returns
        -------
        array_like(int)
            An array of k independent draws from q

        """
        random_state = check_random_state(random_state)
        return self.Q.searchsorted(random_state.uniform(0, 1, size=k), side='right')