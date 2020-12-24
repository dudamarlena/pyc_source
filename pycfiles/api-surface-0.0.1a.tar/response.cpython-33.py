# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/tomchristie/GitHub/api-star/api_star/frameworks/flask/response.py
# Compiled at: 2016-04-13 15:50:46
# Size of source mod 2**32: 680 bytes
from __future__ import unicode_literals
from coreapi import Document
from flask import request, Response
from api_star.core import render

class APIResponse(Response):

    def __init__(self, data=None, *args, **kwargs):
        super(APIResponse, self).__init__(None, *args, **kwargs)
        content, content_type = render(request, data)
        self.set_data(content)
        if content_type:
            self.headers['Content-Type'] = content_type
        return

    @classmethod
    def force_type(cls, response, environ=None):
        if isinstance(response, (Document, list, dict)):
            return cls(response)
        return Response.force_type(response, environ)