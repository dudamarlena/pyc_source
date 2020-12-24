# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/tests/ipv6/extensions/leasequery/test_clt_time_option.py
# Compiled at: 2017-06-23 17:22:45
# Size of source mod 2**32: 1604 bytes
"""
Test the CLTTimeOption implementation
"""
import unittest
from dhcpkit.ipv6.extensions.leasequery import CLTTimeOption
from dhcpkit.tests.ipv6.options import test_option

class CLTTimeOptionTestCase(test_option.OptionTestCase):

    def setUp(self):
        self.option_bytes = bytes.fromhex('002e000400000384')
        self.option_object = CLTTimeOption(clt_time=900)
        self.parse_option()

    def test_validate_clt_time(self):
        self.check_unsigned_integer_property('clt_time', 32)

    def test_parse_wrong_type(self):
        with self.assertRaisesRegex(ValueError, 'does not contain CLTTimeOption data'):
            option = CLTTimeOption()
            option.load_from(b'00020010ff12000000000000000000000000abcd')

    def test_bad_option_length(self):
        with self.assertRaisesRegex(ValueError, 'must have length 4'):
            CLTTimeOption.parse(bytes.fromhex('002e000300000384'))
        with self.assertRaisesRegex(ValueError, 'must have length 4'):
            CLTTimeOption.parse(bytes.fromhex('002e000500000384'))


if __name__ == '__main__':
    unittest.main()