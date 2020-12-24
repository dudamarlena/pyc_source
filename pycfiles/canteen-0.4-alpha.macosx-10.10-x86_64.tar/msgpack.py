# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/canteen/rpc/protocol/msgpack.py
# Compiled at: 2014-09-26 04:50:19
"""

  msgpack RPC protocol
  ~~~~~~~~~~~~~~~~~~~~

  :author: Sam Gammon <sg@samgammon.com>
  :copyright: (c) Sam Gammon, 2014
  :license: This software makes use of the MIT Open Source License.
            A copy of this license is included as ``LICENSE.md`` in
            the root of the project.

"""
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