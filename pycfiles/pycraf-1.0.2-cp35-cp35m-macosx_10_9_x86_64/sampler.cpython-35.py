# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/runner/runners/2.166.2/work/1/s/build/lib.macosx-10.9-x86_64-3.5/pycraf/mc/sampler.py
# Compiled at: 2020-04-16 04:29:51
# Size of source mod 2**32: 6325 bytes
import numpy as np
__all__ = [
 'HistogramSampler']

class HistogramSampler(object):
    __doc__ = '\n    Sampler to get random values obeying a discrete(!) density distribution.\n\n    With this class, one can use discrete densities (think of them as\n    binned entities, aka histograms) to get random samples that follow\n    the same (binned) distribution as the histogram. For simplicity\n    the returned values are the N-dim indices that need to be fed\n    into the histogram bin-ranges if one wants to convert them\n    to physical values (see examples, below).\n\n    Parameters\n    ----------\n    histvals : N-D `~numpy.ndarray`\n        Discrete density distribution. (This is the histogram array, which\n        one would get out of `~numpy.histogram` functions.)\n\n    Returns\n    -------\n    hist_sampler : `~pycraf.mc.HistogramSampler`\n        A `~pycraf.mc.HistogramSampler` instance.\n\n    Examples\n    --------\n\n    A trivial one-dimensional use case::\n\n        >>> import numpy as np\n        >>> from astropy.utils.misc import NumpyRNGContext\n        >>> from pycraf import mc\n\n        >>> with NumpyRNGContext(1):\n        ...     x = np.random.normal(0, 1, 100)\n\n        >>> hist, bins = np.histogram(x, bins=16, range=(-4, 4))\n        >>> mid_points = (bins[1:] + bins[:-1]) / 2\n\n        >>> my_sampler = mc.HistogramSampler(hist)\n        >>> with NumpyRNGContext(1):\n        ...     indices = my_sampler.sample(10)\n        ...     # Note that you could also do\n        ...     # indices = my_sampler(10)\n        >>> print(indices)\n        [7 9 3 7 6 5 6 7 7 8]\n\n        >>> print(mid_points[indices])  # doctest: +FLOAT_CMP\n        [-0.25  0.75 -2.25 -0.25 -0.75 -1.25 -0.75 -0.25 -0.25  0.25]\n\n    Works equally simple in 2D::\n\n        >>> with NumpyRNGContext(1):\n        ...     x = np.random.normal(0, 1, 1000)\n        ...     y = np.random.normal(2, 2, 1000)\n\n        >>> hist2d, xbins, ybins = np.histogram2d(\n        ...     x, y, bins=(16, 16), range=((-4, 4), (-6, 10))\n        ...     )\n        >>> xmids = (xbins[1:] + xbins[:-1]) / 2\n        >>> ymids = (ybins[1:] + ybins[:-1]) / 2\n\n        >>> my_sampler = mc.HistogramSampler(hist2d)\n        >>> with NumpyRNGContext(1):\n        ...     indices = my_sampler.sample(10)\n        >>> print(list(zip(*indices)))\n        [(7, 8), (9, 6), (1, 7), (7, 5), (6, 4),\n         (5, 7), (6, 7), (7, 6), (7, 8), (8, 6)]\n\n        >>> print(list(zip(xmids[indices[0]], ymids[indices[1]])))  # doctest: +FLOAT_CMP\n        [(-0.25, 2.5), (0.75, 0.5), (-3.25, 1.5), (-0.25, -0.5),\n         (-0.75, -1.5), (-1.25, 1.5), (-0.75, 1.5), (-0.25, 0.5),\n         (-0.25, 2.5), (0.25, 0.5)]\n\n    It is also easily possible to apply weights. Just assume\n    that one bin was observed exceptionally frequent::\n\n        >>> weights = np.ones_like(x)\n        >>> weights[500] = 1000\n\n        >>> hist2d, xbins, ybins = np.histogram2d(\n        ...     x, y, bins=(16, 16), range=((-4, 4), (-6, 10)),\n        ...     weights=weights\n        ...     )\n\n        >>> my_sampler = mc.HistogramSampler(hist2d)\n        >>> with NumpyRNGContext(1):\n        ...     indices = my_sampler.sample(10)\n        >>> print(list(zip(xmids[indices[0]], ymids[indices[1]])))  # doctest: +FLOAT_CMP\n        [(-1.75, 4.5), (-0.25, 3.5), (-3.25, 1.5), (-1.75, 4.5),\n         (-1.75, 4.5), (-1.75, 4.5), (-1.75, 4.5), (-1.75, 4.5),\n         (-1.75, 4.5), (-1.25, 0.5)]\n\n    As can be seen, the value `((1.25, -1.5))` is now exceptionally\n    often sampled from the distribution.\n\n    As discussed in the notes, for some use-cases a KDE might\n    be the better tool::\n\n        >>> from scipy.stats import gaussian_kde  # doctest: +SKIP\n\n        >>> kernel = gaussian_kde((x, y))  # doctest: +SKIP\n        >>> with NumpyRNGContext(1):  # doctest: +SKIP\n        ...     values = kernel.resample(10)\n\n        >>> print(*zip(values[0], values[1]))  # doctest: +SKIP +FLOAT_CMP\n        [(-1.4708084392424643, 0.73081055816321849),\n         (0.088396607804818894, 3.4075844477993105),\n        ...\n         (-2.0977896525658681, -0.2514770710536518),\n         (0.26194085609813555, -0.93622928331194344)]\n\n    Notes\n    -----\n    Even if you have continuous data to start with, using the histogram\n    approach obviously works, as well (as is demonstrated in the examples).\n    However, one looses the "continuous" property in the process.\n    The resulting samples will always be just be able to work\n    out the bin, but no continuous quantity can be reconstructed.\n    For many use cases this is probably fine, but in others one\n    might be better of by using Kernel Density Estimation.\n    There is a function for this in `~scipy.stats`\n    (`~scipy.stats.gaussian_kde`), which even allows works with\n    multi-variate data and allows one to sample from the KDE PDF\n    (see also the examples). Unfortunately, one cannot work with\n    weighted data.\n    '

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