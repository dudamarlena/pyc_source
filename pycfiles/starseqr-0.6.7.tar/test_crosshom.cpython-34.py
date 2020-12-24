# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mounts/isilon/data/eahome/q804348/ea_code/STAR-SEQR/starseqr_utils/tests/test_crosshom.py
# Compiled at: 2017-12-07 17:16:00
# Size of source mod 2**32: 1944 bytes
import unittest, os, sys
sys.path.insert(0, '../../')
import starseqr_utils as su
path = os.path.dirname(__file__)
if path != '':
    os.chdir(path)

class CrossHomologyTestCase(unittest.TestCase):
    __doc__ = 'Tests cross homology'

    def test_crosshom_v1(self):
        """test homology paired.fastq TUBA1B--TUBA1A test case"""
        res1 = su.cross_homology.get_cross_homology('chr12:49521770:-:chr12:49578857:-:6:0', 'test_data/chim_transcripts/')
        assert res1 == (0.778, 0.5)

    def test_crosshom_v2(self):
        """test homology paired.fastq no reads in fastq test case"""
        res1 = su.cross_homology.get_cross_homology('chr2:131389025:+:chr2:131996848:+:0:4', 'test_data/chim_transcripts/')
        assert res1 == (0, 0)

    def test_crosshom_v3(self):
        """test homology TRIM46--TMEM161A--a known FP with borderline homology """
        res1 = su.cross_homology.get_cross_homology('1:155152411:+:19:19243318:-:1:0', 'test_data/chim_transcripts/')
        assert res1 == (0.0, 0.667)

    def test_crosshom_v4(self):
        """test homology a known TP with borderline homology """
        res1 = su.cross_homology.get_cross_homology('5:149206449:+:1:156848913:+:1:0', 'test_data/chim_transcripts/')
        assert res1 == (0.0, 0.071)

    def test_crosshom_v5(self):
        """ test with SMURF1--SMURF2 FP fusion"""
        res1 = su.cross_homology.get_cross_homology('7:98645306:-:17:62557722:-:2:1', 'test_data/chim_transcripts/')
        assert res1 == (0.0, 1.0)

    def test_crosshom_v6(self):
        """ known TP with small overhang. 1 Read """
        res1 = su.cross_homology.get_cross_homology('chr6:26936302:+:chr15:74623003:+:2:0', 'test_data/chim_transcripts/')
        assert res1 == (0.0, 0.5)


if __name__ == '__main__':
    unittest.main()