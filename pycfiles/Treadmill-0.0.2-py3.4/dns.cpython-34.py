# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/rest/api/dns.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 1784 bytes
"""
Treadmill DNS REST api.
"""
import flask_restplus as restplus
from flask_restplus import fields
from treadmill import webutils

def init(api, cors, impl):
    """Configures REST handlers for DNS resource."""
    namespace = webutils.namespace(api, __name__, 'DNS REST operations')
    server_model = fields.String(description='Server')
    dns_model = {'_id': fields.String(description='Name', max_length=32), 
     'location': fields.String(description='Location'), 
     'nameservers': fields.List(server_model), 
     'rest-server': fields.List(server_model), 
     'zkurl': fields.String(description='Zookeeper URL'), 
     'fqdn': fields.String(description='FQDN'), 
     'ttl': fields.String(description='Time To Live')}
    response_model = api.model('RespDNS', dns_model)

    @namespace.route('/')
    class _DNSList(restplus.Resource):
        __doc__ = 'Treadmill DNS resource'

        @webutils.get_api(api, cors, marshal=api.marshal_list_with, resp_model=response_model)
        def get(self):
            """Returns list of configured DNS servers."""
            return impl.list()

    @namespace.route('/<dns>')
    @api.doc(params={'dns': 'DNS ID/name or FQDN'})
    class _DNSResource(restplus.Resource):
        __doc__ = 'Treadmill DNS resource.'

        @webutils.get_api(api, cors, marshal=api.marshal_with, resp_model=response_model)
        def get(self, dns):
            """Return Treadmill cell configuration."""
            return impl.get(dns)