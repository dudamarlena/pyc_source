# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mounts/isilon/data/eahome/q804348/ea_code/STAR-SEQR/starseqr_utils/tests/test_diversity.py
# Compiled at: 2017-12-07 17:16:01
import unittest, os, sys
sys.path.insert(0, '../')
import starseqr_utils as su
path = os.path.dirname(__file__)
if path != '':
    os.chdir(path)

class DiversityTestCase(unittest.TestCase):
    """Tests cross homology"""

    def test_overhang_v1(self):
        """test homology paired.fastq TUBA1B--TUBA1A test case"""
        res1 = su.overhang_diversity.get_diversity('chr12:49521770:-:chr12:49578857:-:6:0')
        assert res1 == (2, 0, 0)

    def test_overhang_v2(self):
        """test diversity with no reads in fastq test case"""
        res1 = su.overhang_diversity.get_diversity('chr2:131389025:+:chr2:131996848:+:0:4')
        assert res1 == (0, 0, 0)

    def test_overhang_v3(self):
        """test homology with lots of reads in fastq test case"""
        res1 = su.overhang_diversity.get_diversity('chr1:45268528:+:chr4:107152937:-:0:2')
        assert res1 == (6, 6, 5)


if __name__ == '__main__':
    unittest.main()