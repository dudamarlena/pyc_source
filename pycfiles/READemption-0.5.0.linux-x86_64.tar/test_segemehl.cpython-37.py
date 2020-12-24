# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/anaconda3/lib/python3.7/site-packages/tests/test_segemehl.py
# Compiled at: 2019-07-15 11:59:22
# Size of source mod 2**32: 10526 bytes
import hashlib, os, sys, unittest
sys.path.append('.')
from reademptionlib.segemehl import Segemehl

class TestSegemehl(unittest.TestCase):
    __doc__ = 'Provide general functionalities for tha actuall testing classes.'
    fasta_file_path = '/tmp/test.fa'
    index_file_path = '/tmp/test.idx'

    def setUp(self):
        self.segemehl = Segemehl(segemehl_bin='segemehl.x')
        self.example_data = ExampleData()
        self.maxDiff = None

    def _create_tmp_fasta_file(self, fasta_file_path, content):
        fasta_fh = open(fasta_file_path, 'w')
        fasta_fh.write(content)
        fasta_fh.close()

    def _sha1_of_file(self, file_path):
        fh = open(file_path, 'rb')
        content = fh.read()
        fh.close()
        return hashlib.sha1(content).hexdigest()

    def _remove_files(self, *args):
        for file_path in args:
            if os.path.exists(file_path):
                os.remove(file_path)


class TestSegemehlIndexBuilding(TestSegemehl):

    def test_build_index_lower_letters(self):
        self._create_tmp_fasta_file(self.fasta_file_path, self.example_data.genome_fasta_lower)
        self.segemehl.build_index([self.fasta_file_path], self.index_file_path)
        self.assertEqual(self._sha1_of_file(self.index_file_path), '78668505720e53735f807bb5485b0b38cc3cbc22')
        self._remove_files(self.fasta_file_path, self.index_file_path)

    def test_build_index_lower_letters(self):
        self._create_tmp_fasta_file(self.fasta_file_path, self.example_data.genome_fasta_upper)
        self.segemehl.build_index([self.fasta_file_path], self.index_file_path)
        self.assertEqual(self._sha1_of_file(self.index_file_path), '78668505720e53735f807bb5485b0b38cc3cbc22')
        self._remove_files(self.fasta_file_path, self.index_file_path)


class TestSegemehlAligning(TestSegemehl):
    read_fasta_file_path = '/tmp/test_reads.fa'
    aligning_result_path = '/tmp/test_aligning_results.sam'

    def setUp(self):
        super().setUp()
        self.large_output = LargeOutput()
        self._create_tmp_fasta_file(self.fasta_file_path, self.example_data.genome_fasta_upper)
        self.segemehl.build_index([self.fasta_file_path], self.index_file_path)

    def tearDown(self):
        self._remove_files(self.fasta_file_path, self.index_file_path)

    def test_align_reads_single_read_perfect_match(self):
        """
        ACAACATCCATGAACCGCATCAGCACCACCACCATTACCACCATCACCATTACCACAGGT
        ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        ACAACATCCATGAACCGCATCAGCACCACCACCATTACCACCATCACCATTACCACAGGT
        """
        read_file_content = '>read_01\nACAACATCCATGAACCGCATCAGCACCACCACCATTACCACCATCACCATTACCACAGGT\n'
        self.assertEqual(self._align_reads_and_give_result(read_file_content), self.large_output.sam_result_aligned_1)

    def test_map_reads_single_read_not_matching(self):
        """
        ACAACATCCATGAACCGCATCAGCACCACCACCATTACCACCATCACCATTACCACAGGT
        |       | |||     ||    |            |   ||  |            ||
        ATGTACCACATGAGAGAGATAGAGAGAGATTGACAACCACACACGAGAGAGAGAGAGAGT
        """
        read_file_content = '>read_02\nATGTACCACATGAGAGAGATAGAGAGAGATTGACAACCACACACGAGAGAGAGAGAGAGT\n'
        self.assertEqual(self._align_reads_and_give_result(read_file_content), self.large_output.sam_result_no_aligned_1)

    def test_map_reads_single_read_one_mismatch(self):
        """A 20 nt long read with 1 mismatch at 95% accu should be
        mapped.

        GCTTTTTTTTCGACCAGAGA
        |||||||||||||||||| |
        GCTTTTTTTTCGACCAGACA
        """
        read_file_content = '>read_03\nGCTTTTTTTTCGACCAGACA\n'
        self.assertEqual(self._align_reads_and_give_result(read_file_content), self.large_output.sam_result_aligned_2)

    def test_map_reads_single_read_two_mismatches_95(self):
        """A 20 nt long read with 2 mismatches at 95% accuracy should
        not be mapped.

        GCTTTTTTTTCGACCAGAGA
        |||||||||||||||||  |
        GCTTTTTTTTCGACCAGTCA
        """
        read_file_content = '>read_04\nGCTTTTTTTTCGACCAGTCA\n'
        self.assertEqual(self._align_reads_and_give_result(read_file_content), self.large_output.sam_result_no_aligned_1)

    def test_map_reads_single_read_two_mismatches_90(self):
        """A 20 nt long read with 2 mismatches at 90% accuracy should
        be mapped.

        GCTTTTTTTTCGACCAGAGA
        |||||||||||||||||  |
        GCTTTTTTTTCGACCAGTCA
        """
        read_file_content = '>read_05\nGCTTTTTTTTCGACCAGTCA\n'
        self.assertEqual(self._align_reads_and_give_result(read_file_content, accuracy=90), self.large_output.sam_result_aligned_3)

    def test_map_reads_single_read_three_mismatches(self):
        """A 20 nt long read with 3 mismatches at 90% accuracy should
        not be mapped.
        GCTTTTTTTTCGACCAGAGA
        ||||| |||||||||||  |
        GCTTTATTTTCGACCAGTCA
        """
        read_file_content = '>read_06\nGCTTTTTTTTCGACCAGTCA\n'
        self.assertEqual(self._align_reads_and_give_result(read_file_content), self.large_output.sam_result_no_aligned_1)

    def test_map_reads_single_too_short_read(self):
        """Reads that are too short should be mapped
        """
        read_file_content = '>read_07\nGCTTTTTTT\n'
        self.assertEqual(self._align_reads_and_give_result(read_file_content), self.large_output.sam_result_no_aligned_1)

    def _align_reads_and_give_result(self, read_file_content, **kwargs):
        """

        - read_file_content: the content of a read file (in fasta format)
        - **kwargs: are directly given to map_reads()
        """
        self._create_tmp_fasta_file(self.read_fasta_file_path, read_file_content)
        (self.segemehl.align_reads)((self.read_fasta_file_path), (self.index_file_path), 
         [
          self.fasta_file_path], (self.aligning_result_path), **kwargs)
        result_fh = open(self.aligning_result_path)
        result = result_fh.read()
        result_fh.close()
        return result


