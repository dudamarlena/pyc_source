# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ryan/anaconda3/envs/wsl2/lib/python3.8/site-packages/pyEQL/tests/test_debye_length.py
# Compiled at: 2020-04-22 00:40:50
# Size of source mod 2**32: 1947 bytes
__doc__ = '\npyEQL debye length test suite\n============================================\n\nThis file contains tests that check the Debye Length\ncomputations of pyEQL\n\n'
import pyEQL, unittest

class Test_debye_length(unittest.TestCase, pyEQL.CustomAssertions):
    """Test_debye_length"""

    def setUp(self):
        self.tol = 0.03

    def test_debye_length_1(self):
        """

        """
        s1 = pyEQL.Solution([['Na+', '0.1 mmol/L'], ['Cl-', '0.1 mmol/L']])
        result = s1.get_debye_length().magnitude
        expected = 31
        self.assertWithinExperimentalError(result, expected, self.tol)

    def test_debye_length_2(self):
        """

        """
        s1 = pyEQL.Solution([['Na+', '10 mmol/L'], ['Cl-', '10 mmol/L']])
        result = s1.get_debye_length().magnitude
        expected = 3.1
        self.assertWithinExperimentalError(result, expected, self.tol)

    def test_debye_length_3(self):
        """

        """
        s1 = pyEQL.Solution([['Na+', '0.2 mmol/L'], ['SO4-2', '0.1 mmol/L']])
        result = s1.get_debye_length().magnitude
        expected = 18
        self.assertWithinExperimentalError(result, expected, self.tol)

    def test_debye_length_4(self):
        """

        """
        s1 = pyEQL.Solution([['Na+', '20 mmol/L'], ['SO4-2', '10 mmol/L']])
        result = s1.get_debye_length().magnitude
        expected = 1.8
        self.assertWithinExperimentalError(result, expected, self.tol)


if __name__ == '__main__':
    unittest.main()