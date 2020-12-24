# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/bdgenomics/mango/test/distribution_test.py
# Compiled at: 2019-01-29 15:49:04
# Size of source mod 2**32: 3645 bytes
from bdgenomics.mango.coverage import CoverageDistribution
from bdgenomics.mango.test import SparkTestCase
from bdgenomics.adam.adamContext import ADAMContext

class DistributionTest(SparkTestCase):

    def test_normalized_count_distribution(self):
        ac = ADAMContext(self.ss)
        testFile = self.resourceFile('small.sam')
        reads = ac.loadAlignments(testFile)
        coverage = reads.toCoverage()
        qc = CoverageDistribution(self.ss, coverage)
        _, cd = qc.plotDistributions(testMode=True, normalize=True)
        items = list(cd.popitem()[1])
        assert len(items) == 1
        assert items.pop()[1] == 1.0
        _, cd = qc.plotDistributions(testMode=True, normalize=False)
        items = list(cd.popitem()[1])
        assert len(items) == 1
        assert items.pop()[1] == 1500

    def test_cumulative_count_distribution(self):
        ac = ADAMContext(self.ss)
        testFile = self.resourceFile('small.sam')
        reads = ac.loadAlignments(testFile)
        coverage = reads.toCoverage()
        qc = CoverageDistribution(self.ss, coverage)
        _, cd = qc.plotDistributions(testMode=True, cumulative=True, normalize=False)
        items = list(cd.popitem()[1])
        assert len(items) == 1
        assert items.pop()[1] == 1500
        _, cd = qc.plotDistributions(testMode=True, cumulative=False, normalize=False)
        items = list(cd.popitem()[1])
        assert len(items) == 1
        assert items.pop()[1] == 1500

    def test_fail_on_invalid_sample(self):
        ac = ADAMContext(self.ss)
        testFile = self.resourceFile('small.sam')
        reads = ac.loadAlignments(testFile)
        coverage = reads.toCoverage()
        with self.assertRaises(Exception):
            CoverageDistribution((self.ss), coverage, sample=1.2)
            CoverageDistribution((self.ss), coverage, sample=0)

    def test_sampling(self):
        ac = ADAMContext(self.ss)
        testFile = self.resourceFile('small.sam')
        reads = ac.loadAlignments(testFile)
        coverage = reads.toCoverage()
        cd1 = CoverageDistribution((self.ss), coverage, sample=0.9)
        sum1 = sum(map(lambda x: x[1], cd1.collectedCounts.popitem()[1]))
        cd2 = CoverageDistribution((self.ss), coverage, sample=1.0)
        sum2 = sum(map(lambda x: x[1], cd2.collectedCounts.popitem()[1]))
        dev = 500
        if not (sum1 > sum2 - dev and sum1 < sum2 + dev):
            raise AssertionError