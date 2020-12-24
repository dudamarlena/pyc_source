# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/loup/Workspace/Projects/personal/palmer/palmer/response.py
# Compiled at: 2016-11-16 03:39:02
# Size of source mod 2**32: 1369 bytes
from __future__ import unicode_literals
import datetime
from flask import request, Response
from flask._compat import text_type, string_types
from palmer.utils import http_statuses

class APIResponse(Response):

    def __init__(self, content=None, *args, **kwargs):
        super(APIResponse, self).__init__(None, *args, **kwargs)
        self.response_at = datetime.datetime.utcnow()
        media_type = None
        if isinstance(content, (list, dict, text_type, string_types)):
            renderer = request.renderer
            media_type = renderer.media_type
            if self.status_code == http_statuses.HTTP_204_NO_CONTENT:
                self.status_code = http_statuses.HTTP_200_OK
            content = self.get_cleaned_content(content)
            content = renderer.render(content, media_type)
        if content is None:
            content = []
        if isinstance(content, (text_type, bytes, bytearray)):
            self.set_data(content)
        else:
            self.response = content
        if media_type is not None:
            self.headers['Content-Type'] = str(media_type)

    def get_cleaned_content(self, content):
        return dict(request_at=request.request_at, response_at=self.response_at, status_code=self.status_code, result=content)