# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ryan/anaconda3/envs/wsl2/lib/python3.8/site-packages/pyEQL/tests/test_salt_matching.py
# Compiled at: 2020-04-22 00:40:31
# Size of source mod 2**32: 8691 bytes
__doc__ = '\npyEQL salt matching test suite\n==============================\n\nThis file contains tests for the salt-matching algorithm used by pyEQL in\nsalt_ion_match.py\n'
import pyEQL, unittest

class Test_empty_solution(unittest.TestCase, pyEQL.CustomAssertions):
    """Test_empty_solution"""

    def setUp(self):
        self.s1 = pyEQL.Solution()

    def test_salt_type(self):
        result = self.s1.get_salt()
        expected = pyEQL.salt_ion_match.Salt
        self.assertIsInstance(result, expected)

    def test_salt_formula(self):
        result = self.s1.get_salt().formula
        expected = 'HOH'
        self.assertEqual(result, expected)

    def test_salt_cation(self):
        result = self.s1.get_salt().cation
        expected = 'H+'
        self.assertEqual(result, expected)

    def test_salt_anion(self):
        result = self.s1.get_salt().anion
        expected = 'OH-'
        self.assertEqual(result, expected)

    def test_salt_nu_cation(self):
        result = self.s1.get_salt().nu_cation
        expected = 1
        self.assertEqual(result, expected)

    def test_salt_nu_anion(self):
        result = self.s1.get_salt().nu_anion
        expected = 1
        self.assertEqual(result, expected)


class Test_single_salt_mono(unittest.TestCase, pyEQL.CustomAssertions):
    """Test_single_salt_mono"""

    def setUp(self):
        self.s1 = pyEQL.Solution([['Na+', '2 mol/L'], ['Cl-', '2 mol/L']])

    def test_salt_type(self):
        result = self.s1.get_salt()
        expected = pyEQL.salt_ion_match.Salt
        self.assertIsInstance(result, expected)

    def test_salt_formula(self):
        result = self.s1.get_salt().formula
        expected = 'NaCl'
        self.assertEqual(result, expected)

    def test_salt_cation(self):
        result = self.s1.get_salt().cation
        expected = 'Na+'
        self.assertEqual(result, expected)

    def test_salt_anion(self):
        result = self.s1.get_salt().anion
        expected = 'Cl-'
        self.assertEqual(result, expected)

    def test_salt_nu_cation(self):
        result = self.s1.get_salt().nu_cation
        expected = 1
        self.assertEqual(result, expected)

    def test_salt_nu_anion(self):
        result = self.s1.get_salt().nu_anion
        expected = 1
        self.assertEqual(result, expected)


class Test_single_salt_di(unittest.TestCase, pyEQL.CustomAssertions):
    """Test_single_salt_di"""

    def setUp(self):
        self.s1 = pyEQL.Solution([['Na+', '4 mol/L'], ['SO4-2', '2 mol/L']])

    def test_salt_type(self):
        result = self.s1.get_salt()
        expected = pyEQL.salt_ion_match.Salt
        self.assertIsInstance(result, expected)

    def test_salt_formula(self):
        result = self.s1.get_salt().formula
        expected = 'Na2SO4'
        self.assertEqual(result, expected)

    def test_salt_cation(self):
        result = self.s1.get_salt().cation
        expected = 'Na+'
        self.assertEqual(result, expected)

    def test_salt_anion(self):
        result = self.s1.get_salt().anion
        expected = 'SO4-2'
        self.assertEqual(result, expected)

    def test_salt_nu_cation(self):
        result = self.s1.get_salt().nu_cation
        expected = 2
        self.assertEqual(result, expected)

    def test_salt_nu_anion(self):
        result = self.s1.get_salt().nu_anion
        expected = 1
        self.assertEqual(result, expected)


class Test_single_salt_di2(unittest.TestCase, pyEQL.CustomAssertions):
    """Test_single_salt_di2"""

    def setUp(self):
        self.s1 = pyEQL.Solution([['Fe+3', '1 mol/L'], ['Cl-', '3 mol/L']])

    def test_salt_type(self):
        result = self.s1.get_salt()
        expected = pyEQL.salt_ion_match.Salt
        self.assertIsInstance(result, expected)

    def test_salt_formula(self):
        result = self.s1.get_salt().formula
        expected = 'FeCl3'
        self.assertEqual(result, expected)

    def test_salt_cation(self):
        result = self.s1.get_salt().cation
        expected = 'Fe+3'
        self.assertEqual(result, expected)

    def test_salt_anion(self):
        result = self.s1.get_salt().anion
        expected = 'Cl-'
        self.assertEqual(result, expected)

    def test_salt_nu_cation(self):
        result = self.s1.get_salt().nu_cation
        expected = 1
        self.assertEqual(result, expected)

    def test_salt_nu_anion(self):
        result = self.s1.get_salt().nu_anion
        expected = 3
        self.assertEqual(result, expected)


class Test_single_ion(unittest.TestCase, pyEQL.CustomAssertions):
    """Test_single_ion"""

    def setUp(self):
        self.s1 = pyEQL.Solution([['Fe+3', '1 mol/L']])

    def test_salt_type(self):
        result = self.s1.get_salt()
        expected = pyEQL.salt_ion_match.Salt
        self.assertIsInstance(result, expected)

    def test_salt_formula(self):
        result = self.s1.get_salt().formula
        expected = 'Fe(OH)3'
        self.assertEqual(result, expected)

    def test_salt_cation(self):
        result = self.s1.get_salt().cation
        expected = 'Fe+3'
        self.assertEqual(result, expected)

    def test_salt_anion(self):
        result = self.s1.get_salt().anion
        expected = 'OH-'
        self.assertEqual(result, expected)

    def test_salt_nu_cation(self):
        result = self.s1.get_salt().nu_cation
        expected = 1
        self.assertEqual(result, expected)

    def test_salt_nu_anion(self):
        result = self.s1.get_salt().nu_anion
        expected = 3
        self.assertEqual(result, expected)


class Test_salt_asymmetric(unittest.TestCase, pyEQL.CustomAssertions):
    """Test_salt_asymmetric"""

    def setUp(self):
        self.s1 = pyEQL.Solution([['Na+', '1 mol/kg'], ['Cl-', '4 mol/kg']])

    def test_salt_type(self):
        result = self.s1.get_salt()
        expected = pyEQL.salt_ion_match.Salt
        self.assertIsInstance(result, expected)

    def test_salt_formula(self):
        result = self.s1.get_salt().formula
        expected = 'NaCl'
        self.assertEqual(result, expected)

    def test_salt_cation(self):
        result = self.s1.get_salt().cation
        expected = 'Na+'
        self.assertEqual(result, expected)

    def test_salt_anion(self):
        result = self.s1.get_salt().anion
        expected = 'Cl-'
        self.assertEqual(result, expected)

    def test_salt_nu_cation(self):
        result = self.s1.get_salt().nu_cation
        expected = 1
        self.assertEqual(result, expected)

    def test_salt_nu_anion(self):
        result = self.s1.get_salt().nu_anion
        expected = 1
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()