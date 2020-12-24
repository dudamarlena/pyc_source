# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/site-packages/canteen_tests/test_base/test_protocol.py
# Compiled at: 2014-09-26 04:50:19
__doc__ = '\n\n  base protocol tests\n  ~~~~~~~~~~~~~~~~~~~\n\n  :author: Sam Gammon <sg@samgammon.com>\n  :copyright: (c) Sam Gammon, 2014\n  :license: This software makes use of the MIT Open Source License.\n            A copy of this license is included as ``LICENSE.md`` in\n            the root of the project.\n\n'
from canteen import test
from canteen.base import protocol

class SomeValidProtocol(protocol.Protocol):
    """ I am a valid, registered protocol """

    def encode_message(self, message):
        """ sample encode message """
        pass

    def decode_message(self, _type, encoded):
        """ sample decode message """
        pass


class BaseProtocolTest(test.FrameworkTest):
    """ Tests `base.protocol`. """

    def _make_protocol(self, valid=True):
        """ Build a quick mock Protocol """
        if valid:

            class _SomeValidProtocol(protocol.Protocol):
                """ I am a valid, registered protocol """

                def encode_message(self, message):
                    """ sample encode message """
                    pass

                def decode_message(self, _type, encoded):
                    """ sample decode message """
                    pass

            return _SomeValidProtocol
        else:

            class SomeInvalidProtocol(protocol.Protocol):
                """ I am an invalid protocol """

            return SomeInvalidProtocol

    def test_base_protocol(self):
        """ Test that `base` exports `Protocol` """
        assert hasattr(protocol, 'Protocol')

    def test_protocol_abstract(self):
        """ Test that `Protocol` is abstract """
        with self.assertRaises(TypeError):
            self._make_protocol(valid=False)()

    def test_protocol_extend(self):
        """ Test that `Protocol` can be extended """
        self._make_protocol()()

    def test_protocol_register(self):
        """ Test that `Protocol` registers properly """
        protocol.Protocol.register('randorpc', ('application/rando', 'application/x-rando'))(SomeValidProtocol)

    def test_protocol_all(self):
        """ Test that `Protocol.all` iterates over registered protocols """
        protocol.Protocol.register('randorpc', ('application/rando', 'application/x-rando'))(SomeValidProtocol)
        all_protocols = [ p for p in protocol.Protocol.all ]
        assert SomeValidProtocol in all_protocols

    def test_protocol_mapping(self):
        """ Test that `Protocol.mapping` returns a proper type=>protocol
        mapping """
        protocol.Protocol.register('randorpc', ('application/rando', 'application/x-rando'))(SomeValidProtocol)
        map = protocol.Protocol.mapping
        assert isinstance(*(
         map.lookup_by_name('randorpc').protocol, SomeValidProtocol))
        assert isinstance(*(
         map.lookup_by_content_type('application/rando').protocol,
         SomeValidProtocol))