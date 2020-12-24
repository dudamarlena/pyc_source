# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/rest/api/local.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 3241 bytes
"""
Local node REST api.
"""
import os, http.client, flask, flask_restplus as restplus
from treadmill import webutils

def init(api, cors, impl):
    """Configures REST handlers for allocation resource."""
    app_ns = api.namespace('app', description='Local app REST operations')

    @app_ns.route('/')
    class _AppList(restplus.Resource):
        __doc__ = 'Local app list resource.'

        @webutils.get_api(api, cors)
        def get(self):
            """Returns list of local instances."""
            return impl.list(flask.request.args.get('state'))

    @app_ns.route('/<app>/<uniq>')
    class _AppDetails(restplus.Resource):
        __doc__ = 'Local app details resource.'

        @webutils.get_api(api, cors)
        def get(self, app, uniq):
            """Returns list of local instances."""
            return impl.get('/'.join([app, uniq]))

    @app_ns.route('/<app>/<uniq>/sys/<component>')
    class _AppSystemLog(restplus.Resource):
        __doc__ = 'Local app details resource.'

        @webutils.raw_get_api(api, cors)
        def get(self, app, uniq, component):
            """Return content of system component log.."""
            mimetype = 'text/plain'
            return flask.Response(impl.log.get('/'.join([app, uniq, 'sys', component])), mimetype=mimetype)

    @app_ns.route('/<app>/<uniq>/service/<service>')
    class _AppServiceLog(restplus.Resource):
        __doc__ = 'Local app details resource.'

        @webutils.raw_get_api(api, cors)
        def get(self, app, uniq, service):
            """Return content of system component log.."""
            mimetype = 'text/plain'
            return flask.Response(impl.log.get('/'.join([app, uniq, 'app', service])), mimetype=mimetype)

    archive_ns = api.namespace('archive', description='Local archive REST operations')

    @archive_ns.route('/<app>/<uniq>/sys')
    class _SysArchiveAsAttachment(restplus.Resource):
        __doc__ = 'Download sys archive as attachment.'

        @webutils.raw_get_api(api, cors)
        def get(self, app, uniq):
            """Return content of sys archived file.."""
            fname = impl.archive.get('/'.join([app, uniq, 'sys']))
            if not os.path.exists(fname):
                return ('Not found.', http.client.NOT_FOUND)
            return flask.send_file(fname, as_attachment=True, attachment_filename=os.path.basename(fname))

    @archive_ns.route('/<app>/<uniq>/app')
    class _AppArchiveAsAttachment(restplus.Resource):
        __doc__ = 'Download app archive as attachment.'

        @webutils.raw_get_api(api, cors)
        def get(self, app, uniq):
            """Return content of app archived file.."""
            fname = impl.archive.get('/'.join([app, uniq, 'app']))
            if not os.path.exists(fname):
                return ('Not found.', http.client.NOT_FOUND)
            return flask.send_file(fname, as_attachment=True, attachment_filename=os.path.basename(fname))