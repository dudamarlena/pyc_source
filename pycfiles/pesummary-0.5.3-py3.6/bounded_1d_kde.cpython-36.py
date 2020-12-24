# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pesummary/core/plots/bounded_1d_kde.py
# Compiled at: 2020-04-21 06:57:35
# Size of source mod 2**32: 2714 bytes
import numpy as np
from scipy.stats import gaussian_kde as kde

class Bounded_1d_kde(kde):
    __doc__ = 'Represents a one-dimensional Gaussian kernel density estimator\n    for a probability distribution function that exists on a bounded\n    domain\n\n    Parameters\n    ----------\n    pts: np.ndarray\n        The datapoints to estimate a bounded kde from\n    xlow: float\n        The lower bound of the distribution\n    xhigh: float\n        The upper bound of the distribution\n    '

    def __init__(self, pts, xlow=None, xhigh=None, *args, **kwargs):
        pts = np.atleast_1d(pts)
        if pts.ndim != 1:
            raise TypeError('Bounded_1d_kde can only be one-dimensional')
        (super(Bounded_1d_kde, self).__init__)(pts.T, *args, **kwargs)
        self._xlow = xlow
        self._xhigh = xhigh

    @property
    def xlow(self):
        """The lower bound of the x domain
        """
        return self._xlow

    @property
    def xhigh(self):
        """The upper bound of the x domain
        """
        return self._xhigh

    def evaluate(self, pts):
        x = pts.T
        pdf = super(Bounded_1d_kde, self).evaluate(pts.T)
        if self.xlow is not None:
            pdf += super(Bounded_1d_kde, self).evaluate(2 * self.xlow - x)
        if self.xhigh is not None:
            pdf += super(Bounded_1d_kde, self).evaluate(2 * self.xhigh - x)
        return pdf

    def __call__(self, pts):
        pts = np.atleast_1d(pts)
        out_of_bounds = np.zeros((pts.shape[0]), dtype='bool')
        if self.xlow is not None:
            out_of_bounds[pts[:, 0] < self.xlow] = True
        if self.xhigh is not None:
            out_of_bounds[pts[:, 0] > self.xhigh] = True
        results = self.evaluate(pts)
        results[out_of_bounds] = 0.0
        return results