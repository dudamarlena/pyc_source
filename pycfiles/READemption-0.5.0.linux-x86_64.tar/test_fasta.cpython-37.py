# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/anaconda3/lib/python3.7/site-packages/tests/test_fasta.py
# Compiled at: 2019-07-15 11:59:22
# Size of source mod 2**32: 1701 bytes
from io import StringIO
import unittest, sys
sys.path.append('.')
from reademptionlib.fasta import FastaParser

class TestFastaParser(unittest.TestCase):

    def setUp(self):
        self.fasta_parser = FastaParser()
        self.example_data = ExampleData()

    def test_parse_1(self):
        fasta_fh = StringIO(self.example_data.fasta_seqs_1)
        self.assertEqual(list(self.fasta_parser.entries(fasta_fh)), [
         ('test_1 a random sequence', 'TTTAGAAATTACACA'),
         ('test_2 another random sequence', 'ACGAGAAATTAAATTAAATT'),
         ('test_3 another random sequence', 'TAGAGACATTGGATTTTATT')])

    def test_parse_empty_file(self):
        fasta_fh = StringIO('')
        self.assertEqual(list(self.fasta_parser.entries(fasta_fh)), [])

    def test_single_entry_file_header(self):
        fasta_fh = StringIO(self.example_data.fasta_seqs_2)
        self.assertEqual(self.fasta_parser.single_entry_file_header(fasta_fh), 'test_4 a random sequence')

    def test_header_id_1(self):
        self.assertEqual(self.fasta_parser.header_id('seq_10101 An important protein'), 'seq_10101')

    def test_header_id_2(self):
        self.assertEqual(self.fasta_parser.header_id('seq_10101\tAn important protein'), 'seq_10101')


class ExampleData(object):
    fasta_seqs_1 = '>test_1 a random sequence\nTTTAG\nAAATT\nACACA\n>test_2 another random sequence\nACGAG\nAAATT\nAAATT\nAAATT\n>test_3 another random sequence\nTAGAG\nACATT\nGGATT\nTTATT\n'
    fasta_seqs_2 = '>test_4 a random sequence\nTTTAG\nAAATT\nACACA\n'


if __name__ == '__main__':
    unittest.main()