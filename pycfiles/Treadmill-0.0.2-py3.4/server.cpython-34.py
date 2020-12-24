# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/rest/api/server.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 1529 bytes
"""
Treadmill Server REST api.
"""
import flask, flask_restplus as restplus
from treadmill import webutils

def init(api, cors, impl):
    """Configures REST handlers for server resource."""
    namespace = webutils.namespace(api, __name__, 'Server REST operations')

    @namespace.route('/')
    class _ServerList(restplus.Resource):
        __doc__ = 'Treadmill Server resource'

        @webutils.get_api(api, cors)
        def get(self):
            """Returns list of configured servers."""
            return impl.list(flask.request.args.get('cell'), flask.request.args.getlist('features'))

    @namespace.route('/<server_id>')
    class _ServerResource(restplus.Resource):
        __doc__ = 'Treadmill Server resource.'

        @webutils.get_api(api, cors)
        def get(self, server_id):
            """Return Treadmill server configuration."""
            return impl.get(server_id)

        @webutils.delete_api(api, cors)
        def delete(self, server_id):
            """Deletes Treadmill server."""
            return impl.delete(server_id)

        @webutils.put_api(api, cors)
        def put(self, server_id):
            """Updates Treadmill server configuration."""
            return impl.update(server_id, flask.request.json)

        @webutils.post_api(api, cors)
        def post(self, server_id):
            """Creates Treadmill server."""
            return impl.create(server_id, flask.request.json)