# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/tests/ipv6/options/test_client_id_option.py
# Compiled at: 2017-06-23 17:22:45
# Size of source mod 2**32: 742 bytes
"""
Test the ClientIdOption implementation
"""
import unittest
from dhcpkit.ipv6.duids import EnterpriseDUID
from dhcpkit.ipv6.options import ClientIdOption
from dhcpkit.tests.ipv6.options import test_option

class ClientIdOptionTestCase(test_option.OptionTestCase):

    def setUp(self):
        self.option_bytes = b'\x00\x01\x00\x15\x00\x02\x00\x00\x9d\x100123456789abcde'
        self.option_object = ClientIdOption(EnterpriseDUID(40208, b'0123456789abcde'))
        self.parse_option()

    def test_validate_duid(self):
        self.option.duid = b'0123456789abcdef'
        with self.assertRaisesRegex(ValueError, 'DUID object'):
            self.option.validate()


if __name__ == '__main__':
    unittest.main()