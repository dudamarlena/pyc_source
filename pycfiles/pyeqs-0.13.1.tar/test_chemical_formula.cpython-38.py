# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ryan/anaconda3/envs/wsl2/lib/python3.8/site-packages/pyEQL/tests/test_chemical_formula.py
# Compiled at: 2020-04-22 00:41:02
# Size of source mod 2**32: 8284 bytes
__doc__ = '\nchemical_formula.py test suite\n==============================\n\nThis file contains tests for the chemical formula interpreter module of pyEQL.\n'
import pyEQL
from pyEQL import chemical_formula as cf
import unittest

class Test_check_formula(unittest.TestCase, pyEQL.CustomAssertions):
    """Test_check_formula"""

    def test_check_formula_1(self):
        input = 'Fe2(SO4)3'
        result = cf._check_formula(input)
        expected = ['Fe', '2', '(', 'S', 'O', '4', ')', '3']
        self.assertEqual(result, expected)

    def test_check_formula_2(self):
        input = 'C7H16'
        result = cf._check_formula(input)
        expected = ['C', '7', 'H', '16']
        self.assertEqual(result, expected)

    def test_check_formula_3(self):
        input = '(NH3)2SO4'
        result = cf._check_formula(input)
        expected = ['(', 'N', 'H', '3', ')', '2', 'S', 'O', '4']
        self.assertEqual(result, expected)

    def test_check_formula_4(self):
        input = 'MgCl2'
        result = cf._check_formula(input)
        expected = ['Mg', 'Cl', '2']
        self.assertEqual(result, expected)

    def test_check_formula_5(self):
        input = 'C100H202'
        result = cf._check_formula(input)
        expected = ['C', '100', 'H', '202']
        self.assertEqual(result, expected)

    def test_check_formula_6(self):
        input = 'Fe+++'
        result = cf._check_formula(input)
        expected = ['Fe', '+++']
        self.assertEqual(result, expected)

    def test_check_formula_7(self):
        input = 'V+4'
        result = cf._check_formula(input)
        expected = ['V', '+', '4']
        self.assertEqual(result, expected)


class Test_is_valid_formula(unittest.TestCase, pyEQL.CustomAssertions):
    """Test_is_valid_formula"""

    def test_is_valid_formula_1(self):
        input = '(NH3)2'
        result = cf.is_valid_formula(input)
        expected = True
        self.assertEqual(result, expected)

    def test_is_valid_formula_2(self):
        input = '3CO3-'
        result = cf.is_valid_formula(input)
        expected = False
        self.assertEqual(result, expected)

    def test_is_valid_formula_3(self):
        input = 'Na^+'
        result = cf.is_valid_formula(input)
        expected = False
        self.assertEqual(result, expected)

    def test_is_valid_formula_4(self):
        input = 'Na+-+'
        result = cf.is_valid_formula(input)
        expected = False
        self.assertEqual(result, expected)

    def test_is_valid_formula_5(self):
        input = 'HCO3-'
        result = cf.is_valid_formula(input)
        expected = True
        self.assertEqual(result, expected)

    def test_is_valid_formula_6(self):
        input = 'Fe++'
        result = cf.is_valid_formula(input)
        expected = True
        self.assertEqual(result, expected)

    def test_is_valid_formula_7(self):
        input = 'Mg+2'
        result = cf.is_valid_formula(input)
        expected = True
        self.assertEqual(result, expected)

    def test_is_valid_formula_8(self):
        input = 'V+5+'
        result = cf.is_valid_formula(input)
        expected = False
        self.assertEqual(result, expected)

    def test_is_valid_formula_9(self):
        input = 'NaOH'
        result = cf.is_valid_formula(input)
        expected = True
        self.assertEqual(result, expected)

    def test_is_valid_formula_9(self):
        input = 'naOH'
        result = cf.is_valid_formula(input)
        expected = False
        self.assertEqual(result, expected)

    def test_is_valid_formula_10(self):
        input = 'HzCl'
        result = cf.is_valid_formula(input)
        expected = False
        self.assertEqual(result, expected)

    def test_is_valid_formula_11(self):
        input = '(NH3)2(NO3)2'
        result = cf.is_valid_formula(input)
        expected = True
        self.assertEqual(result, expected)

    def test_is_valid_formula_12(self):
        input = 'Mg)(OH)2'
        result = cf.is_valid_formula(input)
        expected = False
        self.assertEqual(result, expected)

    def test_is_valid_formula_13(self):
        input = 'Na+('
        result = cf.is_valid_formula(input)
        expected = False
        self.assertEqual(result, expected)

    def test_is_valid_formula_14(self):
        input = '(3)Na+'
        result = cf.is_valid_formula(input)
        expected = False
        self.assertEqual(result, expected)

    def test_is_valid_formula_15(self):
        input = '()'
        result = cf.is_valid_formula(input)
        expected = False
        self.assertEqual(result, expected)

    def test_is_valid_formula_16(self):
        input = 'CH3C(O)CH3'
        result = cf.is_valid_formula(input)
        expected = True
        self.assertEqual(result, expected)

    def test_is_valid_formula_17(self):
        input = 'Mg(OH)2'
        result = cf.is_valid_formula(input)
        expected = True
        self.assertEqual(result, expected)

    def test_is_valid_formula_17(self):
        input = 'CH3(CH)2(CH)2'
        result = cf.is_valid_formula(input)
        expected = True
        self.assertEqual(result, expected)

    def test_is_valid_formula_18(self):
        input = ')Na+('
        result = cf.is_valid_formula(input)
        expected = False
        self.assertEqual(result, expected)


class Test_consolidate_formula(unittest.TestCase, pyEQL.CustomAssertions):
    """Test_consolidate_formula"""

    def test_is_valid_formula_1(self):
        input = 'Fe2(SO4)4'
        result = cf._consolidate_formula(input)
        expected = ['Fe', 2, 'S', 4, 'O', 16]
        self.assertEqual(result, expected)

    def test_is_valid_formula_2(self):
        input = '(NH4)3PO4'
        result = cf._consolidate_formula(input)
        expected = ['N', 3, 'H', 12, 'P', 1, 'O', 4]
        self.assertEqual(result, expected)

    def test_is_valid_formula_3(self):
        input = 'CH3(CH2)6CH3'
        result = cf._consolidate_formula(input)
        expected = ['C', 8, 'H', 18]
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()