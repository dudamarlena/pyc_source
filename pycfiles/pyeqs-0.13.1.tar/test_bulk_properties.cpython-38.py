# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ryan/anaconda3/envs/wsl2/lib/python3.8/site-packages/pyEQL/tests/test_bulk_properties.py
# Compiled at: 2020-04-22 00:41:08
# Size of source mod 2**32: 2600 bytes
__doc__ = '\npyEQL test suite for bulk property calculations\n===============================================\n\nThis file contains tests for the bulk properties calculated by\nSolution class methods. Currently included methods are:\n\n- get_hardness()\n\n'
import pyEQL, unittest

class test_hardness(unittest.TestCase, pyEQL.CustomAssertions):
    """test_hardness"""

    def test_empty_solution(self):
        s1 = pyEQL.Solution()
        result = s1.get_hardness().magnitude
        expected = 0
        self.assertEqual(result, expected)

    def test_hardness_1(self):
        s1 = pyEQL.Solution([['Na+', '0.2 mol/L'], ['Cl-', '0.2 mol/L']])
        result = s1.get_hardness().magnitude
        expected = 0
        self.assertEqual(result, expected)

    def test_hardness_2(self):
        s1 = pyEQL.Solution([['Na+', '0.4 mol/L'], ['SO4-2', '0.2 mol/L']])
        result = s1.get_hardness().magnitude
        expected = 0
        self.assertEqual(result, expected)

    def test_hardness_3(self):
        s1 = pyEQL.Solution([['Fe+3', '0.1 mol/L'], ['Cl-', '0.3 mol/L']])
        result = s1.get_hardness().magnitude
        expected = 15013.5
        self.assertAlmostEqual(result, expected)

    def test_hardness_4(self):
        s1 = pyEQL.Solution([
         [
          'Na+', '0.1 mol/L'],
         [
          'K+', '0.1 mol/L'],
         [
          'Mg+2', '0.1 mol/L'],
         [
          'Ca+2', '0.1 mol/L'],
         [
          'Fe+3', '0.1 mol/L'],
         [
          'Cl-', '0.1 mol/L'],
         [
          'F-', '0.1 mol/L'],
         [
          'SO4-2', '0.2 mol/L'],
         [
          'PO4-3', '0.1 mol/L']])
        result = s1.get_hardness().magnitude
        expected = 35031.5
        self.assertAlmostEqual(result, expected)

    def test_hardness_5(self):
        s1 = pyEQL.Solution([['Fe+3', '0.1 mol/L'], ['Cl-', '0.3 mol/L']])
        result = str(s1.get_hardness().dimensionality)
        expected = '[mass] / [length] ** 3'
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()