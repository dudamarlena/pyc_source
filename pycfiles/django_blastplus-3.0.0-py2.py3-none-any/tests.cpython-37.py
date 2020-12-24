# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/michal/workspace/code/django-blastplus/blastplus/tests/tests.py
# Compiled at: 2019-10-26 08:24:44
# Size of source mod 2**32: 2383 bytes
import os, tempfile, unittest
from Bio.Blast import NCBIXML
from django.test import TestCase
from blastplus import utils
from blastplus.features import record
from blastplus.settings import SAMPLE_DIR

class UtilsTestCase(TestCase):

    def setUp(self):
        self.fastfile = tempfile.NamedTemporaryFile(mode='w+', delete=False)
        self.fastfile.write('>seq1\n')
        self.fastfile.write('AAACCCGGG\n')
        self.fastfile.close()
        self.blast_out = os.path.join(SAMPLE_DIR, 'blast.xml')

    def tearDown(self):
        os.unlink(self.fastfile.name)

    def test_get_sample_data(self):
        with open(self.fastfile.name) as (f):
            self.assertEquals(utils.get_sample_data(self.fastfile.name), f.read())

    def test_blast_records_parse(self):
        brs = list(NCBIXML.parse(open(self.blast_out)))
        self.assertTrue(len(brs) == 1)

    def test_blast_records_to_object(self):
        brs = utils.blast_records_to_object(list(NCBIXML.parse(open(self.blast_out))))
        self.assertTrue(len(brs) == 1)


class FeatureRecordTestCase(TestCase):

    def setUp(self):
        self.hsp = (record.Hsp)(**dict(sbjct_end=203, sbjct='TTTGGAGCCTGAGCAGGA', bits=35.5503, frame=(1,
                                                                                                       -1), query_end=19,
          score=38.0,
          gaps=0,
          expect=0.0122843,
          str='Score 38 (35 bits), expectation 1.2e-02',
          positives=19,
          sbjct_start=221,
          query='TTTGGAGCCTGAGCAGGA',
          align_length=19,
          num_alignments=None,
          identities=19,
          query_start=1,
          strand=(None, None),
          match='||||||||||||||||||'))
        self.limit_length = 9
        self.alignment = (record.Alignment)(**dict(hit_def='hit_def', title='title', length=(self.hsp.align_length)))
        self.alignment.hsp_list.append(self.hsp)

    def tearDown(self):
        del self.hsp
        del self.alignment

    def test_hsp(self):
        self.assertIsInstance(self.hsp, record.Hsp)
        self.assertTrue(self.hsp.chop_sequence('AACC', 2), ['AA', 'CC'])
        self.assertTrue(self.hsp.chop_query(), ['TTTGGAGCC', 'TGAGCAGGA'])

    def test_alignment(self):
        self.assertIsInstance(self.alignment, record.Alignment)
        self.assertEqual(self.alignment.best_evalue(), self.hsp.expect)
        self.assertEqual(self.alignment.best_identities(), 100.0)


if __name__ == '__main__':
    unittest.main()