# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/quantecon/lae.py
# Compiled at: 2018-05-14 00:27:06
# Size of source mod 2**32: 2066 bytes
r"""
Computes a sequence of marginal densities for a continuous state space
Markov chain :math:`X_t` where the transition probabilities can be represented
as densities. The estimate of the marginal density of :math:`X_t` is

.. math::

    \frac{1}{n} \sum_{i=0}^n p(X_{t-1}^i, y)

This is a density in :math:`y`.

References
----------

https://lectures.quantecon.org/py/stationary_densities.html

"""
from textwrap import dedent
import numpy as np

class LAE:
    __doc__ = '\n    An instance is a representation of a look ahead estimator associated\n    with a given stochastic kernel p and a vector of observations X.\n\n    Parameters\n    ----------\n    p : function\n        The stochastic kernel.  A function p(x, y) that is vectorized in\n        both x and y\n    X : array_like(float)\n        A vector containing observations\n\n    Attributes\n    ----------\n    p, X : see Parameters\n\n    Examples\n    --------\n    >>> psi = LAE(p, X)\n    >>> y = np.linspace(0, 1, 100)\n    >>> psi(y)  # Evaluate look ahead estimate at grid of points y\n\n    '

    def __init__(self, p, X):
        X = X.flatten()
        n = len(X)
        self.p, self.X = p, X.reshape((n, 1))

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        m = '        Look ahead estimator\n          - number of observations : {n}\n        '
        return dedent(m.format(n=(self.X.size)))

    def __call__(self, y):
        """
        A vectorized function that returns the value of the look ahead
        estimate at the values in the array y.

        Parameters
        ----------
        y : array_like(float)
            A vector of points at which we wish to evaluate the look-
            ahead estimator

        Returns
        -------
        psi_vals : array_like(float)
            The values of the density estimate at the points in y

        """
        k = len(y)
        v = self.p(self.X, y.reshape((1, k)))
        psi_vals = np.mean(v, axis=0)
        return psi_vals.flatten()