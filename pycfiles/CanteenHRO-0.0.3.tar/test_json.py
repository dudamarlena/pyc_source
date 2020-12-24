# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/site-packages/canteen_tests/test_rpc/test_json.py
# Compiled at: 2014-09-26 04:50:19
__doc__ = "\n\n  JSON protocol tests\n  ~~~~~~~~~~~~~~~~~~~\n\n  tests canteen's builtin JSON RPC protocol.\n\n  :author: Sam Gammon <sg@samgammon.com>\n  :copyright: (c) Sam Gammon, 2014\n  :license: This software makes use of the MIT Open Source License.\n      A copy of this license is included as ``LICENSE.md`` in\n      the root of the project.\n\n"
import json
from canteen.core import Library
from canteen.test import FrameworkTest
with Library('protorpc', strict=True) as (library, protorpc):
    messages = library.load('messages')
    from canteen.rpc.protocol import json as jsonrpc

    class SampleMessage(messages.Message):
        """ Sample ProtoRPC message. """
        string = messages.StringField(1)
        integer = messages.IntegerField(2)


    class JSONProtocolTests(FrameworkTest):
        """ Tests `rpc.protocol.json.JSON` """

        def test_json_construct(self):
            """ Test basic construction of JSON RPC protocol """
            jsonrpc.JSON()

        def test_json_encode_message(self):
            """ Test encoding RPC messages in JSON """
            msg = SampleMessage(string='hi', integer=5)
            protocol = jsonrpc.JSON()
            result = protocol.encode_message(msg)
            inflated = json.loads(result)
            assert 'string' in inflated
            assert 'integer' in inflated
            assert inflated['string'] == 'hi'
            assert inflated['integer'] == 5
            return (
             result, protocol)

        def test_json_decode_message(self):
            """ Test decoding RPC messages from JSON """
            encoded, protocol = self.test_json_encode_message()
            decoded = protocol.decode_message(SampleMessage, encoded)
            assert decoded.string == 'hi'
            assert decoded.integer == 5