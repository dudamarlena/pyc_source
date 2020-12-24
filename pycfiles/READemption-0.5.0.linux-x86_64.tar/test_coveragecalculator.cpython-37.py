# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/anaconda3/lib/python3.7/site-packages/tests/test_coveragecalculator.py
# Compiled at: 2019-07-15 11:59:22
# Size of source mod 2**32: 7321 bytes
import sys, os, unittest
sys.path.append('.')
from reademptionlib.coveragecalculator import CoverageCalculator
from io import StringIO
import pysam

class TestCoverageCalculator(unittest.TestCase):

    def setUp(self):
        self.coverage_calculator = CoverageCalculator()
        self.example_data = ExampleData()
        self._sam_bam_prefix = 'dummy'

    def tearDown(self):
        for suffix in ('.sam', '.bam', '.bam.bai'):
            if os.path.exists(self._sam_bam_prefix + suffix) is True:
                os.remove(self._sam_bam_prefix + suffix)

    def _generate_bam_file(self, sam_content, file_prefix):
        sam_file = '{}.sam'.format(file_prefix)
        bam_file = '{}.bam'.format(file_prefix)
        sam_fh = open(sam_file, 'w')
        sam_fh.write(sam_content)
        sam_fh.close()
        pysam.view('-Sb',
          ('-o{}'.format(bam_file)), sam_file, catch_stdout=False)
        pysam.index(bam_file)
        self._bam = pysam.Samfile(bam_file)

    def test_init_coverage_list(self):
        self.coverage_calculator._init_coverage_list(10)
        self.assertListEqual(sorted(self.coverage_calculator._coverages.keys()), [
         'forward', 'reverse'])
        self.assertListEqual(self.coverage_calculator._coverages['forward'].tolist(), [0.0] * 10)
        self.assertListEqual(self.coverage_calculator._coverages['reverse'].tolist(), [0.0] * 10)

    def test_calc_coverage_1(self):
        """Check correct start at first list element"""
        self._generate_bam_file(self.example_data.sam_content_1, self._sam_bam_prefix)
        self.coverage_calculator._init_coverage_list(self._bam.lengths[0])
        self.coverage_calculator._calc_coverage('chrom', self._bam)
        self.assertEqual(len(self.coverage_calculator._coverages['forward']), 1500)
        self.assertListEqual(self.coverage_calculator._coverages['forward'][0:15].tolist(), [
         5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0,
         0.0, 0.0, 0.0, 0.0, 0.0])
        self.assertListEqual(self.coverage_calculator._coverages['reverse'][0:15].tolist(), [
         -5.0, -5.0, -5.0, -5.0, -5.0, -5.0, -5.0, -5.0, -5.0, -5.0,
         0.0, 0.0, 0.0, 0.0, 0.0])

    def test_calc_coverage_2(self):
        """Consider how often a read is mapped. Mappings of reads that
        are aligned to several location contribute only fractions to
        the counting.

        """
        self._generate_bam_file(self.example_data.sam_content_2, self._sam_bam_prefix)
        self.coverage_calculator._init_coverage_list(self._bam.lengths[0])
        self.coverage_calculator._calc_coverage('chrom', self._bam)
        self.assertListEqual(self.coverage_calculator._coverages['forward'][0:15].tolist(), [
         0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
         0.0, 0.0, 0.0, 0.0, 0.0])

    def test_calc_coverage_3(self):
        """If read_count_splitting is set to False then every
        mapping is counted as one to each of the matching position
        independent how often its read is mapped in in total.
        """
        self.coverage_calculator = CoverageCalculator(read_count_splitting=False)
        self._generate_bam_file(self.example_data.sam_content_2, self._sam_bam_prefix)
        self.coverage_calculator._init_coverage_list(self._bam.lengths[0])
        self.coverage_calculator._calc_coverage('chrom', self._bam)
        self.assertListEqual(self.coverage_calculator._coverages['forward'][0:15].tolist(), [
         1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
         0.0, 0.0, 0.0, 0.0, 0.0])

    def test_calc_coverage_4(self):
        """If uniqueley_aligned_only is True skip any mapping of read
        that are aligned to more than on location.
        """
        self.coverage_calculator = CoverageCalculator(uniquely_aligned_only=True)
        self._generate_bam_file(self.example_data.sam_content_3, self._sam_bam_prefix)
        self.coverage_calculator._init_coverage_list(self._bam.lengths[0])
        self.coverage_calculator._calc_coverage('chrom', self._bam)
        self.assertListEqual(self.coverage_calculator._coverages['forward'][0:15].tolist(), [
         3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0,
         0.0, 0.0, 0.0, 0.0, 0.0])

    def test_calc_coverage_5(self):
        """If first_base_only is True only the first nucleotide of a
        mapping is considered.
        """
        self.coverage_calculator = CoverageCalculator(coverage_style='first_base_only')
        self._generate_bam_file(self.example_data.sam_content_1, self._sam_bam_prefix)
        self.coverage_calculator._init_coverage_list(self._bam.lengths[0])
        self.coverage_calculator._calc_coverage('chrom', self._bam)
        self.assertListEqual(self.coverage_calculator._coverages['forward'][0:15].tolist(), [
         5.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
         0.0, 0.0, 0.0, 0.0, 0.0])
        self.assertListEqual(self.coverage_calculator._coverages['reverse'][0:15].tolist(), [
         0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -5.0,
         0.0, 0.0, 0.0, 0.0, 0.0])


