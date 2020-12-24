# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/views/file_upload.py
# Compiled at: 2019-10-30 05:24:12
# Size of source mod 2**32: 973 bytes
import os
from jet_bridge_base.configuration import configuration
from jet_bridge_base.permissions import HasProjectPermissions
from jet_bridge_base.responses.json import JSONResponse
from jet_bridge_base.views.base.api import APIView

class FileUploadView(APIView):
    permission_classes = (
     HasProjectPermissions,)

    def post(self, *args, **kwargs):
        original_filename, file = self.request.files.get('file', None)
        path = self.request.get_body_argument('path')
        filename = self.request.get_body_argument('filename', original_filename)
        upload_path = os.path.join(path, filename)
        upload_path = configuration.media_get_available_name(upload_path)
        configuration.media_save(upload_path, file)
        return JSONResponse({'uploaded_path': upload_path, 
         'uploaded_url': configuration.media_url(upload_path, self.request)})