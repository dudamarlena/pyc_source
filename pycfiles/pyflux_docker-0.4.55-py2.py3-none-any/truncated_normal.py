# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-n5kV9S/pyflux/pyflux/families/truncated_normal.py
# Compiled at: 2018-02-01 11:59:15
import numpy as np, scipy.stats as ss, scipy.special as sp
from .family import Family

class TruncatedNormal(Family):
    """ 
    TruncatedNormal Distribution
    ----
    This class contains methods relating to the truncated normal distribution for time series.
    """

    def __init__(self, mu=0.0, sigma=1.0, lower=None, upper=None, transform=None, **kwargs):
        """
        Parameters
        ----------
        mu : float
            Mean parameter for the Truncated Normal distribution

        sigma : float
            Standard deviation for the Truncated Normal distribution

        lower: float
            Lower truncation for the distribution

        upper: float
            Upper truncation for the distribution

        transform : str
            Whether to apply a transformation - e.g. 'exp' or 'logit'
        """
        super(TruncatedNormal, self).__init__(transform)
        self.mu0 = mu
        self.sigma0 = sigma
        self.upper = upper
        self.lower = lower
        self.covariance_prior = False

    def logpdf(self, mu):
        """
        Log PDF for Truncated Normal prior

        Parameters
        ----------
        mu : float
            Latent variable for which the prior is being formed over

        Returns
        ----------
        - log(p(mu))
        """
        if self.transform is not None:
            mu = self.transform(mu)
        if mu < self.lower and self.lower is not None:
            return -1000000.0
        else:
            if mu > self.upper and self.upper is not None:
                return -1000000.0
            else:
                return -np.log(float(self.sigma0)) - 0.5 * (mu - self.mu0) ** 2 / float(self.sigma0 ** 2)

            return

    def pdf(self, mu):
        """
        PDF for Truncated Normal prior

        Parameters
        ----------
        mu : float
            Latent variable for which the prior is being formed over

        Returns
        ----------
        - p(mu)
        """
        if self.transform is not None:
            mu = self.transform(mu)
        if mu < self.lower and self.lower is not None:
            return 0.0
        else:
            if mu > self.upper and self.upper is not None:
                return 0.0
            else:
                return 1 / float(self.sigma0) * np.exp(-(0.5 * (mu - self.mu0) ** 2) / float(self.sigma0 ** 2))

            return