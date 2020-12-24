# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/tests/ipv6/extensions/test_pd_exclude.py
# Compiled at: 2017-06-23 17:22:45
# Size of source mod 2**32: 960 bytes
"""
Test the PDExcludeOption implementation
"""
import unittest
from dhcpkit.ipv6.extensions.pd_exclude import PDExcludeOption
from dhcpkit.tests.ipv6.options import test_option

class PDExcludeOptionTestCase(test_option.OptionTestCase):

    def setUp(self):
        self.option_bytes = bytes.fromhex('004300024078')
        self.option_object = PDExcludeOption(64, bytes.fromhex('78'))
        self.parse_option()

    def test_prefix_length(self):
        self.check_integer_property_range('prefix_length', 1, 128)

    def test_subnet_id(self):
        self.option.subnet_id = 'Not bytes'
        with self.assertRaisesRegex(ValueError, 'sequence of .* bytes'):
            self.option.validate()

    def test_bad_option_length(self):
        with self.assertRaisesRegex(ValueError, 'longer than the available buffer'):
            PDExcludeOption.parse(bytes.fromhex('004300034078'))


if __name__ == '__main__':
    unittest.main()