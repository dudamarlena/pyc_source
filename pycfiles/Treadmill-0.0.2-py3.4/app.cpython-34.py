# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/rest/api/app.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 2082 bytes
"""
Treadmill App REST api.
"""
import flask, flask_restplus as restplus
from treadmill import webutils
from treadmill.api.model import app as app_model

def init(api, cors, impl):
    """Configures REST handlers for app resource."""
    namespace = webutils.namespace(api, __name__, 'Application REST operations')
    request_model, response_model = app_model.models(api)

    @namespace.route('/')
    class _AppList(restplus.Resource):
        __doc__ = 'Treadmill App resource'

        @webutils.get_api(api, cors, marshal=api.marshal_list_with, resp_model=response_model)
        def get(self):
            """Returns list of configured applications."""
            ret = impl.list()
            return ret

    @namespace.route('/<app>')
    @api.doc(params={'app': 'Application ID/Name'})
    class _AppResource(restplus.Resource):
        __doc__ = 'Treadmill App resource.'

        @webutils.get_api(api, cors, marshal=api.marshal_with, resp_model=response_model)
        def get(self, app):
            """Return Treadmill application configuration."""
            return impl.get(app)

        @webutils.post_api(api, cors, req_model=request_model, resp_model=response_model)
        def post(self, app):
            """Creates Treadmill application."""
            return impl.create(app, flask.request.json)

        @webutils.put_api(api, cors, req_model=request_model, resp_model=response_model)
        def put(self, app):
            """Updates Treadmill application configuration."""
            return impl.update(app, flask.request.json)

        @webutils.delete_api(api, cors)
        def delete(self, app):
            """Deletes Treadmill application."""
            return impl.delete(app)