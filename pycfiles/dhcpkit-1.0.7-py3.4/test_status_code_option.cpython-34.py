# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/tests/ipv6/options/test_status_code_option.py
# Compiled at: 2017-06-24 11:14:24
# Size of source mod 2**32: 1193 bytes
"""
Test the StatusCodeOption implementation
"""
import unittest
from dhcpkit.ipv6.options import STATUS_NOT_ON_LINK, StatusCodeOption
from dhcpkit.tests.ipv6.options import test_option

class StatusCodeOptionTestCase(test_option.OptionTestCase):

    def setUp(self):
        self.option_bytes = bytes.fromhex('000d001d00044fc3b920c3aa7465732d766f7573206d6f6e206d61c3ae7472653f')
        self.option_object = StatusCodeOption(STATUS_NOT_ON_LINK, 'Où êtes-vous mon maître?')
        self.parse_option()

    def test_status_code(self):
        self.check_unsigned_integer_property('status_code', size=16)

    def test_status_message(self):
        self.option.status_message = b'This is not a string'
        with self.assertRaisesRegex(ValueError, 'must be a string'):
            self.option.validate()

    def test_display(self):
        output = str(self.option_object)
        self.assertEqual(output, "StatusCodeOption(\n  status_code=NotOnLink (4),\n  status_message='Où êtes-vous mon maître?',\n)")


if __name__ == '__main__':
    unittest.main()