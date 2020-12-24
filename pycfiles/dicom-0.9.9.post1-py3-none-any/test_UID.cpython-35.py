# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\git\pydicom-clean\source\build\lib\dicom\test\test_UID.py
# Compiled at: 2017-01-26 21:08:30
# Size of source mod 2**32: 3415 bytes
"""Test suite for UID.py"""
import unittest
from dicom.UID import UID, generate_uid, pydicom_root_UID, InvalidUID

class UIDtests(unittest.TestCase):

    def testKnownUID(self):
        """UID: Known UID properties accessed....................."""
        msg = "UID: expected '{1:s}', got '{2:s}' for UID {0:s}"
        uid = UID('1.2.840.10008.1.2')
        expected = 'Implicit VR Little Endian'
        got = uid.name
        self.assertEqual(got, expected, msg.format('name', expected, got))
        expected = 'Transfer Syntax'
        got = uid.type
        self.assertEqual(got, expected, msg.format('type', expected, got))
        expected = 'Default Transfer Syntax for DICOM'
        got = uid.info
        self.assertEqual(got, expected, msg.format('info', expected, got))
        expected = False
        got = uid.is_retired
        self.assertEqual(got, expected, msg.format('is_retired', str(expected), str(got)))

    def testComparison(self):
        """UID: can compare by number or by name.................."""
        uid = UID('1.2.840.10008.1.2')
        self.assertEqual(uid, 'Implicit VR Little Endian', 'UID equality failed on name')
        self.assertEqual(uid, '1.2.840.10008.1.2', 'UID equality failed on number string')

    def testCompareNumber(self):
        """UID: comparing against a number give False............."""
        uid = UID('1.2.3')
        self.assertNotEqual(uid, 3, 'Comparison to a number returned True')

    def testCompareNotEqualByName(self):
        """UID: comparing not equal by name......................."""
        ct_image_storage = UID('1.2.840.10008.5.1.4.1.1.2')
        msg = 'UID not equal comparison by name was not correct'
        self.assertFalse(ct_image_storage != 'CT Image Storage', msg)

    def testCompareNone(self):
        """UID: comparing against None give False................."""
        uid = UID('1.2.3')
        self.assertNotEqual(uid, None, 'Comparison to a number returned True')

    def testTransferSyntaxes(self):
        pass

    def testGenerateUID(self):
        """
        Test UID generator
        """
        uid = generate_uid()
        self.assertEqual(uid[:26], pydicom_root_UID)
        uid = generate_uid(None)
        self.assertEqual(uid[:5], '2.25.')
        invalid_prefix = '1.2.33333333333333333333333333333333333333333333333333333333333.333.'
        self.assertRaises(InvalidUID, lambda : generate_uid(prefix=invalid_prefix, truncate=True))
        prefix = '1.2.3.444444'
        uid = generate_uid(prefix=prefix, truncate=True)
        self.assertEqual(uid[:12], prefix)


if __name__ == '__main__':
    unittest.main()