class ExampleData(object):
    genome_fasta_lower = '>SL1344 genome sequence\nagagattacgtctggttgcaagagatcatgacagggggaattggttgaaaataaatatat\ncgccagcagcacatgaacaagtttcggaatgtgatcaatttaaaaatttattgacttagg\ncgggcagatactttaaccaatataggaatacaagacagacaaataaaaatgacagagtac\nacaacatccatgaaccgcatcagcaccaccaccattaccaccatcaccattaccacaggt\naacggtgcgggctgacgcgtacaggaaacacagaaaaaagcccgcacctgaacagtgcgg\ngcttttttttcgaccagagatcacgaggtaacaaccatgcgagtgttgaagttcggcggt\nacatcagtggcaaatgcagaacgttttctgcgtgttgccgatattctggaaagcaatgcc\naggcaagggcaggtagcgaccgtactttccgcccccgcgaaaattaccaaccatctggtg\ngcaatgattgaaaaaactatcggcggccaggatgctttgccgaatatcagcgatgcagaa\ncgtattttttctgacctgctcgcaggacttgccagcgcgcagccgggattcccgcttgca\ncggttgaaaatggttgtcgaacaagaattcgctcagatcaaacatgttctgcatggtatc\nagcctgctgggtcagtgcccggatagcatcaacgccgcgctgatttgccgtggcgaaaaa\natgtcgatcgcgattatggcgggacttctggaggcgcgtgggcatcgcgtcacggtgatc\ngatccggtagaaaaattgctggcggtgggccattaccttgaatctaccgtcgatatcgcg\ngaatcgactcgccgtatcgccgccagccagatcccggccgatcacatgatcctgatggcg\nggctttaccgccggtaatgaaaagggtgaactggtggtgctgggccgtaatggttccgac\n'
    genome_fasta_upper = '>SL1344 genome sequence\nAGAGATTACGTCTGGTTGCAAGAGATCATGACAGGGGGAATTGGTTGAAAATAAATATAT\nCGCCAGCAGCACATGAACAAGTTTCGGAATGTGATCAATTTAAAAATTTATTGACTTAGG\nCGGGCAGATACTTTAACCAATATAGGAATACAAGACAGACAAATAAAAATGACAGAGTAC\nACAACATCCATGAACCGCATCAGCACCACCACCATTACCACCATCACCATTACCACAGGT\nAACGGTGCGGGCTGACGCGTACAGGAAACACAGAAAAAAGCCCGCACCTGAACAGTGCGG\nGCTTTTTTTTCGACCAGAGATCACGAGGTAACAACCATGCGAGTGTTGAAGTTCGGCGGT\nACATCAGTGGCAAATGCAGAACGTTTTCTGCGTGTTGCCGATATTCTGGAAAGCAATGCC\nAGGCAAGGGCAGGTAGCGACCGTACTTTCCGCCCCCGCGAAAATTACCAACCATCTGGTG\nGCAATGATTGAAAAAACTATCGGCGGCCAGGATGCTTTGCCGAATATCAGCGATGCAGAA\nCGTATTTTTTCTGACCTGCTCGCAGGACTTGCCAGCGCGCAGCCGGGATTCCCGCTTGCA\nCGGTTGAAAATGGTTGTCGAACAAGAATTCGCTCAGATCAAACATGTTCTGCATGGTATC\nAGCCTGCTGGGTCAGTGCCCGGATAGCATCAACGCCGCGCTGATTTGCCGTGGCGAAAAA\nATGTCGATCGCGATTATGGCGGGACTTCTGGAGGCGCGTGGGCATCGCGTCACGGTGATC\nGATCCGGTAGAAAAATTGCTGGCGGTGGGCCATTACCTTGAATCTACCGTCGATATCGCG\nGAATCGACTCGCCGTATCGCCGCCAGCCAGATCCCGGCCGATCACATGATCCTGATGGCG\nGGCTTTACCGCCGGTAATGAAAAGGGTGAACTGGTGGTGCTGGGCCGTAATGGTTCCGAC\n'


