# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/staramr/tests/unit/blast/results/pointfinder/test_PointfinderHitHSP.py
# Compiled at: 2019-12-17 17:26:02
# Size of source mod 2**32: 990 bytes
import unittest, pandas as pd
import staramr.blast.results.pointfinder.PointfinderHitHSP as PointfinderHitHSP
import staramr.exceptions.InvalidPositionException as InvalidPositionException

class PointfinderHitHSPTest(unittest.TestCase):

    def testBuildPointfinderHitHSPSuccess(self):
        blast_record = pd.Series({'sstart':1,  'send':10,  'qstart':1,  'qend':10,  'sstrand':'plus'})
        PointfinderHitHSP(file=None, blast_record=blast_record)

    def testBuildPointfinderHitHSPFailInvalidSubjectCoords(self):
        blast_record = pd.Series({'sstart':10,  'send':1,  'qstart':1,  'qend':10,  'sstrand':'plus'})
        self.assertRaises(InvalidPositionException, PointfinderHitHSP, None, blast_record)

    def testBuildPointfinderHitHSPInvalidQueryCoords(self):
        blast_record = pd.Series({'sstart':1,  'send':10,  'qstart':10,  'qend':1,  'sstrand':'plus'})
        self.assertRaises(InvalidPositionException, PointfinderHitHSP, None, blast_record)