# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ryan/anaconda3/envs/wsl2/lib/python3.8/site-packages/pyEQL/tests/test_dielectric.py
# Compiled at: 2020-04-22 00:39:48
# Size of source mod 2**32: 4373 bytes
__doc__ = '\npyEQL dielectric constant test suite\n============================================\n\nThis file contains tests that check the dielectric constant\ncomputations of pyEQL\n\n'
import pyEQL, unittest

class Test_dielectric(unittest.TestCase, pyEQL.CustomAssertions):
    """Test_dielectric"""

    def setUp(self):
        self.tol = 0.01

    def test_dielectric_constant(self):
        """
        4.4 mol/kg NaCl = 46
        """
        s1 = pyEQL.Solution([['Na+', '4.4 mol/kg'], ['Cl-', '4.4 mol/kg']])
        result = s1.get_dielectric_constant().magnitude
        expected = 46
        self.assertWithinExperimentalError(result, expected, self.tol)

    def test_dielectric_constant2(self):
        """
        2 mol/kg NaCl = 58
        """
        s1 = pyEQL.Solution([['Na+', '2 mol/kg'], ['Cl-', '2 mol/kg']])
        result = s1.get_dielectric_constant().magnitude
        expected = 58
        self.assertWithinExperimentalError(result, expected, self.tol)

    def test_dielectric_constant3(self):
        """
        1 mol/kg NaCl = 66
        """
        s1 = pyEQL.Solution([['Na+', '1 mol/kg'], ['Cl-', '1 mol/kg']])
        result = s1.get_dielectric_constant().magnitude
        expected = 66
        self.assertWithinExperimentalError(result, expected, self.tol)

    def test_dielectric_constant4(self):
        """
        1 mol/kg KBr = 67
        """
        s1 = pyEQL.Solution([['K+', '1 mol/kg'], ['Br-', '1 mol/kg']])
        result = s1.get_dielectric_constant().magnitude
        expected = 67
        self.assertWithinExperimentalError(result, expected, self.tol)

    def test_dielectric_constant5(self):
        """
        3.4 mol/kg KBr = 51
        """
        s1 = pyEQL.Solution([['K+', '3.4 mol/kg'], ['Br-', '3.4 mol/kg']])
        result = s1.get_dielectric_constant().magnitude
        expected = 51
        self.assertWithinExperimentalError(result, expected, self.tol)

    def test_dielectric_constant6(self):
        """
        5 mol/kg LiCl = 39
        """
        s1 = pyEQL.Solution([['Li+', '5 mol/kg'], ['Cl-', '5 mol/kg']])
        result = s1.get_dielectric_constant().magnitude
        expected = 39
        self.assertWithinExperimentalError(result, expected, self.tol)

    def test_dielectric_constant7(self):
        """
        1 mol/kg LiCl = 64
        """
        s1 = pyEQL.Solution([['Li+', '1 mol/kg'], ['Cl-', '1 mol/kg']])
        result = s1.get_dielectric_constant().magnitude
        expected = 64
        self.assertWithinExperimentalError(result, expected, self.tol)

    @unittest.expectedFailure
    def test_dielectric_constant8(self):
        """
        12 mol/kg LiCl = 24
        """
        s1 = pyEQL.Solution([['Li+', '12 mol/kg'], ['Cl-', '12 mol/kg']])
        result = s1.get_dielectric_constant().magnitude
        expected = 24
        self.assertWithinExperimentalError(result, expected, self.tol)

    def test_dielectric_constant9(self):
        """
        6.5 mol/kg RbCl = 43
        """
        s1 = pyEQL.Solution([['Rb+', '6.5 mol/kg'], ['Cl-', '6.5 mol/kg']])
        result = s1.get_dielectric_constant().magnitude
        expected = 43
        self.assertWithinExperimentalError(result, expected, self.tol)

    def test_dielectric_constant9(self):
        """
        2.1 mol/kg RbCl = 59
        """
        s1 = pyEQL.Solution([['Rb+', '2.1 mol/kg'], ['Cl-', '2.1 mol/kg']])
        result = s1.get_dielectric_constant().magnitude
        expected = 59
        self.assertWithinExperimentalError(result, expected, self.tol)

    def test_dielectric_constant9(self):
        """
        0.5 mol/kg RbCl = 73
        """
        s1 = pyEQL.Solution([['Rb+', '0.5 mol/kg'], ['Cl-', '0.5 mol/kg']])
        result = s1.get_dielectric_constant().magnitude
        expected = 73
        self.assertWithinExperimentalError(result, expected, self.tol)


if __name__ == '__main__':
    unittest.main()