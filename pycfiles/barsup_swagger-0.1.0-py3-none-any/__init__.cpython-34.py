# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pirogov/.virtualenvs/py3bup/lib/python3.4/site-packages/barsup_swagger/__init__.py
# Compiled at: 2015-03-04 07:52:48
# Size of source mod 2**32: 1072 bytes
import os
from webob import Response
from webob.dec import wsgify
from webob.static import DirectoryApp

def with_swagger(spec_file_name, path='/swagger'):
    """
    WSGI-middleware, релизующее поведение серверной стороны Swagger-UI
    """
    static_path = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'static')
    static_app = DirectoryApp(static_path, hide_index_with_redirect=True)
    spec_file_name = os.path.expandvars(spec_file_name)

    @wsgify.middleware
    def swagger_middleware(request, app):
        url = request.path
        if url == '/v2/swagger.json':
            with open(spec_file_name, encoding='utf-8') as (f):
                return Response(body=f.read(), content_type='application/json')
        else:
            if url.startswith(path):
                return static_app
            else:
                return app

    return swagger_middleware