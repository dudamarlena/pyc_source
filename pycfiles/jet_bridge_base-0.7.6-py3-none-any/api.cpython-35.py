# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/views/api.py
# Compiled at: 2020-03-04 23:26:03
# Size of source mod 2**32: 451 bytes
from jet_bridge_base.configuration import configuration
from jet_bridge_base.responses.json import JSONResponse
from jet_bridge_base.views.base.api import BaseAPIView

class ApiView(BaseAPIView):

    def get(self, *args, **kwargs):
        return JSONResponse({'version': configuration.get_version(), 
         'type': configuration.get_type(), 
         'media_url_template': configuration.media_url('{}', self.request)})