# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/josefernandeznavarro/Projects/st/st_pipeline/tests/adaptors_test.py
# Compiled at: 2016-11-02 13:30:40
# Size of source mod 2**32: 1411 bytes
""" 
Unit-test the package adaptors
"""
import unittest
from stpipeline.common.adaptors import removeAdaptor

class TestAdaptors(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    @classmethod
    def tearDownClass(self):
        pass

    def test_removeAdaptor(self):
        """
        Test that the function removeAdaptor removes correctly
        adaptors when using different parameters.
        It also tests that it fails when it has to
        """
        fake_qual = 'AAAAAAAAAAAAAAAAAAAA'
        seq_adaptor_beginning = 'TTTTTAAAAAAAAAAAAAAA'
        seq_adaptor_middle = 'AAAAAAAAAATTTTTAAAAA'
        seq_adaptor_end = 'AAAAAAAAAAAAAAATTTTT'
        adaptor = 'TTTTT'
        result_seq, result_qual = removeAdaptor(seq_adaptor_beginning, fake_qual, adaptor, missmatches=0)
        self.assertTrue(len(result_seq) == 0 and len(result_qual) == 0)
        result_seq, result_qual = removeAdaptor(seq_adaptor_middle, fake_qual, adaptor, missmatches=0)
        self.assertTrue(len(result_seq) == 10 and len(result_qual) == 10)
        result_seq, result_qual = removeAdaptor(seq_adaptor_end, fake_qual, adaptor, missmatches=0)
        self.assertTrue(len(result_seq) == 15 and len(result_qual) == 15)


if __name__ == '__main__':
    unittest.main()