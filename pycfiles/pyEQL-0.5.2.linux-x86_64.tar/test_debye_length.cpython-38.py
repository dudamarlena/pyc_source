# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ryan/anaconda3/envs/wsl2/lib/python3.8/site-packages/pyEQL/tests/test_debye_length.py
# Compiled at: 2020-04-22 00:40:50
# Size of source mod 2**32: 1947 bytes
"""
pyEQL debye length test suite
============================================

This file contains tests that check the Debye Length
computations of pyEQL

"""
import pyEQL, unittest

class Test_debye_length(unittest.TestCase, pyEQL.CustomAssertions):
    __doc__ = '\n    test the Debye Length calculations of various solutions\n    ------------------------------------------------\n\n    Reference: [1] M. Hu, B. Mi, Enabling graphene oxide nanosheets as water separation membranes,\n    Environ. Sci. Technol. 47 (2013) 3715–3723. doi:10.1021/es400571g.\n\n    0.1 mM NaCl: 31nm\n    10 mM NaCl: 3.1 nm\n    0.1 mM Na2SO4: 18nm\n    10 mM Na2SO4: 1.8nm\n\n    '

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