# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/site-packages/canteen/rpc/protocol/json.py
# Compiled at: 2014-09-26 04:50:19
__doc__ = '\n\n  JSON RPC protocol\n  ~~~~~~~~~~~~~~~~~\n\n  :author: Sam Gammon <sg@samgammon.com>\n  :copyright: (c) Sam Gammon, 2014\n  :license: This software makes use of the MIT Open Source License.\n            A copy of this license is included as ``LICENSE.md`` in\n            the root of the project.\n\n'
from canteen.core import runtime
from canteen.base import protocol
_content_types = ('application/json', 'application/x-javascript', 'text/javascript',
                  'text/x-javascript', 'text/x-json', 'text/json')
with runtime.Library('protorpc') as (library, protorpc):
    protojson = library.load('protojson')
    json = __import__('json', globals(), locals(), [], 0)

    @protocol.Protocol.register('json', _content_types)
    class JSON(protocol.Protocol, protojson.ProtoJson):
        """  """

        def encode_message(self, message):
            """  """
            return protojson.ProtoJson().encode_message(message)

        def decode_message(self, message_type, encoded_message):
            """  """
            return protojson.ProtoJson().decode_message(message_type, encoded_message)