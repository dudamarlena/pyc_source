# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/runner/runners/2.166.2/work/1/s/build/lib.macosx-10.9-x86_64-3.5/pycraf/mc/sampler.py
# Compiled at: 2020-04-16 04:29:51
# Size of source mod 2**32: 6325 bytes
import numpy as np
__all__ = [
 'HistogramSampler']

class HistogramSampler(object):
    """HistogramSampler"""

    def __init__(self, histvals):
        histvals = np.atleast_1d(histvals)
        self._hshape = histvals.shape
        self._ndim = histvals.ndim
        self._cdf = np.cumsum(histvals.flatten().astype(np.float64, copy=False))
        self._cdf /= self._cdf[(-1)]

    def sample(self, n):
        """
        Sample from the (discrete) density distribution.

        Parameters
        ----------
        n : int
            Number of samples to draw.

        Returns
        -------
        Indices : tuple of `~numpy.ndarray`
            The indices of the drawn samples with respect to the
            discrete density array (aka histogram object). See
            `~pycraf.mc.HistogramSampler` for examples of use.
        """
        rsamples = np.random.rand(n)
        rbins = np.searchsorted(self._cdf, rsamples)
        indices = np.unravel_index(rbins, self._hshape)
        if self._ndim == 1:
            return indices[0]
        else:
            return indices

    def __call__(self, n):
        """
        Convenience method to allow using an *instance* of
        `~pycraf.mc.HistogramSampler` like a function::

            my_sampler = mc.HistogramSampler(hist)
            my_sampler(10)

        Calls `~pycraf.mc.HistogramSampler.sample` internally.
        """
        return self.sample(n)