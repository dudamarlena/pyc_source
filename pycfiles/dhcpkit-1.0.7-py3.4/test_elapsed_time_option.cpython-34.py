# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/tests/ipv6/options/test_elapsed_time_option.py
# Compiled at: 2017-06-23 17:22:45
# Size of source mod 2**32: 911 bytes
"""
Test the ElapsedTimeOption implementation
"""
import unittest
from dhcpkit.ipv6.options import ElapsedTimeOption
from dhcpkit.tests.ipv6.options import test_option

class ElapsedTimeOptionTestCase(test_option.OptionTestCase):

    def setUp(self):
        self.option_bytes = bytes.fromhex('0008000204d2')
        self.option_object = ElapsedTimeOption(elapsed_time=1234)
        self.parse_option()

    def test_validate_elapsed_time(self):
        self.check_unsigned_integer_property('elapsed_time', size=16)

    def test_bad_option_length(self):
        with self.assertRaisesRegex(ValueError, 'must have length 2'):
            ElapsedTimeOption.parse(bytes.fromhex('000800000000ffff'))
        with self.assertRaisesRegex(ValueError, 'must have length 2'):
            ElapsedTimeOption.parse(bytes.fromhex('000800030000ffff'))


if __name__ == '__main__':
    unittest.main()