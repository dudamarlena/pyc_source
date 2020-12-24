# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/bdgenomics/mango/distribution.py
# Compiled at: 2019-10-04 17:08:04
# Size of source mod 2**32: 7641 bytes
"""
=================
CountDistribution
=================
.. currentmodule:: bdgenomics.mango.distribution
.. autosummary::
   :toctree: _generate/

   CountDistribution
   HistogramDistribution
"""
import collections
import matplotlib.pyplot as plt
import numpy as np
plt.rcdefaults()

class CountDistribution:
    __doc__ = ' Abstract CountDistribution class.\n    Plotting functionality for visualizing count distributions of multi-sample cohorts.\n    '
    ss = None
    rdd = None
    sample = 1.0
    pre_sampled = False
    seed = 0

    def __init__(self):
        """
        Initializes a Distribution class.
        Computes the distribution of an rdd with records of the form (key: (sample ID, count), value: numObservations).
        Length is usually just a 1, and is used for reduceByKey().
        """
        if self.sample <= 0 or self.sample > 1:
            raise Exception('sample {} should be > 0 and <= 1'.format(self.sample))
        if self.sample < 1:
            if not self.pre_sampled:
                self.rdd = self.rdd.sample(False, self.sample, self.seed)
        collectedCounts = self.rdd.reduceByKey(lambda x, y: x + y).collect()
        approximateCounts = lambda counts, sample: int(counts * 1.0 / sample)
        x = list(map(lambda x: (x[0][0], (x[0][1], approximateCounts(x[1], self.sample))), collectedCounts))
        self.collectedCounts = collections.defaultdict(set)
        for k, v in x:
            self.collectedCounts[k].add(v)

    def plotDistributions(self, normalize=True, cumulative=False, testMode=False, **kwargs):
        """
        Plots final distribution values and returns the plotted distribution as a Counter object.
        Args:
            :param normalize: normalizes readcounts to sum to 1
            :param cumulative: plots CDF of reads
            :param testMode: if true, does not generate plot. Used for testing.
            :param **kwargs: can hold figsize
        Returns:
            matplotlib axis to plot and computed data
        """
        countDistributions = {}
        if not testMode:
            figsize = kwargs.get('figsize', (10, 5))
            bar_plt = kwargs.get('bar', False)
            f, ax = plt.subplots(figsize=figsize)
        for label, data in self.collectedCounts.items():
            if data == set():
                continue
            sData = sorted(data)
            values = list(map(lambda p: p[0], sData))
            counts = list(map(lambda p: p[1], sData))
            if normalize:
                sumCounts = float(sum(counts))
                counts = [i / sumCounts for i in counts]
            if cumulative:
                counts = np.cumsum(counts)
            countDistributions[label] = list(zip(values, counts))
            if not testMode:
                if bar_plt:
                    ax.bar(values, counts, 1, label=label)
                else:
                    ax.plot(values, counts, label=label)

        if not testMode:
            ax.legend(loc=2, shadow=True, bbox_to_anchor=(1.05, 1))
            return (ax, countDistributions)
        return (None, countDistributions)


class HistogramDistribution:
    __doc__ = ' Abstract HistogramDistribution class.\n    Plotting functionality for visualizing count distributions of multi-sample cohorts.\n    HistogramDistribution is based off of distributions with a single key.\n    '
    ss = None
    rdd = None
    sample = 1.0
    pre_sampled = False
    seed = 0

    def __init__(self):
        """
        Initializes a Distribution class.
        Computes the distribution of an rdd with records of the form (key: (sample ID, count), value: numObservations).
        Length is usually just a 1, and is used for reduceByKey().
        """
        if self.sample <= 0 or self.sample > 1:
            raise Exception('sample {} should be > 0 and <= 1'.format(self.sample))
        if self.sample < 1:
            if not self.pre_sampled:
                self.rdd = self.rdd.sample(False, self.sample, self.seed)
        collectedCounts = self.rdd.reduceByKey(lambda x, y: x + y).collect()
        approximateCounts = lambda counts, sample: int(counts * 1.0 / sample)
        self.collectedCounts = map(lambda x: approximateCounts(x[1], self.sample), collectedCounts)

    def plotDistributions(self, normalize=True, cumulative=False, testMode=False, **kwargs):
        """
        Plots final distribution values and returns the plotted distribution as a Counter object.

        Args:
            :param normalize: normalizes readcounts to sum to 1
            :param cumulative: plots CDF of reads
            :param testMode: if true, does not generate plot. Used for testing.
            :param **kwargs: can hold figsize

        Returns:
            matplotlib axis to plot and computed data
        """
        if not testMode:
            figsize = kwargs.get('figsize', (10, 5))
            bins = kwargs.get('bins', 100)
            f, ax = plt.subplots(figsize=figsize)
            ax.hist(list(self.collectedCounts), bins)
            return (ax, list(self.collectedCounts))
        return (None, list(self.collectedCounts))