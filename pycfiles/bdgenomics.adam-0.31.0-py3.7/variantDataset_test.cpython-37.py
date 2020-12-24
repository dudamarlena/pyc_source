# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/bdgenomics/adam/test/variantDataset_test.py
# Compiled at: 2020-01-08 15:53:47
# Size of source mod 2**32: 1701 bytes
from bdgenomics.adam.adamContext import ADAMContext
from bdgenomics.adam.test import SparkTestCase

class VariantDatasetTest(SparkTestCase):

    def test_vcf_round_trip(self):
        testFile = self.resourceFile('small.vcf')
        ac = ADAMContext(self.ss)
        variants = ac.loadVariants(testFile)
        tmpPath = self.tmpFile() + '.vcf'
        variants.toVariantContexts().saveAsVcf(tmpPath)
        savedVariants = ac.loadVariants(testFile)
        self.assertEqual(variants._jvmRdd.jrdd().count(), savedVariants._jvmRdd.jrdd().count())

    def test_transform(self):
        variantPath = self.resourceFile('small.vcf')
        ac = ADAMContext(self.ss)
        variants = ac.loadVariants(variantPath)
        transformedVariants = variants.transform(lambda x: x.filter(x.start < 19190))
        self.assertEqual(transformedVariants.toDF().count(), 3)