class LargeOutput(object):
    sam_result_aligned_1 = '@HD\tVN:1.0\n@SQ\tSN:SL1344\tLN:960\n@PG\tID:segemehl\tVN:0.2.0-$Rev: 418 $ ($Date: 2015-01-05 05:17:35 -0500 (Mon, 05 Jan 2015) $)\tCL:segemehl.x --query /tmp/test_reads.fa --index /tmp/test.idx --database /tmp/test.fa --outfile /tmp/test_aligning_results.sam --hitstrategy 1 --accuracy 95 --evalue 5.0 --threads 1 --silent\nread_01\t0\tSL1344\t181\t255\t60M\t*\t0\t0\tACAACATCCATGAACCGCATCAGCACCACCACCATTACCACCATCACCATTACCACAGGT\t*\tNM:i:0\tMD:Z:60\tNH:i:1\tXI:i:0\tXA:Z:Q\n'
    sam_result_aligned_2 = '@HD\tVN:1.0\n@SQ\tSN:SL1344\tLN:960\n@PG\tID:segemehl\tVN:0.2.0-$Rev: 418 $ ($Date: 2015-01-05 05:17:35 -0500 (Mon, 05 Jan 2015) $)\tCL:segemehl.x --query /tmp/test_reads.fa --index /tmp/test.idx --database /tmp/test.fa --outfile /tmp/test_aligning_results.sam --hitstrategy 1 --accuracy 95 --evalue 5.0 --threads 1 --silent\nread_03\t0\tSL1344\t301\t255\t20M\t*\t0\t0\tGCTTTTTTTTCGACCAGACA\t*\tNM:i:1\tMD:Z:18G1\tNH:i:1\tXI:i:0\tXA:Z:Q\n'
    sam_result_aligned_3 = '@HD\tVN:1.0\n@SQ\tSN:SL1344\tLN:960\n@PG\tID:segemehl\tVN:0.2.0-$Rev: 418 $ ($Date: 2015-01-05 05:17:35 -0500 (Mon, 05 Jan 2015) $)\tCL:segemehl.x --query /tmp/test_reads.fa --index /tmp/test.idx --database /tmp/test.fa --outfile /tmp/test_aligning_results.sam --hitstrategy 1 --accuracy 90 --evalue 5.0 --threads 1 --silent\nread_05\t0\tSL1344\t301\t255\t20M\t*\t0\t0\tGCTTTTTTTTCGACCAGTCA\t*\tNM:i:2\tMD:Z:17A0G1\tNH:i:1\tXI:i:0\tXA:Z:Q\n'
    sam_result_no_aligned_1 = '@HD\tVN:1.0\n@SQ\tSN:SL1344\tLN:960\n@PG\tID:segemehl\tVN:0.2.0-$Rev: 418 $ ($Date: 2015-01-05 05:17:35 -0500 (Mon, 05 Jan 2015) $)\tCL:segemehl.x --query /tmp/test_reads.fa --index /tmp/test.idx --database /tmp/test.fa --outfile /tmp/test_aligning_results.sam --hitstrategy 1 --accuracy 95 --evalue 5.0 --threads 1 --silent\n'


if __name__ == '__main__':
    unittest.main()