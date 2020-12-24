# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/anaconda3/lib/python3.7/site-packages/tests/test_genewisequanti.py
# Compiled at: 2019-07-15 11:59:22
# Size of source mod 2**32: 6116 bytes
import unittest, os, sys
sys.path.append('.')
from reademptionlib.genewisequanti import GeneWiseQuantification
import pysam

class Gff3EntryMoc(object):

    def __init__(self, seq_id, start, end):
        self.seq_id = seq_id
        self.start = start
        self.end = end


class TestGeneWiseQuantification(unittest.TestCase):

    def setUp(self):
        self.example_data = ExampleData()
        self._sam_bam_prefix = 'dummy'
        self.gene_wise_quantification = GeneWiseQuantification()

    def tearDown(self):
        for suffix in ('.sam', '.bam', '.bam.bai'):
            os.remove(self._sam_bam_prefix + suffix)

    def test_overlapping_alignments_1(self):
        self._generate_bam_file(self.example_data.sam_content_1, self._sam_bam_prefix)
        self.gene_wise_quantification = GeneWiseQuantification()
        sam = pysam.Samfile(self._sam_bam_prefix + '.bam')
        self.assertListEqual(self._mapping_ids(self.gene_wise_quantification._overlapping_alignments(sam, Gff3EntryMoc('chrom', 1, 100))), [
         'myread:01', 'myread:02', 'myread:03', 'myread:04', 'myread:05',
         'myread:06', 'myread:07', 'myread:08', 'myread:09', 'myread:10'])
        self.assertListEqual(self._mapping_ids(self.gene_wise_quantification._overlapping_alignments(sam, Gff3EntryMoc('chrom', 1, 5))), [])
        self.assertListEqual(self._mapping_ids(self.gene_wise_quantification._overlapping_alignments(sam, Gff3EntryMoc('chrom', 1, 10))), [
         'myread:01', 'myread:02', 'myread:03', 'myread:04', 'myread:05'])
        self.assertListEqual(self._mapping_ids(self.gene_wise_quantification._overlapping_alignments(sam, Gff3EntryMoc('chrom', 1, 9))), [])
        self.assertListEqual(self._mapping_ids(self.gene_wise_quantification._overlapping_alignments(sam, Gff3EntryMoc('chrom', 19, 23))), [
         'myread:01', 'myread:02', 'myread:03', 'myread:04', 'myread:05'])
        self.assertListEqual(self._mapping_ids(self.gene_wise_quantification._overlapping_alignments(sam, Gff3EntryMoc('chrom', 20, 23))), [])

    def test_overlapping_alignments_2(self):
        """Extraction of overlapping reads - with a non-default
        minimal overlap.
        """
        self._generate_bam_file(self.example_data.sam_content_1, self._sam_bam_prefix)
        self.gene_wise_quantification = GeneWiseQuantification()
        self.gene_wise_quantification._min_overlap = 5
        sam = pysam.Samfile(self._sam_bam_prefix + '.bam')
        self.assertListEqual(self._mapping_ids(self.gene_wise_quantification._overlapping_alignments(sam, Gff3EntryMoc('chrom', 1, 10))), [])
        self.assertListEqual(self._mapping_ids(self.gene_wise_quantification._overlapping_alignments(sam, Gff3EntryMoc('chrom', 1, 13))), [])
        self.assertListEqual(self._mapping_ids(self.gene_wise_quantification._overlapping_alignments(sam, Gff3EntryMoc('chrom', 1, 14))), [
         'myread:01', 'myread:02', 'myread:03', 'myread:04', 'myread:05'])
        self.assertListEqual(self._mapping_ids(self.gene_wise_quantification._overlapping_alignments(sam, Gff3EntryMoc('chrom', 19, 23))), [])
        self.assertListEqual(self._mapping_ids(self.gene_wise_quantification._overlapping_alignments(sam, Gff3EntryMoc('chrom', 16, 23))), [])
        self.assertListEqual(self._mapping_ids(self.gene_wise_quantification._overlapping_alignments(sam, Gff3EntryMoc('chrom', 15, 23))), [
         'myread:01', 'myread:02', 'myread:03', 'myread:04', 'myread:05'])

    def _mapping_ids(self, mappings):
        return [mapping.qname for mapping in mappings]

    def _generate_bam_file(self, sam_content, file_prefix):
        sam_file = '{}.sam'.format(file_prefix)
        bam_file = '{}.bam'.format(file_prefix)
        sam_fh = open(sam_file, 'w')
        sam_fh.write(sam_content)
        sam_fh.close()
        pysam.view('-Sb',
          ('-o{}'.format(bam_file)), sam_file, catch_stdout=False)
        pysam.index(bam_file)


class ExampleData(object):
    sam_content_1 = '@HD\tVN:1.0\n@SQ\tSN:chrom\tLN:1500\n@SQ\tSN:plasmid1\tLN:100\n@SQ\tSN:plasmid2\tLN:200\nmyread:01\t0\tchrom\t10\t255\t10M\t*\t0\t0\tGTGGACAACC\t*\tNM:i:1\tMD:Z:11T3\tNH:i:1\tXI:i:1\tXA:Z:Q\nmyread:02\t0\tchrom\t10\t255\t10M\t*\t0\t0\tGTGGACAACC\t*\tNM:i:1\tMD:Z:11T3\tNH:i:1\tXI:i:1\tXA:Z:Q\nmyread:03\t0\tchrom\t10\t255\t10M\t*\t0\t0\tGTGGACAACC\t*\tNM:i:1\tMD:Z:11T3\tNH:i:1\tXI:i:1\tXA:Z:Q\nmyread:04\t0\tchrom\t10\t255\t10M\t*\t0\t0\tGTGGACAACC\t*\tNM:i:1\tMD:Z:11T3\tNH:i:1\tXI:i:1\tXA:Z:Q\nmyread:05\t0\tchrom\t10\t255\t10M\t*\t0\t0\tGTGGACAACC\t*\tNM:i:1\tMD:Z:11T3\tNH:i:1\tXI:i:1\tXA:Z:Q\nmyread:06\t16\tchrom\t35\t255\t10M\t*\t0\t0\tGTGGACAACC\t*\tNM:i:1\tMD:Z:11T3\tNH:i:1\tXI:i:1\tXA:Z:Q\nmyread:07\t16\tchrom\t35\t255\t10M\t*\t0\t0\tGTGGACAACC\t*\tNM:i:1\tMD:Z:11T3\tNH:i:1\tXI:i:1\tXA:Z:Q\nmyread:08\t16\tchrom\t35\t255\t10M\t*\t0\t0\tGTGGACAACC\t*\tNM:i:1\tMD:Z:11T3\tNH:i:1\tXI:i:1\tXA:Z:Q\nmyread:09\t16\tchrom\t35\t255\t10M\t*\t0\t0\tGTGGACAACC\t*\tNM:i:1\tMD:Z:11T3\tNH:i:1\tXI:i:1\tXA:Z:Q\nmyread:10\t16\tchrom\t35\t255\t10M\t*\t0\t0\tGTGGACAACC\t*\tNM:i:1\tMD:Z:11T3\tNH:i:1\tXI:i:1\tXA:Z:Q\n'


if __name__ == '__main__':
    unittest.main()