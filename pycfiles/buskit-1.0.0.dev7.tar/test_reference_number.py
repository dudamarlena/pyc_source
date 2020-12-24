# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/business_tools/tests/test_reference_number.py
# Compiled at: 2011-07-05 05:12:41
import unittest
from business_tools.reference_number import ReferenceNumber

class TestReferenceNumber(unittest.TestCase):

    def test_repr(self):
        ref = ReferenceNumber('12344')
        self.assertEqual(ref.__repr__(), '<Reference number: 12344>')

    def test_str(self):
        ref = ReferenceNumber('12344')
        self.assertEqual(str(ref), '12344')

    def test_unicode(self):
        ref = ReferenceNumber('12344')
        self.assertEqual(unicode(ref), '12344')

    def test_human_format(self):
        values = ('123 45672', '12345672', '1 2345672')
        for val in values:
            ref = ReferenceNumber(val)
            self.assertEqual('123 45672', ref.human_format())

    def test_machine_format(self):
        values = ('123 45672', '12345672')
        for val in values:
            ref = ReferenceNumber(val)
            self.assertEqual('00000000000012345672', ref.machine_format())

    def test_validate(self):
        self.assertEqual(ReferenceNumber.validate('12344'), True)
        self.assertEqual(ReferenceNumber.validate('12341'), False)

    def test_calculate_checksum(self):
        chksum = ReferenceNumber.calculate_checksum('1234')
        self.assertEqual(chksum, '4')
        chksum = ReferenceNumber.calculate_checksum('1 23456 78912 34567')
        self.assertEqual(chksum, '9')
        self.assertRaises(ValueError, ReferenceNumber.calculate_checksum, None)
        self.assertRaises(ValueError, ReferenceNumber.calculate_checksum, '')
        self.assertRaises(ValueError, ReferenceNumber.calculate_checksum, 'HelloWorld')
        return