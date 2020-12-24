# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/anaconda3/lib/python3.7/site-packages/tests/test_fastq.py
# Compiled at: 2019-07-15 11:59:22
# Size of source mod 2**32: 1771 bytes
from io import StringIO
import unittest, sys
sys.path.append('.')
from reademptionlib.fastq import FastqParser

class TestFastqParser(unittest.TestCase):

    def setUp(self):
        self.fastq_parser = FastqParser()
        self.example_data = ExampleData()

    def test_parse_1(self):
        fastq_fh = StringIO(self.example_data.fastq_seqs_1)
        self.assertEqual(list(self.fastq_parser.entries(fastq_fh)), [
         ('test_1 a random sequence', 'TTTAGAAATTACACA'),
         ('test_2 another random sequence', 'ACGAGAAATTAAATTAAATT'),
         ('test_3 another random sequence', 'TAGAGACATTGGATTTTATT')])

    def test_parse_empty_file(self):
        fastq_fh = StringIO('')
        self.assertEqual(list(self.fastq_parser.entries(fastq_fh)), [])

    def test_single_entry_file_header(self):
        fastq_fh = StringIO(self.example_data.fastq_seqs_2)
        self.assertEqual(self.fastq_parser.single_entry_file_header(fastq_fh), 'test_4 a random sequence')

    def test_header_id_1(self):
        self.assertEqual(self.fastq_parser.header_id('seq_10101 An important protein'), 'seq_10101')

    def test_header_id_2(self):
        self.assertEqual(self.fastq_parser.header_id('seq_10101\tAn important protein'), 'seq_10101')


class ExampleData(object):
    fastq_seqs_1 = '@test_1 a random sequence\nTTTAGAAATTACACA\n+\n!!!!!!!!!!!!!!!\n@test_2 another random sequence\nACGAGAAATTAAATTAAATT\n+\n@@@@@@@@@@@@@@@@@@@@\n@test_3 another random sequence\nTAGAGACATTGGATTTTATT\n+\n!!!!!!!!!!!!!!!!!!!!\n'
    fastq_seqs_2 = '@test_4 a random sequence\nTTTAGAAATTACACA\n+\n!!!!!!!!!!!!!!!\n'


if __name__ == '__main__':
    unittest.main()