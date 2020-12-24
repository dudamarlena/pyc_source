# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\git\pydicom-clean\source\build\lib\dicom\test\test_valuerep.py
# Compiled at: 2017-01-26 21:08:30
# Size of source mod 2**32: 5009 bytes
"""Test suite for valuerep.py"""
import unittest
from dicom import in_py3
import dicom.config
if in_py3:
    from dicom.valuerep import PersonName3 as PersonNameUnicode
    PersonName = PersonNameUnicode
else:
    from dicom.valuerep import PersonName, PersonNameUnicode
default_encoding = 'iso8859'

class DecimalStringtests(unittest.TestCase):
    __doc__ = 'Unit tests unique to the use of DS class derived from python Decimal'

    def setUp(self):
        dicom.config.DS_decimal(True)

    def tearDown(self):
        dicom.config.DS_decimal(False)

    def testValidDecimalStrings(self):
        valid_str = '-9.81338674e-006'
        ds = dicom.valuerep.DS(valid_str)
        L = len(str(ds))
        self.assertTrue(L <= 16, 'DS: expected a string of length 16 but got %d' % (L,))
        long_str = '-0.000000981338674'
        ds = dicom.valuerep.DS(long_str)
        L = len(str(ds))
        self.assertTrue(L <= 16, 'DS: expected a string of length 16 but got %d' % (L,))

    def testInvalidDecimalStrings(self):
        invalid_string = '-9.813386743e-006'
        self.assertRaises(OverflowError, dicom.valuerep.DS, invalid_string)


class PersonNametests(unittest.TestCase):

    def testLastFirst(self):
        """PN: Simple Family-name^Given-name works..............................."""
        pn = PersonName('Family^Given')
        expected = 'Family'
        got = pn.family_name
        self.assertEqual(got, expected, "PN: expected '%s', got '%s' for family name" % (expected, got))
        expected = 'Given'
        got = pn.given_name
        self.assertEqual(got, expected, "PN: expected '%s', got '%s' for given name" % (expected, got))
        expected = ''
        got = pn.name_suffix
        self.assertEqual(got, expected, "PN: expected '%s', got '%s' for name_suffix" % (expected, got))
        expected = ''
        got = pn.phonetic
        self.assertEqual(got, expected, "PN: expected '%s', got '%s' for phonetic component" % (expected, got))

    def testThreeComponent(self):
        """PN: 3component (single-byte, ideographic, phonetic characters) works.."""
        pn = PersonName('Hong^Gildong=\x1b$)Cûó^\x1b$)CÑÎÔ×=\x1b$)CÈ«^\x1b$)C±æµ¿')
        expected = ('Hong', 'Gildong')
        got = (pn.family_name, pn.given_name)
        self.assertEqual(got, expected, "PN: Expected single_byte name '%s', got '%s'" % (expected, got))

    def testFormatting(self):
        """PN: Formatting works.................................................."""
        pn = PersonName('Family^Given')
        expected = 'Family, Given'
        got = pn.family_comma_given()
        self.assertEqual(got, expected, "PN: expected '%s', got '%s' for formatted Family, Given" % (expected, got))

    def testUnicodeKr(self):
        """PN: 3component in unicode works (Korean).............................."""
        pn = PersonNameUnicode('Hong^Gildong=\x1b$)Cûó^\x1b$)CÑÎÔ×=\x1b$)CÈ«^\x1b$)C±æµ¿', [
         default_encoding, 'euc_kr'])
        expected = ('Hong', 'Gildong')
        got = (pn.family_name, pn.given_name)
        self.assertEqual(got, expected, "PN: Expected single_byte name '{0!s}', got '{1!s}'".format(expected, got))

    def testUnicodeJp(self):
        """PN: 3component in unicode works (Japanese)............................"""
        pn = PersonNameUnicode('Yamada^Tarou=\x1b$B;3ED\x1b(B^\x1b$BB@O:\x1b(B=\x1b$B$d$^$@\x1b(B^\x1b$B$?$m$&\x1b(B', [
         default_encoding, 'iso2022_jp'])
        expected = ('Yamada', 'Tarou')
        got = (pn.family_name, pn.given_name)
        self.assertEqual(got, expected, "PN: Expected single_byte name '{0!s}', got '{1!s}'".format(expected, got))

    def testNotEqual(self):
        """PN3: Not equal works correctly (issue 121)..........................."""
        from dicom.valuerep import PersonName3
        pn = PersonName3('John^Doe')
        msg = 'PersonName3 not equal comparison did not work correctly'
        self.assertFalse(pn != 'John^Doe', msg)


if __name__ == '__main__':
    unittest.main()