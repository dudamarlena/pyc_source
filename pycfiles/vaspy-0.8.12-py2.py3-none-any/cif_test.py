# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zjshao/Documents/repos/VASPy/tests/cif_test.py
# Compiled at: 2017-03-18 23:50:22
"""
CifFile单元测试
"""
import unittest
from vaspy.atomco import CifFile
from tests import path

class CifFileTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = True

    def test_construction(self):
        filename = path + '/ceo2-111.cif'
        cif = CifFile(filename)


if '__main__' == __name__:
    suite = unittest.TestLoader().loadTestsFromTestCase(CifFileTest)
    unittest.TextTestRunner(verbosity=2).run(suite)