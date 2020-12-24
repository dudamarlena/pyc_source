# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/rest/api/app_monitor.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 2458 bytes
"""
Treadmill App monitor REST api.
"""
import flask, flask_restplus as restplus
from flask_restplus import fields
from treadmill import webutils

def init(api, cors, impl):
    """Configures REST handlers for app monitor resource."""
    namespace = webutils.namespace(api, __name__, 'Application monitor REST operations')
    app_monitor_model = {'_id': fields.String(description='Name'), 
     'count': fields.Integer(description='Count', required=True)}
    request_model = api.model('ReqAppMonitor', app_monitor_model)
    response_model = api.model('RespAppMonitor', app_monitor_model)

    @namespace.route('/')
    class _AppMonitorList(restplus.Resource):
        __doc__ = 'Treadmill App monitor resource'

        @webutils.get_api(api, cors, marshal=api.marshal_list_with, resp_model=response_model)
        def get(self):
            """Returns list of configured app monitors."""
            return impl.list()

    @namespace.route('/<app_monitor>')
    @api.doc(params={'app_monitor': 'Application Monitor ID/name'})
    class _AppMonitorResource(restplus.Resource):
        __doc__ = 'Treadmill App monitor resource.'

        @webutils.get_api(api, cors, marshal=api.marshal_with, resp_model=response_model)
        def get(self, app_monitor):
            """Return Treadmill application monitor configuration."""
            return impl.get(app_monitor)

        @webutils.post_api(api, cors, req_model=request_model, resp_model=response_model)
        def post(self, app_monitor):
            """Creates Treadmill application."""
            return impl.create(app_monitor, flask.request.json)

        @webutils.put_api(api, cors, req_model=request_model, resp_model=response_model)
        def put(self, app_monitor):
            """Updates Treadmill application configuration."""
            return impl.update(app_monitor, flask.request.json)

        @webutils.delete_api(api, cors)
        def delete(self, app_monitor):
            """Deletes Treadmill application monitor."""
            return impl.delete(app_monitor)