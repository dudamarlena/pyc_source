# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/bdgenomics/mango/test/coverage_test.py
# Compiled at: 2019-01-29 15:49:04
# Size of source mod 2**32: 2832 bytes
import sys
from bdgenomics.mango.coverage import *
from bdgenomics.mango.test import SparkTestCase
from collections import Counter
from bdgenomics.adam.adamContext import ADAMContext

class CoverageTest(SparkTestCase):

    def test_coverage_distribution(self):
        ac = ADAMContext(self.ss)
        testFile = self.resourceFile('small.sam')
        reads = ac.loadAlignments(testFile)
        coverage = reads.toCoverage()
        qc = CoverageDistribution((self.ss), coverage, bin_size=1)
        _, cd = qc.plotDistributions(testMode=True, normalize=False)
        assert len(cd) == 1
        items = list(cd.popitem()[1])
        assert items[0][1] == 1500

    def test_example_coverage(self):
        ac = ADAMContext(self.ss)
        testFile = self.exampleFile('chr17.7500000-7515000.sam')
        alignments = ac.loadAlignments(testFile)
        coverage = alignments.toCoverage()
        qc = CoverageDistribution((self.ss), coverage, bin_size=1)
        _, cd1 = qc.plotDistributions(testMode=True, cumulative=False, normalize=False)
        total = sum(map(lambda x: x[1], list(qc.collectedCounts.items())[0][1]))
        items = list(cd1.popitem()[1])
        x = items[0]
        assert x[0] == 1
        assert x[1] == 6
        _, cd2 = qc.plotDistributions(testMode=True, cumulative=False, normalize=True)
        items = list(cd2.popitem()[1])
        x = items[0]
        assert x[0] == 1
        assert x[1] == 6.0 / total
        _, cd3 = qc.plotDistributions(testMode=True, cumulative=True, normalize=True)
        items = list(cd3.popitem()[1])
        x = items[(-1)]
        assert x[0] == 89
        assert x[1] > 0.999