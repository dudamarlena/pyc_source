# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zjshao/Documents/repos/VASPy/tests/ani_test.py
# Compiled at: 2017-06-01 01:58:46
# Size of source mod 2**32: 877 bytes
"""
AniFile单元测试
"""
import unittest
from vaspy.iter import AniFile
from vaspy.atomco import XyzFile
from tests import abs_path

class AniFileTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = True
        self.filename = abs_path + '/testdata/OUT.ANI'

    def test_construction(self):
        ani = AniFile(self.filename)

    def test_iterable(self):
        """ Make sure the ani object is iterable."""
        ani = AniFile(self.filename)
        generator = iter(ani)
        xyz = next(generator)
        self.assertTrue(isinstance(xyz, XyzFile))
        self.assertListEqual(xyz.atom_types, ['Pt', 'C', 'O'])
        self.assertListEqual(xyz.atom_numbers, [40, 1, 1])


if '__main__' == __name__:
    suite = unittest.TestLoader().loadTestsFromTestCase(AniFileTest)
    unittest.TextTestRunner(verbosity=2).run(suite)