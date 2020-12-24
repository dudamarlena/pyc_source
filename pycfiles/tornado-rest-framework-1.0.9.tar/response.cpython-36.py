# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/work/lib/pyenv/versions/3.6.1/envs/maestro/lib/python3.6/site-packages/rest_framework/core/response.py
# Compiled at: 2018-10-12 04:41:52
# Size of source mod 2**32: 2153 bytes
import typing
from rest_framework.core.types import Receive, Send
from rest_framework.utils.escape import json_encode

class Response:
    charset = 'utf-8'

    def __init__(self, data: typing.Any, status_code: int=200, headers: dict=None, content_type='application/json') -> None:
        self.content_type = content_type
        self.body = self.render(data)
        self.status_code = status_code
        self.init_headers(headers)

    def render(self, content: typing.Any) -> bytes:
        if self.content_type == 'application/json':
            return json_encode(content).encode(self.charset)
        else:
            if isinstance(content, bytes):
                return content
            return content.encode(self.charset)

    def init_headers(self, headers):
        if headers is None:
            raw_headers = []
            populate_content_length = True
            populate_content_type = True
        else:
            raw_headers = [(k.lower().encode('latin-1'), v.encode('latin-1')) for k, v in headers.items()]
            keys = [h[0] for h in raw_headers]
            populate_content_length = b'content-length' in keys
            populate_content_type = b'content-type' in keys
        body = getattr(self, 'body', None)
        if body is not None:
            if populate_content_length:
                content_length = str(len(body))
                raw_headers.append((b'content-length', content_length.encode('latin-1')))
        else:
            content_type = self.content_type
            if content_type is not None:
                if populate_content_type:
                    if content_type.startswith('text/'):
                        content_type += '; charset=' + self.charset
                    raw_headers.append((b'content-type', content_type.encode('latin-1')))
        self.raw_headers = raw_headers

    async def __call__(self, receive: Receive, send: Send) -> None:
        await send({'type':'http.response.start', 
         'status':self.status_code, 
         'headers':self.raw_headers})
        await send({'type':'http.response.body',  'body':self.body})