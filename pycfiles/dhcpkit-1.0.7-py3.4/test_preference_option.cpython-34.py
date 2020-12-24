# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/tests/ipv6/options/test_preference_option.py
# Compiled at: 2017-06-23 17:22:45
# Size of source mod 2**32: 887 bytes
"""
Test the PreferenceOption implementation
"""
import unittest
from dhcpkit.ipv6.options import PreferenceOption
from dhcpkit.tests.ipv6.options import test_option

class PreferenceOptionTestCase(test_option.OptionTestCase):

    def setUp(self):
        self.option_bytes = bytes.fromhex('00070001ff')
        self.option_object = PreferenceOption(preference=255)
        self.parse_option()

    def test_validate_preference(self):
        self.check_unsigned_integer_property('preference', size=8)

    def test_bad_option_length(self):
        with self.assertRaisesRegex(ValueError, 'must have length 1'):
            PreferenceOption.parse(bytes.fromhex('00070000ffff'))
        with self.assertRaisesRegex(ValueError, 'must have length 1'):
            PreferenceOption.parse(bytes.fromhex('00070002ffff'))


if __name__ == '__main__':
    unittest.main()