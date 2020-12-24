# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/views/reload.py
# Compiled at: 2020-03-04 22:15:05
# Size of source mod 2**32: 729 bytes
from jet_bridge_base.db import dispose_connection, get_request_connection
from jet_bridge_base.permissions import HasProjectPermissions
from jet_bridge_base.responses.json import JSONResponse
from jet_bridge_base.views.base.api import APIView

class ReloadView(APIView):
    permission_classes = (
     HasProjectPermissions,)

    def required_project_permission(self):
        return {'permission_type': 'project', 
         'permission_object': 'project_settings', 
         'permission_actions': ''}

    def post(self, *args, **kwargs):
        result = dispose_connection(self.request)
        get_request_connection(self.request)
        return JSONResponse({'success': result})