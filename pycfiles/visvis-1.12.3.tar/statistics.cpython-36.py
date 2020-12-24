# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\dev\pylib\visvis\processing\statistics.py
# Compiled at: 2017-05-31 20:05:28
# Size of source mod 2**32: 11657 bytes
import numpy as np

def statistics(data):
    """ Get StatData object for the given data.
    """
    return StatData(data)


class StatData:
    __doc__ = " StatData(data)\n    \n    Get statistics on the given sequence of data. The data must be\n    something that is accepted by np.array(). Any nonfinite data points\n    (NaN, Inf, -Inf) are removed from the data.\n    \n    Allows easy calculation of statistics such as mean, std, median,\n    any percentile, histogram data and kde's.\n    \n    This class was initially designed for the boxplot functionality.\n    This interface was made public because it can be usefull to the\n    generic user too.\n    \n    "

    def __init__(self, data):
        if not isinstance(data, np.ndarray):
            data = np.array(data)
        self._data = np.sort(data.ravel())
        valid = np.isfinite(self._data)
        self._data = self._data[valid]
        self._mean = self._data.mean()
        self._std = self._data.std()

    def __repr__(self):
        return '<StatData object with %i elements>' % self.size

    def __str__(self):
        s = 'Summary of StatData object:\n'
        for key in ('size', 'dmin', 'dmax', 'drange', 'mean', 'std', 'Q1', 'Q2', 'Q3',
                    'IQR'):
            value = str(getattr(self, key))
            line = key.rjust(10) + ' = ' + value + '\n'
            s += line

        return s

    @property
    def size(self):
        """ Get the number of elements in the data.
        """
        return self._data.size

    @property
    def drange(self):
        """ Get the range of the data (max-min).
        """
        return float(self._data[(-1)] - self._data[0])

    @property
    def dmin(self):
        """ Get the minimum of the data.
        """
        return self._data[0]

    @property
    def dmax(self):
        """ Get the max of the data.
        """
        return self._data[(-1)]

    @property
    def mean(self):
        """ Get the mean of the data.
        """
        return self._mean

    @property
    def std(self):
        """ Get the standard deviation of the data.
        """
        return self._std

    @property
    def Q1(self):
        """ Get first quartile of the data (i.e. the 25th percentile).
        """
        return self.percentile(0.25)

    @property
    def Q2(self):
        """ Get second quartile of the data (i.e. the 50th percentile).
        This is the median.
        """
        return self.percentile(0.5)

    @property
    def median(self):
        """ Get the median. This is the same as Q2.
        """
        return self.percentile(0.5)

    @property
    def Q3(self):
        """ Get second quartile of the data (i.e. the 50th percentile).
        """
        return self.percentile(0.75)

    @property
    def IQR(self):
        """ Get the inter-quartile range; the range where 50% of the
        data is.
        """
        return self.percentile(0.75) - self.percentile(0.25)

    def percentile(self, per, interpolate=True):
        """ percentile(per, interpolate=True)
        
        Given a percentage (as a number between 0 and 1)
        return the value corresponding to that percentile.
        
        By default, the value is linearly interpolated if it does not
        fall exactly on an existing value.
        """
        data = self._data
        i = (data.size - 1) * float(per)
        if interpolate:
            ik = int(i)
            ir = i - ik
            if ik >= data.size - 1:
                return data[ik]
            else:
                return data[ik] + ir * (data[(ik + 1)] - data[ik])
        else:
            i = int(round(i))
            return data[i]

    def histogram_np(self, nbins=None, drange=None, normed=False, weights=None):
        """"  histogram_np(self, nbins=None, range=None, normed=False, weights=None)
        
        Calculate the histogram of the data.
        
        If nbins is not given, a good value is chosen using
        the Freedman-Diaconis rule.
        Returns a 2-element tuple containing the bin centers and the
        counts.
        
        See also the kde() method.
        
        Parameters
        ----------
        nbins : int or sequence of scalars, optional
            If `bins` is an int, it defines the number of equal-width bins in
            the given range. If `bins` is a sequence, it defines
            the bin edges, including the rightmost edge, allowing for non-uniform
            bin widths. If not given, the optimal number of bins is calculated
            using the Freedman-Diaconis rule.
        range : (float, float)
            The lower and upper range of the bins. If not provided, range is
            simply (a.min(), a.max()). Values outside the range are ignored.
        normed : bool
            If False, the result will contain the number of samples in each bin.
            If True, the result is the value of the probability *density*
            function at the bin, normalized such that the *integral* over the
            range is 1. Note that the sum of the histogram values will not be
            equal to 1 unless bins of unity width are chosen; it is not a
            probability *mass* function.
        weights : array_like
            An array of weights, of the same shape as `a`. Each value in `a`
            only contributes its associated weight towards the bin count
            (instead of 1). If `normed` is True, the weights are normalized,
            so that the integral of the density over the range remains 1.
        
        """
        if nbins is None:
            nbins = self.best_number_of_bins()
        values, edges = np.histogram(self._data, nbins, drange, normed, weights)
        centers = np.empty(values.size, np.float32)
        for i in range(len(values)):
            centers[i] = (edges[i] + edges[(i + 1)]) * 0.5

        return (
         centers, values)

    def histogram(self, nbins=None):
        """  histogram(self, nbins=None)
        
        Calculate the (normalized) histogram of the data.
        
        If nbins is not given, a good value is chosen using
        the Freedman-Diaconis rule.
        
        See also the histogram_np() and kde() methods.
        
        """
        if nbins is None:
            nbins = self.best_number_of_bins()
        return self._kernel_density_estimate(nbins, [1])

    def kde(self, nbins=None, kernel=None):
        """  kde(self, nbins=None)
        
        Calculate the kernel density estimation of the data.
        
        If nbins is not given, a good value is chosen using
        the Freedman-Diaconis rule. If kernel is not given,
        a Gaussian kernel is used, with a sigma depending
        on nbins.
        
        """
        best_nbins = self.best_number_of_bins()
        if nbins is None:
            nbins = 4 * best_nbins
        if kernel is None:
            kernel = float(nbins) / best_nbins
        return self._kernel_density_estimate(nbins, kernel)

    def best_number_of_bins(self, minbins=8, maxbins=256):
        """ best_number_of_bins(minbins=8, maxbins=256)
        
        Calculates the best number of bins to make a histogram
        of this data, according to Freedman-Diaconis rule.
        
        """
        data = self._data
        bin_size = 2 * self.IQR * data.size ** (-0.3333333333333333)
        nbins = self.drange / (bin_size + 0.001)
        nbins = max(minbins, min(maxbins, int(nbins)))
        return nbins

    def _kernel_density_estimate(self, n, kernel):
        """ kernel density estimate(n, kernel)
        """
        data = self._data
        dmin, dmax, drange = self.dmin, self.dmax, self.drange
        if not drange:
            eps = 0.5
            dmin, dmax, drange = dmin - eps, dmax + eps, 2 * eps
        else:
            if isinstance(kernel, float):
                sigma = kernel
                ktail = int(sigma * 3)
                kn = ktail * 2 + 1
                t = np.arange((-kn / 2.0 + 0.5), (kn / 2.0), 1.0, dtype=(np.float64))
                k = np.exp(-t ** 2 / (2 * sigma ** 2))
            else:
                k = np.array(kernel, dtype='float64').ravel()
                ktail = int(k.size / 2)
        dbin = drange / n
        nbins = n + ktail * 2
        bins = (np.arange(nbins) - ktail + 0.5) * dbin + dmin
        k /= k.sum() * data.size * dbin
        kde = np.zeros_like(bins)
        xx = (data - dmin) * (1.0 / dbin)
        xxi = xx.astype('int32')
        step = max(1, int(data.size / n))
        i0, i1, i2 = 0, 0, step
        val = xxi[i0]
        totalSplats = 0
        i2 = min(i2, xxi.size - 1)
        while i1 < i2:
            if xxi[i2] > val:
                if xxi[(i2 - 1)] == val:
                    nSplats = i2 - i0
                    kde[val:val + k.size] += k * nSplats
                    totalSplats += nSplats
                    step = max(1, nSplats)
                    i0, i1, i2 = i2, i2, i2 + step
                    val = xxi[i0]
                else:
                    step = max(1, int(0.5 * step))
                    i2 = i1 + step
            else:
                i1, i2 = i2, i2 + step
            i2 = min(i2, xxi.size - 1)

        if val >= n:
            val -= 1
        nSplats = i2 - i0 + 1
        kde[val:val + k.size] += k * nSplats
        totalSplats += nSplats
        return (
         bins, kde)