# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/bdgenomics/mango/test/variant_test.py
# Compiled at: 2019-01-29 15:49:04
# Size of source mod 2**32: 1337 bytes
from bdgenomics.mango.test import SparkTestCase
from bdgenomics.mango.variants import *
from bdgenomics.adam.adamContext import ADAMContext

class VariantTest(SparkTestCase):

    def test_visualize_variants(self):
        ac = ADAMContext(self.ss)
        testFile = self.resourceFile('bqsr1.vcf')
        variants = ac.loadVariants(testFile)
        variantViz = VariantSummary(ac, variants)
        contig = 'chrM'
        start = 1
        end = 2000
        x = variantViz.viewPileup(contig, start, end)
        assert x != None