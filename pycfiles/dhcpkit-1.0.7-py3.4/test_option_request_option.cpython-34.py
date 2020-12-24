# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/tests/ipv6/options/test_option_request_option.py
# Compiled at: 2017-06-23 17:22:45
# Size of source mod 2**32: 2006 bytes
"""
Test the OptionRequestOption implementation
"""
import unittest
from dhcpkit.ipv6.options import OPTION_IA_NA, OPTION_IA_TA, OptionRequestOption
from dhcpkit.protocol_element import ElementDataRepresentation
from dhcpkit.tests.ipv6.options import test_option

class OptionRequestOptionTestCase(test_option.OptionTestCase):

    def setUp(self):
        self.option_bytes = bytes.fromhex('0006000400030004')
        self.option_object = OptionRequestOption(requested_options=[OPTION_IA_NA, OPTION_IA_TA])
        self.parse_option()

    def test_validate_requested_options(self):
        self.option.requested_options = 65535
        with self.assertRaisesRegex(ValueError, 'must be a list'):
            self.option.validate()
        self.option.requested_options = [OPTION_IA_NA, 0, OPTION_IA_TA]
        self.option.validate()
        self.option.requested_options = [
         OPTION_IA_NA, -1, OPTION_IA_TA]
        with self.assertRaisesRegex(ValueError, 'unsigned 16 bit integer'):
            self.option.validate()
        self.option.requested_options = [OPTION_IA_NA, 65535, OPTION_IA_TA]
        self.option.validate()
        self.option.requested_options = [
         OPTION_IA_NA, 65536, OPTION_IA_TA]
        with self.assertRaisesRegex(ValueError, 'unsigned 16 bit integer'):
            self.option.validate()

    def test_display_requested_options(self):
        elements = self.option.display_requested_options()
        self.assertIsInstance(elements, list)
        for element in elements:
            self.assertIsInstance(element, ElementDataRepresentation)

        representation = [str(element) for element in elements]
        self.assertRegex(representation[0], ' \\(3\\)$')
        self.assertRegex(representation[1], ' \\(4\\)$')

    def test_bad_option_length(self):
        with self.assertRaisesRegex(ValueError, 'Invalid option length'):
            OptionRequestOption.parse(bytes.fromhex('0006000300030004'))


if __name__ == '__main__':
    unittest.main()