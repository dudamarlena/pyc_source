# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/rest/api/cell.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 3115 bytes
"""
Treadmill Cell REST api.
"""
import flask, flask_restplus as restplus
from flask_restplus import fields
from treadmill import webutils

def init(api, cors, impl):
    """Configures REST handlers for cell resource."""
    namespace = webutils.namespace(api, __name__, 'Cell REST operations')
    master = api.model('Master', {'hostname': fields.String(description='Hostname'), 
     'idx': fields.Integer(description='Index of master'), 
     'zk-followers-port': fields.Integer(description='ZK follower port'), 
     'zk-election-port': fields.Integer(description='ZK election port'), 
     'zk-jmx-port': fields.Integer(description='ZK JMX port'), 
     'zk-client-port': fields.Integer(description='ZK client port')})
    cell_model = {'_id': fields.String(description='Name'), 
     'username': fields.String(description='Treadmill User ID'), 
     'root': fields.String(description='Treadmill Root'), 
     'archive-server': fields.String(description='Archive Server'), 
     'archive-username': fields.String(description='Archive Username'), 
     'ssq-namespace': fields.String(description='SSQ Namespace'), 
     'location': fields.String(description='Location'), 
     'version': fields.String(description='Version'), 
     'masters': fields.List(fields.Nested(master))}
    request_model = api.model('ReqCell', cell_model)
    response_model = api.model('Cell', cell_model)

    @namespace.route('/')
    class _CellList(restplus.Resource):
        __doc__ = 'Treadmill Cell resource'

        @webutils.get_api(api, cors, marshal=api.marshal_list_with, resp_model=response_model)
        def get(self):
            """Returns list of configured cells."""
            return impl.list()

    @namespace.route('/<cell>')
    @api.doc(params={'cell': 'Cell ID/name'})
    class _CellResource(restplus.Resource):
        __doc__ = 'Treadmill Cell resource.'

        @webutils.get_api(api, cors, marshal=api.marshal_with, resp_model=response_model)
        def get(self, cell):
            """Return Treadmill cell configuration."""
            return impl.get(cell)

        @webutils.post_api(api, cors, req_model=request_model, resp_model=response_model)
        def post(self, cell):
            """Creates Treadmill cell."""
            return impl.create(cell, flask.request.json)

        @webutils.put_api(api, cors, req_model=request_model, resp_model=response_model)
        def put(self, cell):
            """Updates Treadmill cell configuration."""
            return impl.update(cell, flask.request.json)

        @webutils.delete_api(api, cors)
        def delete(self, cell):
            """Deletes Treadmill cell."""
            return impl.delete(cell)