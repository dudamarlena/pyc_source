# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/bdgenomics/mango/test/notebook_test.py
# Compiled at: 2019-08-09 11:11:08
# Size of source mod 2**32: 2721 bytes
from bdgenomics.mango.test import SparkTestCase
from bdgenomics.adam.adamContext import ADAMContext

class NotebookTest(SparkTestCase):

    def test_example(self):
        spark = self.ss
        testMode = True
        alignmentFile = self.exampleFile('chr17.7500000-7515000.sam')
        variantFile = self.exampleFile('snv.chr17.7502100-7502500.vcf')
        genotypeFile = self.exampleFile('genodata.v3.vcf')
        featureFile = self.exampleFile('chr17.582500-594500.bed')
        testFile = self.exampleFile('notebooks/mango-viz.py')
        exec(open(testFile).read())

    def test_coverage_example(self):
        spark = self.ss
        testMode = True
        alignmentFile = self.exampleFile('chr17.7500000-7515000.sam')
        testCoverageFile = self.exampleFile('notebooks/mango-python-coverage.py')
        exec(open(testCoverageFile).read())

    def test_alignment_example(self):
        spark = self.ss
        testMode = True
        alignmentFile = self.exampleFile('chr17.7500000-7515000.sam')
        testAlignmentFile = self.exampleFile('notebooks/mango-python-alignment.py')
        exec(open(testAlignmentFile).read())

    def test_variants_example(self):
        spark = self.ss
        testMode = True
        vcfFile = self.exampleFile('genodata.v3.vcf')
        testVariantFile = self.exampleFile('notebooks/mango-python-variants.py')
        exec(open(testVariantFile).read())