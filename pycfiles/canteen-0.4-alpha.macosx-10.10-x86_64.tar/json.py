# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/canteen/rpc/protocol/json.py
# Compiled at: 2014-09-26 04:50:19
"""

  JSON RPC protocol
  ~~~~~~~~~~~~~~~~~

  :author: Sam Gammon <sg@samgammon.com>
  :copyright: (c) Sam Gammon, 2014
  :license: This software makes use of the MIT Open Source License.
            A copy of this license is included as ``LICENSE.md`` in
            the root of the project.

"""
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