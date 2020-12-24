# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/tests/ipv6/options/test_reconfigure_accept_option.py
# Compiled at: 2017-06-23 17:22:45
# Size of source mod 2**32: 656 bytes
"""
Test the ReconfigureAcceptOption implementation
"""
import unittest
from dhcpkit.ipv6.options import ReconfigureAcceptOption
from dhcpkit.tests.ipv6.options import test_option

class ReconfigureAcceptOptionTestCase(test_option.OptionTestCase):

    def setUp(self):
        self.option_bytes = bytes.fromhex('00140000')
        self.option_object = ReconfigureAcceptOption()
        self.parse_option()

    def test_bad_option_length(self):
        with self.assertRaisesRegex(ValueError, 'must have length 0'):
            ReconfigureAcceptOption.parse(bytes.fromhex('00140001'))


if __name__ == '__main__':
    unittest.main()