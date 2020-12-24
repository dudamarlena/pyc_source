# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/bdgenomics/mango/coverage.py
# Compiled at: 2019-03-18 18:04:57
# Size of source mod 2**32: 1978 bytes
"""
========
Coverage
========
.. currentmodule:: bdgenomics.mango.coverage
.. autosummary::
   :toctree: _generate/

   CoverageDistribution
"""
import collections
import matplotlib.pyplot as plt
from .distribution import CountDistribution
plt.rcdefaults()

class CoverageDistribution(CountDistribution):
    __doc__ = ' CoverageDistribution class.\n    Plotting functionality for visualizing coverage distributions of multi-sample cohorts.\n    '

    def __init__(self, ss, coverageDataset, sample=1.0, bin_size=10, pre_sampled=False):
        """
        Initializes a CoverageDistribution class.
        Computes the coverage distribution of a CoverageRDD. This RDD can have data for multiple samples.

        Args:
            :param ss: global SparkSession.
            :param coverageRDD: bdgenomics.adam.rdd.CoverageDataset
            :param sample: Fraction to sample CoverageRDD. Should be between 0 and 1

        """
        self.sc = ss.sparkContext
        self.sample = sample
        self.rdd = coverageDataset.toDF().rdd.map(lambda r: (
         (
          r['optSampleId'], r['count'] - r['count'] % bin_size), int(r['end']) - int(r['start'])))
        CountDistribution.__init__(self)