# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/canteen_tests/test_base/test_protocol.py
# Compiled at: 2014-09-26 04:50:19
"""

  base protocol tests
  ~~~~~~~~~~~~~~~~~~~

  :author: Sam Gammon <sg@samgammon.com>
  :copyright: (c) Sam Gammon, 2014
  :license: This software makes use of the MIT Open Source License.
            A copy of this license is included as ``LICENSE.md`` in
            the root of the project.

"""
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
                pass

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