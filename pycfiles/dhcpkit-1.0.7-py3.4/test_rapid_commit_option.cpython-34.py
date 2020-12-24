# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/tests/ipv6/options/test_rapid_commit_option.py
# Compiled at: 2017-06-23 17:22:45
# Size of source mod 2**32: 626 bytes
"""
Test the RapidCommitOption implementation
"""
import unittest
from dhcpkit.ipv6.options import RapidCommitOption
from dhcpkit.tests.ipv6.options import test_option

class RapidCommitOptionTestCase(test_option.OptionTestCase):

    def setUp(self):
        self.option_bytes = bytes.fromhex('000e0000')
        self.option_object = RapidCommitOption()
        self.parse_option()

    def test_bad_option_length(self):
        with self.assertRaisesRegex(ValueError, 'must have length 0'):
            RapidCommitOption.parse(bytes.fromhex('000e0001'))


if __name__ == '__main__':
    unittest.main()