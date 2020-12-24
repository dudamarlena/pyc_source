# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/bdgenomics/mango/test/alignment_test.py
# Compiled at: 2019-01-29 15:49:04
# Size of source mod 2**32: 5880 bytes
from bdgenomics.mango.test import SparkTestCase
from bdgenomics.mango.alignments import *
from bdgenomics.adam.adamContext import ADAMContext

class AlignmentTest(SparkTestCase):

    def test_visualize_alignments(self):
        ac = ADAMContext(self.ss)
        testFile = self.resourceFile('small.sam')
        reads = ac.loadAlignments(testFile)
        alignmentViz = AlignmentSummary(self.ss, ac, reads)
        contig = '16'
        start = 26472780
        end = 26482780
        x = alignmentViz.viewPileup(contig, start, end)
        assert x != None

    def test_indel_distribution(self):
        ac = ADAMContext(self.ss)
        testFile = self.resourceFile('small.sam')
        reads = ac.loadAlignments(testFile)
        bin_size = 10000000
        summary = AlignmentSummary(self.ss, ac, reads)
        indels = summary.getIndelDistribution(bin_size=10000000)
        _, mDistribution = indels.plot(testMode=True, plotType='M')
        expectedM = Counter({('1', 16 * bin_size): 225, ('1', 24 * bin_size): 150, ('1', 18 * bin_size): 150, ('1', 2 * bin_size): 150, 
         (
 '1', 23 * bin_size): 150, ('1', 1 * bin_size): 75, ('1', 0 * bin_size): 75, ('1', 15 * bin_size): 75, ('1', 20 * bin_size): 75, 
         (
 '1', 19 * bin_size): 75, ('1', 5 * bin_size): 75, ('1', 10 * bin_size): 75, ('1', 3 * bin_size): 75, ('1', 8 * bin_size): 75})
        assert mDistribution == expectedM
        _, iDistribution = indels.plot(testMode=True, plotType='I')
        expectedI = Counter({('1', 1 * bin_size): 0, ('1', 0 * bin_size): 0, ('1', 15 * bin_size): 0, ('1', 20 * bin_size): 0, 
         (
 '1', 19 * bin_size): 0, ('1', 24 * bin_size): 0, ('1', 18 * bin_size): 0, ('1', 16 * bin_size): 0, ('1', 5 * bin_size): 0, 
         (
 '1', 10 * bin_size): 0, ('1', 3 * bin_size): 0, ('1', 8 * bin_size): 0, ('1', 2 * bin_size): 0, ('1', 23 * bin_size): 0})
        assert iDistribution == expectedI

    def test_indel_distribution_maximal_bin_size(self):
        ac = ADAMContext(self.ss)
        testFile = self.resourceFile('small.sam')
        reads = ac.loadAlignments(testFile)
        summary = AlignmentSummary(self.ss, ac, reads)
        indels = summary.getIndelDistribution(bin_size=1000000000)
        _, mDistribution = indels.plot(testMode=True, plotType='M')
        expectedM = Counter({('1', 0): 1500})
        assert mDistribution == expectedM

    def test_indel_distribution_no_elements(self):
        ac = ADAMContext(self.ss)
        testFile = self.resourceFile('small.sam')
        reads = ac.loadAlignments(testFile)
        summary = AlignmentSummary((self.ss), ac, reads, sample=1e-05)
        indels = summary.getIndelDistribution(bin_size=1000000000)
        _, dDistribution = indels.plot(testMode=True, plotType='D')
        expectedD = Counter()
        assert dDistribution == expectedD

    def test_coverage_distribution(self):
        ac = ADAMContext(self.ss)
        testFile = self.resourceFile('small.sam')
        reads = ac.loadAlignments(testFile)
        summary = AlignmentSummary(self.ss, ac, reads)
        coverage = summary.getCoverageDistribution(bin_size=1)
        _, cd = coverage.plotDistributions(testMode=True, cumulative=False, normalize=False)
        items = list(cd.popitem()[1])
        assert len(items) == 1
        x = items.pop()
        assert x[0] == 1
        assert x[0] == 1
        assert x[1] == 1500

    def test_fragment_distribution(self):
        ac = ADAMContext(self.ss)
        testFile = self.resourceFile('small.sam')
        reads = ac.loadAlignments(testFile)
        summary = AlignmentSummary(self.ss, ac, reads)
        fragments = summary.getFragmentDistribution()
        _, cd = fragments.plotDistributions(testMode=True, cumulative=False, normalize=False)
        items = list(cd.popitem()[1])
        assert len(items) == 1
        x = items[0]
        assert x[0] == 75
        assert x[1] == 20

    def test_mapq_distribution(self):
        ac = ADAMContext(self.ss)
        testFile = self.resourceFile('small.sam')
        reads = ac.loadAlignments(testFile)
        summary = AlignmentSummary(self.ss, ac, reads)
        mapq = summary.getMapQDistribution()
        _, md = mapq.plotDistributions(testMode=True, cumulative=False, normalize=False)
        items = list(md.popitem()[1])
        assert len(items) == 5
        x = items[0]
        assert x[0] == 24
        assert x[1] == 1