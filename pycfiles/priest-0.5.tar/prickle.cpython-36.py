# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/prickle/prickle.py
# Compiled at: 2018-07-18 10:59:48
# Size of source mod 2**32: 3060 bytes
import numpy as np, pandas as pd
from itertools import product
from warnings import warn
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

class Prickle(object):
    """Prickle"""

    def __init__(self, samples, zero):
        self.samples = samples
        self.zero = zero
        self.rows = range(samples.shape[0])
        self.cols = range(samples.shape[1])
        self.ij = product(self.rows, self.cols)

    def plot_dots(self, **kwds):
        """Plot dots showing zero values for all elements in `samples` that
            have `m` > 0.

        Args:
            **kwds (Keyword arguments): Passed to ax.scatter().

        Returns:
            `matplotlib.axes.Axes`
        """
        ax = plt.gca()
        dots = np.argwhere(self.samples.notnull().values)
        s = kwds.pop('s', 10)
        c = kwds.pop('c', 'black')
        (ax.scatter)(dots[:, 0], dots[:, 1], s=s, c=c, **kwds)
        return ax

    def plot_prickles(self, **kwds):
        """Plot prickles.

        Args:
            **kwds (Keyword arguments): Passed to
                `matplotlib.collections.LineCollection`.

        Returns:
            `matplotlib.axes.Axes`
        """
        segments = []
        append = segments.append
        for i, j in self.ij:
            element = self.samples.iloc[(i, j)]
            if hasattr(element, '__len__'):
                vectors = np.array(element) - self.zero.values
                x0, y0 = i, j
                for vector in vectors:
                    x1 = x0 + vector[0]
                    y1 = y0 + vector[1]
                    append([[x0, y0], [x1, y1]])

            else:
                if pd.notnull(element):
                    warn('Odd element in df at samples.loc[{}, {}] It is not null, and it could not be plotted'.format(i, j))

        ax = plt.gca()
        linewidths = kwds.pop('linewidths', 1)
        colors = kwds.pop('colors', 'black')
        lc = LineCollection(segments=segments, 
         linewidths=linewidths, colors=colors, **kwds)
        ax.add_artist(lc)
        return ax