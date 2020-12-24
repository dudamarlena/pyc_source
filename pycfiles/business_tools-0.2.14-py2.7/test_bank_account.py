# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/business_tools/tests/test_bank_account.py
# Compiled at: 2011-07-05 05:12:41
"""Unit tests for bank_account.py"""
import unittest
from business_tools.bank_account import BBAN, IBAN, bban_to_iban, iban_to_bban, get_swift_code

class TestBBAN(unittest.TestCase):

    def test_machine_format(self):
        """
        Test that machine_format returns machine parseable output.
        """
        v = BBAN('123456-1234565')
        self.assertEqual(v.machine_format(), '12345601234565')

    def test_human_format(self):
        """
        Test that human_format returns human readable output.
        """
        v = BBAN('123456-1234565')
        self.assertEqual(v.human_format(), '123456-1234565')

    def test_bank_name(self):
        """
        Test that bank_name can parse bank name from the account number.
        """
        v = BBAN('123456-1234565')
        self.assertEqual(v.bank_name(), 'Nordea')

    def test_str(self):
        """
        Test string conversion.
        """
        self.assertEqual(str(BBAN('123456-1234565')), '123456-1234565')

    def test_is_valid(self):
        """
        Test validation.
        """
        self.failUnless(BBAN.is_valid('123456-1234565'))
        self.failIf(BBAN.is_valid('123456-1234567'))


class TestIBAN(unittest.TestCase):

    def test_validate(self):
        """
        Test validation.
        """
        v = IBAN('FI8912345601234565')

    def test_str(self):
        """
        Test string conversion.
        """
        self.assertEqual(str(IBAN('FI8912345601234565')), 'FI8912345601234565')

    def test_bank_name(self):
        """
        Test that bank_name can parse bank name from the IBAN account number.
        """
        v = IBAN('FI8912345601234565')
        self.assertEqual(v.bank_name(), 'Nordea')
        v = IBAN('FI1840551010234569')
        self.assertEqual(v.bank_name(), 'Aktia')


class TestHelpers(unittest.TestCase):

    def test_bban_to_iban(self):
        """
        Test bban->iban conversion.
        """
        for v in (('123456-1234565', 'FI8912345601234565'),
         ('159030-776', 'FI3715903000000776')):
            bban = BBAN(v[0])
            iban = bban_to_iban(bban)
            self.assertEqual(iban, v[1])

    def test_iban_to_bban(self):
        """
        Test bban->iban conversion.
        """
        for v in (('123456-1234565', 'FI8912345601234565'),
         ('159030-776', 'FI3715903000000776')):
            iban = IBAN(v[1])
            bban = iban_to_bban(iban)
            self.assertEqual(bban, v[0])

    def test_get_swift_code(self):
        """
        Test that swift code is found with a bank name.
        """
        values = [
         ('Nordea', 'NDEAFIHH'),
         ('nordea', 'NDEAFIHH'),
         ('nandelsbanken', 'HANDFIHH'),
         ('seb', 'ESSEFIHX'),
         ('danske bank', 'DABAFIHX'),
         ('tapiola', 'TAPIFI22'),
         ('dnb nor', 'DNBAFIHX'),
         ('swedbank', 'SWEDFIHH'),
         ('s-pankki', 'SBANFIHH'),
         ('säästöpankki', 'HELSFIHH'),
         ('pop', 'HELSFIHH'),
         ('osuuspankki', 'OKOYFIHH'),
         ('ålandsbanken', 'AABAFI22'),
         ('sampo', 'DABAFIHH'),
         ('aktia', 'HELSFIHH')]
        for v in values:
            swift = get_swift_code(v[0])
            self.assertEqual(swift, v[1])