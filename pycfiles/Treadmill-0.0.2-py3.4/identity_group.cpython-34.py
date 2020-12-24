# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/rest/api/identity_group.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 2415 bytes
"""
Treadmill Identity Group REST api.
"""
import flask, flask_restplus as restplus
from flask_restplus import fields
from treadmill import webutils

def init(api, cors, impl):
    """Configures REST handlers for app monitor resource."""
    namespace = webutils.namespace(api, __name__, 'Identity Group REST operations')
    identity_group_model = {'_id': fields.String(description='Name'), 
     'count': fields.Integer(description='Identiy Group Count', required=True)}
    request_model = api.model('ReqIdentityGroup', identity_group_model)
    response_model = api.model('RespIdentityGroup', identity_group_model)

    @namespace.route('/')
    class _IdentityGroupList(restplus.Resource):
        __doc__ = 'Treadmill identity group resource'

        @webutils.get_api(api, cors, marshal=api.marshal_list_with, resp_model=response_model)
        def get(self):
            """Returns list of configured identity groups."""
            return impl.list()

    @namespace.route('/<app_id>')
    @api.doc(params={'app_ip': 'App ID/name'})
    class _IdentityGroupResource(restplus.Resource):
        __doc__ = 'Treadmill identity group resource.'

        @webutils.get_api(api, cors, marshal=api.marshal_with, resp_model=response_model)
        def get(self, app_id):
            """Return identity group configuration."""
            return impl.get(app_id)

        @webutils.post_api(api, cors, req_model=request_model, resp_model=response_model)
        def post(self, app_id):
            """Creates identity group."""
            return impl.create(app_id, flask.request.json)

        @webutils.put_api(api, cors, req_model=request_model, resp_model=response_model)
        def put(self, app_id):
            """Updates identity group configuration."""
            return impl.update(app_id, flask.request.json)

        @webutils.delete_api(api, cors)
        def delete(self, app_id):
            """Deletes identity group."""
            return impl.delete(app_id)