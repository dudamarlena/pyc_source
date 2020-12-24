# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/windmill/server/wsgi.py
# Compiled at: 2011-01-13 02:54:30
import httplib, copy, socket, random, os, logging, threading, sys
from time import sleep
if not sys.version.startswith('2.4'):
    from urlparse import urlparse
else:
    from windmill.tools.urlparse_25 import urlparse
logger = logging.getLogger(__name__)
import windmill
from windmill.server import proxy
from windmill.dep import wsgi_jsonrpc
from windmill.dep import wsgi_xmlrpc
from windmill.dep import wsgi_fileserver
import jsmin
START_DST_PORT = 32000
CURRENT_DST_PORT = [random.randint(32000, 34000)]

def reconstruct_url(environ):
    from urllib import quote
    url = environ['wsgi.url_scheme'] + '://'
    if environ.get('HTTP_HOST'):
        url += environ['HTTP_HOST']
    else:
        url += environ['SERVER_NAME']
        if environ['wsgi.url_scheme'] == 'https':
            if environ['SERVER_PORT'] != '443':
                url += ':' + environ['SERVER_PORT']
        elif environ['SERVER_PORT'] != '80':
            url += ':' + environ['SERVER_PORT']
    url += environ.get('SCRIPT_NAME', '')
    url += environ.get('PATH_INFO', '')
    if url.find('%3B') is not -1:
        (url, arg) = url.split('%3B', 1)
        url = (';').join([url, arg.replace('%3D', '=')])
    if environ.get('QUERY_STRING'):
        url += '?' + environ['QUERY_STRING']
    environ['reconstructed_url'] = url
    return url


HTTPConnection = httplib.HTTPConnection
WindmillProxyApplication = proxy.WindmillProxyApplication
WindmillProxyApplication.ConnectionClass = HTTPConnection
add_namespace = None

class WindmillChooserApplication(object):
    """Application to handle choosing the proper application to handle each request"""

    def __init__(self, apps, proxy):
        self.namespaces = dict([ (arg.ns, arg) for arg in apps ])
        self.proxy = proxy

    def add_namespace(self, name, application):
        """Add an application to a specific url namespace in windmill"""
        self.namespaces[name] = application

    def handler(self, environ, start_response):
        """Windmill app chooser"""
        sleep(0.2)
        reconstruct_url(environ)
        for key in self.namespaces:
            if environ['PATH_INFO'].find('/' + key + '/') is not -1:
                logger.debug('dispatching request %s to %s' % (environ['reconstructed_url'], key))
                return self.namespaces[key](environ, start_response)

        logger.debug('dispatching request %s to WindmillProxyApplication' % reconstruct_url(environ))
        response = self.proxy(environ, start_response)
        return response

    def __call__(self, environ, start_response):
        response = self.handler(environ, start_response)
        for x in response:
            yield x


class WindmillCompressor(object):
    """Full JavaScript Compression Library"""
    js_file_list = [
     ('lib', 'firebug', 'pi.js'),
     ('lib', 'firebug', 'firebug-lite.js'),
     ('lib', 'json2.js'),
     ('lib', 'browserdetect.js'),
     ('wm', 'windmill.js'),
     ('lib', 'getXPath.js'),
     ('lib', 'elementslib.js'),
     ('lib', 'js-xpath.js'),
     ('controller', 'controller.js'),
     ('controller', 'commands.js'),
     ('controller', 'asserts.js'),
     ('controller', 'waits.js'),
     ('controller', 'flex.js'),
     ('wm', 'registry.js'),
     ('extensions', 'extensions.js'),
     ('wm', 'utils.js'),
     ('wm', 'ide', 'ui.js'),
     ('wm', 'ide', 'recorder.js'),
     ('wm', 'ide', 'remote.js'),
     ('wm', 'ide', 'dx.js'),
     ('wm', 'ide', 'ax.js'),
     ('wm', 'ide', 'results.js'),
     ('wm', 'xhr.js'),
     ('wm', 'metrics.js'),
     ('wm', 'events.js'),
     ('wm', 'global.js'),
     ('wm', 'jstest.js'),
     ('wm', 'load.js')]

    def __init__(self, js_path, enabled=True):
        self.enabled = enabled
        self.js_path = js_path
        self.compressed_windmill = None
        if enabled:
            self._thread = threading.Thread(target=self.compress_file)
            self._thread.start()
        return

    def compress_file(self):
        compressed_windmill = ''
        for filename in self.js_file_list:
            compressed_windmill += jsmin.jsmin(open(os.path.join(self.js_path, *filename), 'r').read())

        self.compressed_windmill = compressed_windmill

    def __call__(self, environ, start_response):
        if not self.enabled:
            start_response('404 Not Found', [('Content-Type', 'text/plain'), ('Content-Length', '0')])
            return [
             '']
        while not self.compressed_windmill:
            sleep(0.15)

        start_response('200 Ok', [('Content-Type', 'application/x-javascript'),
         (
          'Content-Length', str(len(self.compressed_windmill)))])
        return [self.compressed_windmill]


def make_windmill_server(http_port=None, js_path=None, compression_enabled=None):
    global add_namespace
    if http_port is None:
        http_port = windmill.settings['SERVER_HTTP_PORT']
    if js_path is None:
        js_path = windmill.settings['JS_PATH']
    if compression_enabled is None:
        compression_enabled = not windmill.settings['DISABLE_JS_COMPRESS']
    import convergence
    test_resolution_suite = convergence.TestResolutionSuite()
    command_resolution_suite = convergence.CommandResolutionSuite()
    queue = convergence.ControllerQueue(command_resolution_suite, test_resolution_suite)
    xmlrpc_methods_instance = convergence.XMLRPCMethods(queue, test_resolution_suite, command_resolution_suite)
    jsonrpc_methods_instance = convergence.JSONRPCMethods(queue, test_resolution_suite, command_resolution_suite)
    windmill_serv_app = wsgi_fileserver.WSGIFileServerApplication(root_path=js_path, mount_point='/windmill-serv/')
    windmill_proxy_app = WindmillProxyApplication()
    windmill_xmlrpc_app = wsgi_xmlrpc.WSGIXMLRPCApplication(instance=xmlrpc_methods_instance)
    windmill_jsonrpc_app = wsgi_jsonrpc.WSGIJSONRPCApplication(instance=jsonrpc_methods_instance)
    windmill_compressor_app = WindmillCompressor(os.path.join(js_path, 'js'), compression_enabled)
    windmill_serv_app.ns = 'windmill-serv'
    windmill_xmlrpc_app.ns = 'windmill-xmlrpc'
    windmill_jsonrpc_app.ns = 'windmill-jsonrpc'
    windmill_compressor_app.ns = 'windmill-compressor'
    import https
    if windmill.has_ssl:
        import certificate
        cc = certificate.CertificateCreator()
    else:
        cc = None
    httpd = https.WindmillHTTPServer(('0.0.0.0', http_port), https.WindmillHTTPRequestHandler, cc, apps=[
     windmill_serv_app, windmill_jsonrpc_app,
     windmill_xmlrpc_app, windmill_compressor_app], proxy=https.WindmillHTTPSProxyApplication())
    add_namespace = httpd.add_namespace
    httpd.controller_queue = queue
    httpd.test_resolution_suite = test_resolution_suite
    httpd.command_resolution_suite = command_resolution_suite
    httpd.xmlrpc_methods_instance = xmlrpc_methods_instance
    httpd.jsonrpc_methods_instance = jsonrpc_methods_instance
    return httpd