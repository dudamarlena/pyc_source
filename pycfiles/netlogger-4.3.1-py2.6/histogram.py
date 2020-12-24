# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/analysis/histogram.py
# Compiled at: 2009-12-08 17:43:28
"""
Generic histogram class.
"""

class Histogram:

    def __init__(self, min_, max_, n):
        self._min, self._max, self.nbins = min_, max_, n
        self._width = float(self._max - self._min) / self.nbins
        self._n = 0
        self.counts, self.outliers = [0] * self.nbins, [0, 0]

    def getQuantile(self, q):
        """Return left edge if bin for q-th quantile of
        cumulative distribution of the counts
        No interpolation is performed.
        """
        if q < 0.0 or q > 1.0:
            raise ValueError('Quantile must be in range (0,1)')
            return self._max
        n1 = self._n + 1
        if q < 1 / n1:
            return self._min
        if q > self._n / n1:
            return self._max
        k = int(q * self._n)
        num = 0
        for (i, b) in enumerate(self.counts):
            num += b
            if num >= k:
                break

        xk = i * self._width + self._min
        return xk

    def getBreaks(self):
        """Return list of breakpoints between histogram cells.
        If there are N cells, there will be N-1 breakpoints.
        """
        breaks = [ x * self._width + self._min for x in range(1, self.nbins) ]
        return breaks

    def addLine(self, value):
        bin = self._getBin(value)
        if bin == -1:
            self.outliers[0] += 1
            return
        if bin == self.nbins:
            self.outliers[1] += 1
        else:
            self.counts[bin] += 1
        self._n += 1

    def _getBin(self, value):
        if value < self._min:
            return -1
        if value > self._max:
            return self.nbins
        bin = int((value - self._min) / self._width)
        return bin