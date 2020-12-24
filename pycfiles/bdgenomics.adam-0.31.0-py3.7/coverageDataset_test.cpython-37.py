# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/bdgenomics/adam/test/coverageDataset_test.py
# Compiled at: 2020-01-08 15:53:47
# Size of source mod 2**32: 2705 bytes
from bdgenomics.adam.adamContext import ADAMContext
from bdgenomics.adam.rdd import CoverageDataset, FeatureDataset
from bdgenomics.adam.test import SparkTestCase
import os

class CoverageDatasetTest(SparkTestCase):

    def test_save(self):
        testFile = self.resourceFile('sorted.sam')
        ac = ADAMContext(self.ss)
        reads = ac.loadAlignments(testFile)
        coverage = reads.toCoverage()
        tmpPath = self.tmpFile() + '.coverage.adam'
        coverage.save(tmpPath, asSingleFile=True,
          disableFastConcat=True)
        assert os.listdir(tmpPath) != []

    def test_collapse(self):
        testFile = self.resourceFile('sorted.sam')
        ac = ADAMContext(self.ss)
        reads = ac.loadAlignments(testFile)
        coverage = reads.toCoverage()
        collapsed = coverage.collapse()
        self.assertEqual(collapsed.toDF().count(), coverage.toDF().count())

    def test_toFeatures(self):
        testFile = self.resourceFile('sorted.sam')
        ac = ADAMContext(self.ss)
        reads = ac.loadAlignments(testFile)
        coverage = reads.toCoverage()
        features = coverage.toFeatures()
        assert isinstance(features, FeatureDataset)
        self.assertEquals(features.toDF().count(), coverage.toDF().count())

    def test_aggregatedCoverage(self):
        testFile = self.resourceFile('small.sam')
        ac = ADAMContext(self.ss)
        reads = ac.loadAlignments(testFile)
        coverage = reads.toCoverage()
        collapsed = coverage.aggregatedCoverage(10)
        self.assertEqual(collapsed.toDF().count(), 166)

    def test_flatten(self):
        testFile = self.resourceFile('small.sam')
        ac = ADAMContext(self.ss)
        reads = ac.loadAlignments(testFile)
        coverage = reads.toCoverage()
        flattened = coverage.flatten()
        self.assertEqual(flattened.toDF().count(), 1500)