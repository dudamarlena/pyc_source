# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/views/sql.py
# Compiled at: 2019-10-30 05:24:12
# Size of source mod 2**32: 912 bytes
from jet_bridge_base.exceptions.sql import SqlError
from jet_bridge_base.permissions import HasProjectPermissions
from jet_bridge_base.responses.json import JSONResponse
from jet_bridge_base.serializers.sql import SqlSerializer, SqlsSerializer
from jet_bridge_base.views.base.api import APIView
from jet_bridge_base.status import HTTP_400_BAD_REQUEST

class SqlView(APIView):
    permission_classes = (
     HasProjectPermissions,)

    def post(self, *args, **kwargs):
        if 'queries' in self.request.data:
            serializer = SqlsSerializer(data=(self.request.data))
        else:
            serializer = SqlSerializer(data=(self.request.data))
        serializer.is_valid(raise_exception=True)
        try:
            return JSONResponse(serializer.execute(serializer.validated_data))
        except SqlError as e:
            return JSONResponse({'error': e.detail.string}, status=HTTP_400_BAD_REQUEST)