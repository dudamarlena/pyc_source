# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/tests/ipv6/server/handlers/test_handler.py
# Compiled at: 2017-06-23 17:22:45
# Size of source mod 2**32: 413 bytes
"""
Basic handler testing
"""
import unittest
from dhcpkit.ipv6.server.handlers import Handler

class TestHandler(Handler):
    __doc__ = "\n    A handler that doesn't do anything\n    "


class HandlerTestCase(unittest.TestCase):

    def test_str(self):
        handler = TestHandler()
        self.assertEqual(str(handler), 'TestHandler')


if __name__ == '__main__':
    unittest.main()