# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tw\mods\cp3.py
# Compiled at: 2011-07-14 12:06:35
from pkg_resources import require
require('CherryPy >=3.0')
import logging, pprint, cherrypy, tw
from tw.core import resource_injector, resources
from tw.core.registry import Registry
log = logging.getLogger(__name__)

def _extract_config():
    c = cherrypy.config.copy()
    return c


class TWTool(cherrypy.Tool):
    """Sort-of-emulates TWWidgetsMiddleware + Paste's RegistryManager.

    Takes care of preparing the hostframework for a request.

    """
    __module__ = __name__

    def __init__(self, host_framework, prefix='/toscawidgets', serve_files=True):
        self.serve_files = serve_files
        self.prefix = prefix
        self.host_framework = host_framework
        return super(TWTool, self).__init__('on_start_resource', self.on_start_resource)

    def on_start_resource(self):
        log.debug('TWTool: on_start_resource')
        environ = cherrypy.request.wsgi_environ
        registry = environ.setdefault('paste.registry', Registry())
        environ['toscawidgets.prefix'] = self.prefix
        registry.prepare()
        registry.register(tw.framework, self.host_framework)
        self.host_framework.start_request(environ)

    def before_request_body(self):
        """Intercepts requests for static files and serves them."""
        if not self.serve_files:
            return
        req, resp = cherrypy.request, cherrypy.response
        path = req.path_info
        if path.startswith(self.host_framework.webpath):
            path = path[len(self.host_framework.webpath):]
        if path.startswith(self.prefix):
            reg = resources.registry
            path = path[len(self.prefix) + len(reg.prefix):]

            class FakeRequest(object):
                __module__ = __name__
                path_info = path
                params = req.params
                environ = {}

            (stream, ct, enc) = reg.get_stream_type_encoding(FakeRequest)
            if stream:
                resp.body = stream
                if ct:
                    if enc:
                        ct += '; charset=' + enc
                    resp.headers['Content-Type'] = ct
                req.process_request_body = False
                req.handler = None
        return

    def before_finalize(self):
        log.debug('TWTool: before_finalize')
        response = cherrypy.response
        ct = response.headers.get('content-type', 'text/html').lower()
        if 'html' in ct:
            cs = resource_injector.find_charset(ct)
            html = ('').join(response.body)
            resources = tw.framework.pop_resources()
            log.debug('Injecting Resources:')
            map(log.debug, pprint.pformat(resources).split('\n'))
            html = resource_injector.inject_resources(html=html, resources=resources, encoding=cs)
            response.body = [
             html]
            response.headers.pop('Content-Length', None)
        return

    def on_end_request(self):
        log.debug('TWTool: on_end_request')
        try:
            environ = cherrypy.request.wsgi_environ
            self.host_framework.end_request(environ)
        finally:
            registry = environ.get('paste.registry', None)
            if registry:
                registry.cleanup()
        return

    def _setup(self):
        conf = self._merged_args()
        p = conf.pop('priority', None)
        if p is None:
            p = getattr(self.callable, 'priority', self._priority)
        cherrypy.request.hooks.attach(self._point, self.callable, priority=p, **conf)
        cherrypy.request.hooks.attach('on_end_request', self.on_end_request)
        cherrypy.request.hooks.attach('before_request_body', self.before_request_body)
        cherrypy.request.hooks.attach('before_finalize', self.before_finalize)
        return


def start_extension(host_framework, **filter_args):
    cherrypy.tools.toscawidgets = TWTool(host_framework=host_framework, **filter_args)