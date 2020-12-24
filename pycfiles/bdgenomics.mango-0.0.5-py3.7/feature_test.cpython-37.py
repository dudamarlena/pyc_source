# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/bdgenomics/mango/test/feature_test.py
# Compiled at: 2019-01-29 15:49:04
# Size of source mod 2**32: 1365 bytes
from bdgenomics.mango.test import SparkTestCase
from bdgenomics.mango.features import *
from bdgenomics.adam.adamContext import ADAMContext

class FeatureTest(SparkTestCase):

    def test_visualize_features(self):
        ac = ADAMContext(self.ss)
        testFile = self.resourceFile('smalltest.bed')
        features = ac.loadFeatures(testFile)
        featureViz = FeatureSummary(ac, features)
        contig = 'chrM'
        start = 1
        end = 2000
        x = featureViz.viewPileup(contig, start, end)
        assert x != None