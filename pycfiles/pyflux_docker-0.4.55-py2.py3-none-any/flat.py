# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-n5kV9S/pyflux/pyflux/families/flat.py
# Compiled at: 2018-02-01 11:59:15
import numpy as np, scipy.stats as ss, scipy.special as sp
from .family import Family

class Flat(Family):
    """ 
    Flat Distribution
    ----
    This class contains methods relating to the flat prior distribution for time series.
    """

    def __init__(self, transform=None, **kwargs):
        """
        Parameters
        ----------
        transform : str
            Whether to apply a transformation - e.g. 'exp' or 'logit'
        """
        super(Flat, self).__init__(transform)
        self.covariance_prior = False

    def logpdf(self, mu):
        """
        Log PDF for Flat prior

        Parameters
        ----------
        mu : float
            Latent variable for which the prior is being formed over

        Returns
        ----------
        - log(p(mu))
        """
        return 0.0