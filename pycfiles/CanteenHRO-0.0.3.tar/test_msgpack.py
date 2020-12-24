# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/site-packages/canteen_tests/test_rpc/test_msgpack.py
# Compiled at: 2014-09-26 04:50:19
__doc__ = "\n\n  msgpack protocol tests\n  ~~~~~~~~~~~~~~~~~~~~~~\n\n  tests canteen's builtin msgpack RPC protocol.\n\n  :author: Sam Gammon <sg@samgammon.com>\n  :copyright: (c) Sam Gammon, 2014\n  :license: This software makes use of the MIT Open Source License.\n      A copy of this license is included as ``LICENSE.md`` in\n      the root of the project.\n\n"
from canteen.model import Model
from canteen.core import Library
from canteen.test import FrameworkTest
with Library('msgpack', strict=True) as (mlibrary, msgpack):
    import msgpack
    with Library('protorpc', strict=True) as (plibrary, protorpc):
        messages = plibrary.load('messages')
        from canteen.rpc.protocol import msgpack as msgpackrpc

        class SampleMessage(messages.Message):
            """ Sample ProtoRPC message. """
            string = messages.StringField(1)
            integer = messages.IntegerField(2)


        class SampleParentMessage(messages.Message):
            """ Sample parent Message class. """
            sub = messages.MessageField(SampleMessage, 1)
            string = messages.StringField(2)
            integer = messages.IntegerField(3)


        class TestMsgpackRPCModel(Model):
            """ Sample ProtoRPC-integrated model """
            string = str
            integer = int


        class TestMsgpackRPCParentModel(Model):
            """ Sample ProtoRPC-integrated parent model. """
            sub = TestMsgpackRPCModel
            string = str
            integer = int


        class MsgpackProtocolTests(FrameworkTest):
            """ Tests `rpc.protocol.msgpack.Msgpack` """

            def test_msgpack_encode_message(self):
                """ Test encoding RPC messages in msgpack """
                msg = SampleMessage(string='hi', integer=5)
                protocol = msgpackrpc.Msgpack()
                result = protocol.encode_message(msg)
                inflated = msgpack.unpackb(result)
                assert 'string' in inflated
                assert 'integer' in inflated
                assert inflated['string'] == 'hi'
                assert inflated['integer'] == 5
                return (
                 result, protocol)

            def test_msgpack_decode_message(self):
                """ Test decoding RPC messages from msgpack """
                encoded, protocol = self.test_msgpack_encode_message()
                decoded = protocol.decode_message(SampleMessage, encoded)
                assert decoded.string == 'hi'
                assert decoded.integer == 5

            def test_msgpack_encode_recursive(self):
                """ Test recursively encoding an RPC message using msgpack """
                s = SampleMessage(string='hiblab', integer=5)
                m = SampleParentMessage(string='hibleebs', integer=10, sub=s)
                assert s.integer == m.sub.integer == 5
                assert s.string == m.sub.string == 'hiblab'
                assert m.string == 'hibleebs'
                assert m.integer == 10
                assert m.sub is s
                assert isinstance(m, SampleParentMessage)
                assert isinstance(s, SampleMessage) and isinstance(m.sub, SampleMessage)
                protocol = msgpackrpc.Msgpack()
                result = protocol.encode_message(m)
                assert result
                assert isinstance(msgpack.loads(result), dict)
                return (
                 result, s)

            def test_msgpack_decode_recursive(self):
                """ Test recursively decoding an RPC message using msgpack """
                encoded, sub = self.test_msgpack_encode_recursive()
                protocol = msgpackrpc.Msgpack()
                result = protocol.decode_message(SampleParentMessage, encoded)
                assert sub.integer == result.sub.integer == 5
                assert sub.string == result.sub.string == 'hiblab'
                assert result.string == 'hibleebs'
                assert result.integer == 10
                assert result.sub
                assert isinstance(result, SampleParentMessage)
                assert isinstance(result.sub, SampleMessage)