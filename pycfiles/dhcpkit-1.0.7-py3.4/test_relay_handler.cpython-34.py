# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/tests/ipv6/server/handlers/test_relay_handler.py
# Compiled at: 2017-06-23 17:22:45
# Size of source mod 2**32: 828 bytes
"""
Tests for a relay message handler
"""
import unittest
from dhcpkit.ipv6.messages import RelayForwardMessage, RelayReplyMessage
from dhcpkit.ipv6.server.handlers import RelayHandler
from dhcpkit.ipv6.server.transaction_bundle import TransactionBundle

class TestRelayHandler(RelayHandler):
    __doc__ = "\n    A relay handler that doesn't do anything\n    "

    def handle_relay(self, bundle: TransactionBundle, relay_message_in: RelayForwardMessage, relay_message_out: RelayReplyMessage):
        """
        Handler implementation that doesn't do anything
        """
        pass


class RelayHandlerTestCase(unittest.TestCase):

    def test_str(self):
        handler = TestRelayHandler()
        self.assertEqual(str(handler), 'TestRelayHandler')


if __name__ == '__main__':
    unittest.main()