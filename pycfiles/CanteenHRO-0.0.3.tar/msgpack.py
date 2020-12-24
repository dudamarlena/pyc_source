# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/site-packages/canteen/rpc/protocol/msgpack.py
# Compiled at: 2014-09-26 04:50:19
__doc__ = '\n\n  msgpack RPC protocol\n  ~~~~~~~~~~~~~~~~~~~~\n\n  :author: Sam Gammon <sg@samgammon.com>\n  :copyright: (c) Sam Gammon, 2014\n  :license: This software makes use of the MIT Open Source License.\n            A copy of this license is included as ``LICENSE.md`` in\n            the root of the project.\n\n'
from canteen.core import runtime
from canteen.base import protocol
_content_types = ('application/msgpack', 'application/x-msgpack')
with runtime.Library('msgpack') as (msglib, msgpack):
    with runtime.Library('protorpc') as (protolib, protorpc):
        protojson = protolib.load('protojson')
        messages = protolib.load('messages')

        @protocol.Protocol.register('msgpack', _content_types)
        class Msgpack(protocol.Protocol, protojson.ProtoJson):
            """  """

            def encode_message(self, message):
                """  """
                message.check_initialized()

                def _walk_struct(m):
                    """ recursively encode msgpack """
                    _packed = {}
                    for field in m.all_fields():
                        value = getattr(m, field.name)
                        if value is not None:
                            if isinstance(value, messages.Message):
                                _packed[field.name] = _walk_struct(value)
                            else:
                                _packed[field.name] = value

                    return _packed

                return msgpack.packb(_walk_struct(message))

            def decode_message(self, message_type, encoded_message):
                """  """
                if not encoded_message.strip():
                    return message_type()
                dictionary = msgpack.unpackb(encoded_message)
                message = self._ProtoJson__decode_dictionary(message_type, dictionary)
                message.check_initialized()
                return message