# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/bdgenomics/adam/test/genotypeDataset_test.py
# Compiled at: 2020-01-08 15:53:47
# Size of source mod 2**32: 9947 bytes
from bdgenomics.adam.adamContext import ADAMContext
from bdgenomics.adam.test import SparkTestCase

class GenotypeDatasetTest(SparkTestCase):

    def check_for_line_in_file(self, path, line):
        try:
            fp = open(path)
            foundLine = False
            for l in fp:
                if l.strip().rstrip() == line:
                    foundLine = True
                    break

            self.assertTrue(foundLine)
        finally:
            fp.close()

    def test_vcf_round_trip(self):
        testFile = self.resourceFile('small.vcf')
        ac = ADAMContext(self.ss)
        genotypes = ac.loadGenotypes(testFile)
        tmpPath = self.tmpFile() + '.vcf'
        genotypes.toVariantContexts().saveAsVcf(tmpPath)
        savedGenotypes = ac.loadGenotypes(testFile)
        self.assertEqual(genotypes._jvmRdd.jrdd().count(), savedGenotypes._jvmRdd.jrdd().count())

    def test_vcf_add_filter(self):
        testFile = self.resourceFile('small.vcf')
        ac = ADAMContext(self.ss)
        genotypes = ac.loadGenotypes(testFile)
        tmpPath = self.tmpFile() + '.vcf'
        genotypes.toVariantContexts().addFilterHeaderLine('BAD', 'Bad variant.').saveAsVcf(tmpPath)
        self.check_for_line_in_file(tmpPath, '##FILTER=<ID=BAD,Description="Bad variant.">')

    def test_vcf_add_format_array(self):
        testFile = self.resourceFile('small.vcf')
        ac = ADAMContext(self.ss)
        genotypes = ac.loadGenotypes(testFile)
        tmpPath = self.tmpFile() + '.vcf'
        genotypes.toVariantContexts().addFixedArrayFormatHeaderLine('FA4', 4, 'Fixed array of 4 elements.', int).saveAsVcf(tmpPath)
        self.check_for_line_in_file(tmpPath, '##FORMAT=<ID=FA4,Number=4,Type=Integer,Description="Fixed array of 4 elements.">')

    def test_vcf_add_format_scalar(self):
        testFile = self.resourceFile('small.vcf')
        ac = ADAMContext(self.ss)
        genotypes = ac.loadGenotypes(testFile)
        tmpPath = self.tmpFile() + '.vcf'
        genotypes.toVariantContexts().addScalarFormatHeaderLine('SC', 'Scalar.', str).saveAsVcf(tmpPath)
        self.check_for_line_in_file(tmpPath, '##FORMAT=<ID=SC,Number=1,Type=String,Description="Scalar.">')

    def test_vcf_add_format_genotype_array(self):
        testFile = self.resourceFile('small.vcf')
        ac = ADAMContext(self.ss)
        genotypes = ac.loadGenotypes(testFile)
        tmpPath = self.tmpFile() + '.vcf'
        genotypes.toVariantContexts().addGenotypeArrayFormatHeaderLine('GA', 'Array with # genotypes.', float).saveAsVcf(tmpPath)
        self.check_for_line_in_file(tmpPath, '##FORMAT=<ID=GA,Number=G,Type=Float,Description="Array with # genotypes.">')

    def test_vcf_add_format_alts_array(self):
        testFile = self.resourceFile('small.vcf')
        ac = ADAMContext(self.ss)
        genotypes = ac.loadGenotypes(testFile)
        tmpPath = self.tmpFile() + '.vcf'
        genotypes.toVariantContexts().addAlternateAlleleArrayFormatHeaderLine('AA', 'Array with # alts.', chr).saveAsVcf(tmpPath)
        self.check_for_line_in_file(tmpPath, '##FORMAT=<ID=AA,Number=A,Type=Character,Description="Array with # alts.">')

    def test_vcf_add_format_all_array(self):
        testFile = self.resourceFile('small.vcf')
        ac = ADAMContext(self.ss)
        genotypes = ac.loadGenotypes(testFile)
        tmpPath = self.tmpFile() + '.vcf'
        genotypes.toVariantContexts().addAllAlleleArrayFormatHeaderLine('RA', 'Array with # alleles.', float).saveAsVcf(tmpPath)
        self.check_for_line_in_file(tmpPath, '##FORMAT=<ID=RA,Number=R,Type=Float,Description="Array with # alleles.">')

    def test_vcf_add_info_array(self):
        testFile = self.resourceFile('small.vcf')
        ac = ADAMContext(self.ss)
        genotypes = ac.loadGenotypes(testFile)
        tmpPath = self.tmpFile() + '.vcf'
        genotypes.toVariantContexts().addFixedArrayInfoHeaderLine('FA4', 4, 'Fixed array of 4 elements.', int).saveAsVcf(tmpPath)
        self.check_for_line_in_file(tmpPath, '##INFO=<ID=FA4,Number=4,Type=Integer,Description="Fixed array of 4 elements.">')

    def test_vcf_add_info_scalar(self):
        testFile = self.resourceFile('small.vcf')
        ac = ADAMContext(self.ss)
        genotypes = ac.loadGenotypes(testFile)
        tmpPath = self.tmpFile() + '.vcf'
        genotypes.toVariantContexts().addScalarInfoHeaderLine('SC', 'Scalar.', bool).saveAsVcf(tmpPath)
        self.check_for_line_in_file(tmpPath, '##INFO=<ID=SC,Number=0,Type=Flag,Description="Scalar.">')

    def test_vcf_add_info_alts_array(self):
        testFile = self.resourceFile('small.vcf')
        ac = ADAMContext(self.ss)
        genotypes = ac.loadGenotypes(testFile)
        tmpPath = self.tmpFile() + '.vcf'
        genotypes.toVariantContexts().addAlternateAlleleArrayInfoHeaderLine('AA', 'Array with # alts.', chr).saveAsVcf(tmpPath)
        self.check_for_line_in_file(tmpPath, '##INFO=<ID=AA,Number=A,Type=Character,Description="Array with # alts.">')

    def test_vcf_add_info_all_array(self):
        testFile = self.resourceFile('small.vcf')
        ac = ADAMContext(self.ss)
        genotypes = ac.loadGenotypes(testFile)
        tmpPath = self.tmpFile() + '.vcf'
        genotypes.toVariantContexts().addAllAlleleArrayInfoHeaderLine('RA', 'Array with # alleles.', float).saveAsVcf(tmpPath)
        self.check_for_line_in_file(tmpPath, '##INFO=<ID=RA,Number=R,Type=Float,Description="Array with # alleles.">')

    def test_vcf_sort(self):
        testFile = self.resourceFile('random.vcf')
        ac = ADAMContext(self.ss)
        genotypes = ac.loadGenotypes(testFile)
        tmpPath = self.tmpFile() + '.vcf'
        genotypes.toVariantContexts().sort().saveAsVcf(tmpPath, asSingleFile=True)
        self.checkFiles(tmpPath, self.resourceFile('sorted.vcf', module='adam-cli'))

    def test_vcf_sort_lex(self):
        testFile = self.resourceFile('random.vcf')
        ac = ADAMContext(self.ss)
        genotypes = ac.loadGenotypes(testFile)
        tmpPath = self.tmpFile() + '.vcf'
        genotypes.toVariantContexts().sortLexicographically().saveAsVcf(tmpPath, asSingleFile=True)
        self.checkFiles(tmpPath, self.resourceFile('sorted.lex.vcf', module='adam-cli'))

    def test_transform(self):
        testFile = self.resourceFile('random.vcf')
        ac = ADAMContext(self.ss)
        genotypes = ac.loadGenotypes(testFile)
        transformedGenotypes = genotypes.transform(lambda x: x.filter(x.referenceName == '1'))
        self.assertEqual(transformedGenotypes.toDF().count(), 9)

    def test_to_variants(self):
        testFile = self.resourceFile('small.vcf')
        ac = ADAMContext(self.ss)
        genotypes = ac.loadGenotypes(testFile)
        variants = genotypes.toVariants()
        self.assertEqual(variants.toDF().count(), 18)
        variants = genotypes.toVariants(dedupe=True)
        self.assertEqual(variants.toDF().count(), 6)