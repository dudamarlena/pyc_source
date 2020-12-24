# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pesummary/gw/plots/bounded_2d_kde.py
# Compiled at: 2020-04-21 06:57:35
# Size of source mod 2**32: 3209 bytes
import numpy as np
from scipy.stats import gaussian_kde as kde
from pesummary.gw.plots.bounds import default_bounds

class Bounded_2d_kde(kde):
    __doc__ = 'Class to generate a two-dimensional KDE for a probability distribution\n    functon that exists on a bounded domain\n    '

    def __init__(self, pts, xlow=None, xhigh=None, ylow=None, yhigh=None, *args, **kwargs):
        pts = np.atleast_2d(pts)
        assert pts.ndim == 2, 'Bounded_kde can only be two-dimensional'
        (super(Bounded_2d_kde, self).__init__)(pts.T, *args, **kwargs)
        self._xlow = xlow
        self._xhigh = xhigh
        self._ylow = ylow
        self._yhigh = yhigh

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

    @property
    def ylow(self):
        """The lower bound of the y domain
        """
        return self._ylow

    @property
    def yhigh(self):
        """The upper bound of the y domain
        """
        return self._yhigh

    def evaluate(self, pts):
        pts = np.atleast_2d(pts)
        assert pts.ndim == 2, 'points must be two-dimensional'
        x, y = pts.T
        pdf = super(Bounded_2d_kde, self).evaluate(pts.T)
        if self.xlow is not None:
            pdf += super(Bounded_2d_kde, self).evaluate([2 * self.xlow - x, y])
        if self.xhigh is not None:
            pdf += super(Bounded_2d_kde, self).evaluate([2 * self.xhigh - x, y])
        if self.ylow is not None:
            pdf += super(Bounded_2d_kde, self).evaluate([x, 2 * self.ylow - y])
        if self.yhigh is not None:
            pdf += super(Bounded_2d_kde, self).evaluate([x, 2 * self.yhigh - y])
        if self.xlow is not None:
            if self.ylow is not None:
                pdf += super(Bounded_2d_kde, self).evaluate([
                 2 * self.xlow - x, 2 * self.ylow - y])
            if self.yhigh is not None:
                pdf += super(Bounded_2d_kde, self).evaluate([
                 2 * self.xlow - x, 2 * self.yhigh - y])
        if self.xhigh is not None:
            if self.ylow is not None:
                pdf += super(Bounded_2d_kde, self).evaluate([
                 2 * self.xhigh - x, 2 * self.ylow - y])
            if self.yhigh is not None:
                pdf += super(Bounded_2d_kde, self).evaluate([
                 2 * self.xhigh - x, 2 * self.yhigh - y])
        return pdf

    def __call__(self, pts):
        pts = np.atleast_2d(pts)
        out_of_bounds = np.zeros((pts.shape[0]), dtype='bool')
        if self.xlow is not None:
            out_of_bounds[pts[:, 0] < self.xlow] = True
        if self.xhigh is not None:
            out_of_bounds[pts[:, 0] > self.xhigh] = True
        if self.ylow is not None:
            out_of_bounds[pts[:, 1] < self.ylow] = True
        if self.yhigh is not None:
            out_of_bounds[pts[:, 1] > self.yhigh] = True
        results = self.evaluate(pts)
        results[out_of_bounds] = 0.0
        return results