# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zjshao/Documents/repos/VASPy/tests/cif_test.py
# Compiled at: 2017-06-01 02:10:36
# Size of source mod 2**32: 492 bytes
"""
CifFile单元测试
"""
import unittest
from vaspy.atomco import CifFile
from tests import abs_path

class CifFileTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = True

    def test_construction(self):
        filename = abs_path + '/testdata/ceo2-111.cif'
        cif = CifFile(filename)


if '__main__' == __name__:
    suite = unittest.TestLoader().loadTestsFromTestCase(CifFileTest)
    unittest.TextTestRunner(verbosity=2).run(suite)