class ExampleData(object):
    sam_content_1 = '@HD\tVN:1.0\n@SQ\tSN:chrom\tLN:1500\n@SQ\tSN:plasmid1\tLN:100\n@SQ\tSN:plasmid2\tLN:200\nmyread:001\t0\tchrom\t1\t255\t10M\t*\t0\t0\tGTGGACAACC\t*\tNM:i:1\tMD:Z:11T3\tNH:i:1\tXI:i:1\tXA:Z:Q\nmyread:002\t0\tchrom\t1\t255\t10M\t*\t0\t0\tGTGGACAACC\t*\tNM:i:1\tMD:Z:11T3\tNH:i:1\tXI:i:1\tXA:Z:Q\nmyread:003\t0\tchrom\t1\t255\t10M\t*\t0\t0\tGTGGACAACC\t*\tNM:i:1\tMD:Z:11T3\tNH:i:1\tXI:i:1\tXA:Z:Q\nmyread:004\t0\tchrom\t1\t255\t10M\t*\t0\t0\tGTGGACAACC\t*\tNM:i:1\tMD:Z:11T3\tNH:i:1\tXI:i:1\tXA:Z:Q\nmyread:005\t0\tchrom\t1\t255\t10M\t*\t0\t0\tGTGGACAACC\t*\tNM:i:1\tMD:Z:11T3\tNH:i:1\tXI:i:1\tXA:Z:Q\nmyread:006\t16\tchrom\t1\t255\t10M\t*\t0\t0\tGTGGACAACC\t*\tNM:i:1\tMD:Z:11T3\tNH:i:1\tXI:i:1\tXA:Z:Q\nmyread:007\t16\tchrom\t1\t255\t10M\t*\t0\t0\tGTGGACAACC\t*\tNM:i:1\tMD:Z:11T3\tNH:i:1\tXI:i:1\tXA:Z:Q\nmyread:008\t16\tchrom\t1\t255\t10M\t*\t0\t0\tGTGGACAACC\t*\tNM:i:1\tMD:Z:11T3\tNH:i:1\tXI:i:1\tXA:Z:Q\nmyread:009\t16\tchrom\t1\t255\t10M\t*\t0\t0\tGTGGACAACC\t*\tNM:i:1\tMD:Z:11T3\tNH:i:1\tXI:i:1\tXA:Z:Q\nmyread:010\t16\tchrom\t1\t255\t10M\t*\t0\t0\tGTGGACAACC\t*\tNM:i:1\tMD:Z:11T3\tNH:i:1\tXI:i:1\tXA:Z:Q\n'
    sam_content_2 = '@HD\tVN:1.0\n@SQ\tSN:chrom\tLN:1500\n@SQ\tSN:plasmid1\tLN:100\n@SQ\tSN:plasmid2\tLN:200\nmyread:001\t0\tchrom\t1\t255\t10M\t*\t0\t0\tGTGGACAACC\t*\tNM:i:1\tMD:Z:11T3\tNH:i:2\tXI:i:1\tXA:Z:Q\n'
    sam_content_3 = '@HD\tVN:1.0\n@SQ\tSN:chrom\tLN:1500\n@SQ\tSN:plasmid1\tLN:100\n@SQ\tSN:plasmid2\tLN:200\nmyread:001\t0\tchrom\t1\t255\t10M\t*\t0\t0\tGTGGACAACC\t*\tNM:i:1\tMD:Z:11T3\tNH:i:1\tXI:i:1\tXA:Z:Q\nmyread:002\t0\tchrom\t1\t255\t10M\t*\t0\t0\tGTGGACAACC\t*\tNM:i:1\tMD:Z:11T3\tNH:i:1\tXI:i:1\tXA:Z:Q\nmyread:003\t0\tchrom\t1\t255\t10M\t*\t0\t0\tGTGGACAACC\t*\tNM:i:1\tMD:Z:11T3\tNH:i:1\tXI:i:1\tXA:Z:Q\nmyread:004\t0\tchrom\t5\t255\t10M\t*\t0\t0\tGTGGACAACC\t*\tNM:i:1\tMD:Z:11T3\tNH:i:9\tXI:i:1\tXA:Z:Q\nmyread:005\t0\tchrom\t5\t255\t10M\t*\t0\t0\tGTGGACAACC\t*\tNM:i:1\tMD:Z:11T3\tNH:i:9\tXI:i:1\tXA:Z:Q\nmyread:006\t0\tchrom\t5\t255\t10M\t*\t0\t0\tGTGGACAACC\t*\tNM:i:1\tMD:Z:11T3\tNH:i:9\tXI:i:1\tXA:Z:Q\n'


if __name__ == '__main__':
    unittest.main()