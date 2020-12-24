# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/rest/api/tenant.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 2551 bytes
"""
Treadmill Tenant REST api.
"""
import flask, flask_restplus as restplus
from flask_restplus import fields
from treadmill import webutils

def init(api, cors, impl):
    """Configures REST handlers for tenant resource."""
    namespace = webutils.namespace(api, __name__, 'Tenant REST operations')
    tenant_model = {'_id': fields.String(description='Tenant name'), 
     'tenant': fields.String(description='Tenant name'), 
     'systems': fields.List(fields.Integer(description='System ID', required=True), min_items=1)}
    request_model = api.model('ReqTenant', tenant_model)
    response_model = api.model('RespTenant', tenant_model)

    @namespace.route('/')
    class _TenantList(restplus.Resource):
        __doc__ = 'Treadmill Tenant resource'

        @webutils.get_api(api, cors, marshal=api.marshal_list_with, resp_model=response_model)
        def get(self):
            """Returns list of configured tenants."""
            return impl.list()

    @namespace.route('/<tenant_id>')
    @api.doc(params={'tenant_id': 'Tenant ID/name'})
    class _TenantResource(restplus.Resource):
        __doc__ = 'Treadmill Tenant resource.'

        @webutils.get_api(api, cors, marshal=api.marshal_with, resp_model=response_model)
        def get(self, tenant_id):
            """Return Treadmill tenant configuration."""
            return impl.get(tenant_id)

        @webutils.post_api(api, cors, req_model=request_model, resp_model=response_model)
        def post(self, tenant_id):
            """Creates Treadmill tenant."""
            return impl.create(tenant_id, flask.request.json)

        @webutils.put_api(api, cors, req_model=request_model, resp_model=response_model)
        def put(self, tenant_id):
            """Updates Treadmill tenant configuration."""
            return impl.update(tenant_id, flask.request.json)

        @webutils.delete_api(api, cors)
        def delete(self, tenant_id):
            """Deletes Treadmill tenant."""
            return impl.delete(tenant_id)