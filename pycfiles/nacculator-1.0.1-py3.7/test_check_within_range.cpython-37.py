# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/tests/test_check_within_range.py
# Compiled at: 2019-12-05 17:01:18
# Size of source mod 2**32: 2770 bytes
import unittest, nacc.uds3

class TestWithinRange(unittest.TestCase):
    __doc__ = '\n    These tests are designed to run ivp data fields (generated below\n    the tests here) through the Field class in the uds3.__init__ file.\n    It is checking to ensure that the Field class catches errors in the\n    "allowable_values" and "inclusive_range" variables.\n    '

    def test_for_Char_fields_skipping_range_check(self):
        """
        Have it make sure that only Num fields are being checked for range
        """
        racex = nacc.uds3.Field(name='RACEX', typename='Char', position=(136, 195), length=60, inclusive_range=None, allowable_values=[], blanks=[])
        racex.value = 'race'
        expected = 'race'
        self.assertEqual(racex.val, expected)

    def test_for_allowed_values_within_range(self):
        """
        Ensure that the 'if self.allowable_values' statement returns expected
        errors
        """
        reason = nacc.uds3.Field(name='REASON', typename='Num', position=(45, 45), length=1, inclusive_range=(1,
                                                                                                              4), allowable_values=['4', '2', '1', '9'], blanks=[])
        with self.assertRaises(ValueError):
            reason.value = '10'

    def test_for_allowed_values_out_of_range(self):
        """
        Ensure that the 'if self.allowable_values' statement does not return
        errors if a value is out of the inclusive_range but within
        allowable_values, such as a field that expects 1-3, but also allows 9
        (like 9 = Unknown)
        """
        reason = nacc.uds3.Field(name='REASON', typename='Num', position=(45, 45), length=1, inclusive_range=(1,
                                                                                                              4), allowable_values=['4', '2', '1', '9'], blanks=[])
        reason.value = '9'
        expected = '9'
        self.assertEqual(reason.val, expected)

    def test_for_within_range_without_allowable_values(self):
        """
        Ensure that the 'if no self.allowable_values' statement returns
        out-of-range errors when there is an inclusive_range but no specific
        allowable_values
        """
        kids = nacc.uds3.Field(name='KIDS', typename='Num', position=(956, 957), length=2, inclusive_range=(0,
                                                                                                            15), allowable_values=[], blanks=[])
        with self.assertRaises(ValueError):
            kids.value = '16'


if __name__ == '__main__':
    unittest.main()