# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/bdgenomics/adam/test/featureDataset_test.py
# Compiled at: 2020-01-08 15:53:47
# Size of source mod 2**32: 3275 bytes
from bdgenomics.adam.adamContext import ADAMContext
from bdgenomics.adam.test import SparkTestCase

class FeatureDatasetTest(SparkTestCase):

    def test_round_trip_gtf(self):
        testFile = self.resourceFile('Homo_sapiens.GRCh37.75.trun20.gtf')
        ac = ADAMContext(self.ss)
        features = ac.loadFeatures(testFile)
        tmpPath = self.tmpFile() + '.gtf'
        features.save(tmpPath, asSingleFile=True)
        savedFeatures = ac.loadFeatures(testFile)
        self.assertEqual(features._jvmRdd.jrdd().count(), savedFeatures._jvmRdd.jrdd().count())

    def test_round_trip_bed(self):
        testFile = self.resourceFile('gencode.v7.annotation.trunc10.bed')
        ac = ADAMContext(self.ss)
        features = ac.loadFeatures(testFile)
        tmpPath = self.tmpFile() + '.bed'
        features.save(tmpPath, asSingleFile=True)
        savedFeatures = ac.loadFeatures(testFile)
        self.assertEqual(features._jvmRdd.jrdd().count(), savedFeatures._jvmRdd.jrdd().count())

    def test_round_trip_narrowPeak(self):
        testFile = self.resourceFile('wgEncodeOpenChromDnaseGm19238Pk.trunc10.narrowPeak')
        ac = ADAMContext(self.ss)
        features = ac.loadFeatures(testFile)
        tmpPath = self.tmpFile() + '.narrowPeak'
        features.save(tmpPath, asSingleFile=True)
        savedFeatures = ac.loadFeatures(testFile)
        self.assertEqual(features._jvmRdd.jrdd().count(), savedFeatures._jvmRdd.jrdd().count())

    def test_round_trip_interval_list(self):
        testFile = self.resourceFile('SeqCap_EZ_Exome_v3.hg19.interval_list')
        ac = ADAMContext(self.ss)
        features = ac.loadFeatures(testFile)
        tmpPath = self.tmpFile() + '.interval_list'
        features.save(tmpPath, asSingleFile=True)
        savedFeatures = ac.loadFeatures(testFile)
        self.assertEqual(features._jvmRdd.jrdd().count(), savedFeatures._jvmRdd.jrdd().count())

    def test_transform(self):
        featurePath = self.resourceFile('gencode.v7.annotation.trunc10.bed')
        ac = ADAMContext(self.ss)
        features = ac.loadFeatures(featurePath)
        transformedFeatures = features.transform(lambda x: x.filter(x.start < 12613))
        self.assertEqual(transformedFeatures.toDF().count(), 6)