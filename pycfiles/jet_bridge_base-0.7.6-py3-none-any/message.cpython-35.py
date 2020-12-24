# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/views/message.py
# Compiled at: 2019-10-30 05:24:12
# Size of source mod 2**32: 564 bytes
from jet_bridge_base.permissions import HasProjectPermissions
from jet_bridge_base.responses.optional_json import OptionalJSONResponse
from jet_bridge_base.serializers.message import MessageSerializer
from jet_bridge_base.views.base.api import APIView

class MessageView(APIView):
    permission_classes = (
     HasProjectPermissions,)

    def post(self, *args, **kwargs):
        serializer = MessageSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        return OptionalJSONResponse(result)