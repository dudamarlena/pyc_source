# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/bdgenomics/mango/test/genotypes_test.py
# Compiled at: 2019-08-09 11:11:08
# Size of source mod 2**32: 3588 bytes
from bdgenomics.mango.test import SparkTestCase
from bdgenomics.mango.genotypes import *
from bdgenomics.adam.adamContext import ADAMContext

class GenotypesTest(SparkTestCase):

    def test_VariantsPerSampleDistribution(self):
        ac = ADAMContext(self.ss)
        testFile = self.resourceFile('genodata.v3.test.vcf')
        genotypes = ac.loadGenotypes(testFile)
        _, data = VariantsPerSampleDistribution(self.ss, genotypes).plotDistributions(testMode=True)
        expected = [
         6, 8, 8, 1, 7, 8]
        assert sum(data) == sum(expected)

    def test_VariantsPerSampleDistributionSampling(self):
        ac = ADAMContext(self.ss)
        testFile = self.resourceFile('genodata.v3.test.vcf')
        genotypes = ac.loadGenotypes(testFile)
        _, data = VariantsPerSampleDistribution((self.ss), genotypes, sample=0.9).plotDistributions(testMode=True)
        expected = [
         6, 8, 8, 1, 7, 8]
        dev = 8
        if not (sum(expected) > sum(data) - dev and sum(expected) < sum(data) + dev):
            raise AssertionError

    def test_HetHomRatioDistribution(self):
        ac = ADAMContext(self.ss)
        testFile = self.resourceFile('genodata.v3.test.vcf')
        genotypes = ac.loadGenotypes(testFile)
        _, data = HetHomRatioDistribution((self.ss), genotypes, sample=1.0).plot(testMode=True)
        expected = sorted([5.0, 0.6, 0.14, 0.17, 1.67])
        sorted_data = sorted(data)
        assert expected == [round(x, 2) for x in sorted_data]

    def test_GenotypeCallRatesDistribution(self):
        ac = ADAMContext(self.ss)
        testFile = self.resourceFile('genodata.v3.test.vcf')
        genotypes = ac.loadGenotypes(testFile)
        _, data = GenotypeCallRatesDistribution((self.ss), genotypes, sample=1.0).plot(testMode=True)
        expected = sorted([0.95, 0.88, 0.89, 0.94, 0.93, 0.9])
        sorted_data = sorted(data)
        assert expected == [round(x, 2) for x in sorted_data]

    def test_GenotypeSummary(self):
        ac = ADAMContext(self.ss)
        testFile = self.resourceFile('genodata.v3.test.vcf')
        genotypes = ac.loadGenotypes(testFile)
        gs = GenotypeSummary(self.ss, ac, genotypes)
        _, data = gs.getVariantsPerSampleDistribution().plotDistributions(testMode=True)
        expected = [
         6, 8, 8, 1, 7, 8]
        assert sum(data) == sum(expected)

    def test_visualize_genotypes(self):
        ac = ADAMContext(self.ss)
        testFile = self.resourceFile('genodata.v3.test.vcf')
        genotypes = ac.loadGenotypes(testFile)
        gs = GenotypeSummary(self.ss, ac, genotypes)
        contig = 'chr22'
        start = 21079600
        end = 21079700
        x = gs.viewPileup(contig, start, end)
        assert x != None