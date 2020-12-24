# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-n5kV9S/pyflux/pyflux/families/inverse_wishart.py
# Compiled at: 2018-02-01 11:59:15
import numpy as np, scipy.stats as ss, scipy.special as sp
from .. import inference as ifr
from .family import Family
from scipy.stats import invwishart

class InverseWishart(Family):
    """ 
    Inverse Wishart Distribution
    ----
    This class contains methods relating to the inverse wishart distribution for time series.
    """

    def __init__(self, v, Psi, transform=None, **kwargs):
        """
        Parameters
        ----------
        v : float
            Nu parameter for the Inverse Wishart distribution

        Psi : float
            Psi parameter for the Inverse Wishart distribution

        transform : str
            Whether to apply a transformation - e.g. 'exp' or 'logit'
        """
        super(InverseWishart, self).__init__(transform)
        self.covariance_prior = True
        self.v = v
        self.Psi = Psi

    def logpdf(self, X):
        """
        Log PDF for Inverse Wishart prior

        Parameters
        ----------
        X : float
            Covariance matrix for which the prior is being formed over

        Returns
        ----------
        - log(p(X))
        """
        return invwishart.logpdf(X, df=self.v, scale=self.Psi)

    def pdf(self, X):
        """
        PDF for Inverse Wishart prior

        Parameters
        ----------
        x : float
            Covariance matrix for which the prior is being formed over

        Returns
        ----------
        - p(x)
        """
        return invwishart.pdf(X, df=self.v, scale=self.Psi)