# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/windmill/server/proxy.py
# Compiled at: 2011-01-13 01:48:00
import windmill
from httplib import HTTPConnection
import copy, sys, logging, urllib
logger = logging.getLogger(__name__)
from forwardmanager import ForwardManager
if not sys.version.startswith('2.4'):
    from urlparse import urlparse
else:
    from windmill.tools.urlparse_25 import urlparse
first_forward_domains = []
exclude_from_retry = [
 'http://sb-ssl.google.com',
 'https://sb-ssl.google.com',
 'http://en-us.fxfeeds.mozilla.com',
 'fxfeeds.mozilla.com',
 'http://www.google-analytics.com']
_hoppish = {'connection': 1, 
   'keep-alive': 1, 'proxy-authenticate': 1, 'proxy-authorization': 1, 
   'te': 1, 'trailers': 1, 'transfer-encoding': 1, 'upgrade': 1, 
   'proxy-connection': 1, 'p3p': 1}
cache_headers = {'Pragma': 'no-cache', 'Cache-Control': 'post-check=0, pre-check=0', 'Cache-Control': 'no-store, no-cache, must-revalidate, max-age=0', 
   'Expires': '-1'}
cache_removal = [ k.lower() for k in cache_headers.keys() ]
cache_additions = cache_headers.items()

def is_hop_by_hop(header):
    """check if the given header is hop_by_hop"""
    return _hoppish.has_key(header.lower())


class IterativeResponse(object):

    def __init__(self, response_instance):
        self.response_instance = response_instance
        self.read_size = response_instance.length / 100

    def __iter__(self):
        yield self.response_instance.read(self.read_size)
        while self.response_instance.chunk_left is not None:
            if self.response_instance.chunk_left < self.read_size:
                yield self.response_instance.read()
                self.response_instance.chunk_left = None
            else:
                yield self.response_instance.read(self.read_size)

        return


def get_wsgi_response(response):
    if type(response) is str:
        return [response]
    else:
        if response.length > 512000:
            return IterativeResponse(response)
        return [response.read()]


def conditions_pass(e):
    for c in windmill.server.forwarding_conditions:
        if c(e) is False:
            return False

    return True


def proxy_post_redirect_form(environ, action):
    body = environ['wsgi.input'].read(int(environ['CONTENT_LENGTH']))
    parameters = body.split('&')
    inputs = []
    for parameter in parameters:
        parts = parameter.split('=', 1)
        if len(parts) == 1:
            continue
        parts = tuple(unicode(urllib.unquote(part), 'utf-8') for part in parts)
        inputs.append('<input type="hidden" name="%s" value="%s" />' % parts)

    form = '<html><head><title>There is no spoon.</title></head>\n<body onload="document.getElementById(\'redirect\').submit();"\n      style="text-align: center;">\n  <form id="redirect" action="%s" method="POST">%s</form>\n</body></html>' % (action, ('\n').join(inputs))
    return form.encode('utf-8')


forward_forms = {}

class WindmillProxyApplication(object):
    """Application to handle requests that need to be proxied"""

    def __init__(self):
        self.fmgr = None
        proxyInstances.append(self)
        return

    ConnectionClass = HTTPConnection

    def handler(self, environ, start_response):
        """Proxy for requests to the actual http server"""
        url = urlparse(environ['reconstructed_url'])
        referer = environ.get('HTTP_REFERER', None)
        test_url = windmill.settings['FORWARDING_TEST_URL']
        if self.fmgr is None and windmill.settings['FORWARDING_TEST_URL'] is not None:
            self.fmgr = ForwardManager(test_url)
        if windmill.settings['FORWARDING_TEST_URL'] is not None and not url.netloc.startswith('127.0.0.1') and not url.netloc.startswith('127.0.0.1') and conditions_pass(environ):
            url = urlparse(environ['reconstructed_url'])
            test_target = urlparse(test_url)
            if self.fmgr.is_static_forwarded(url):
                environ = self.fmgr.forward(url, environ)
                url = self.fmgr.forward_map(url)
            else:
                if url.scheme + '://' + url.netloc != test_target.scheme + '://' + test_target.netloc:
                    environ = self.fmgr.forward(url, environ)
                    redirect_url = self.fmgr.forward_map(url).geturl()
                    if environ['REQUEST_METHOD'] == 'POST':
                        form = proxy_post_redirect_form(environ, redirect_url)
                        forward_forms[redirect_url] = form
                    start_response('302 Found', [('Location', redirect_url)] + cache_additions)
                    logger.debug('Domain change, forwarded to ' + redirect_url)
                    return [
                     '']
                if url.geturl() in forward_forms:
                    response = forward_forms[url.geturl()]
                    length = str(len(response))
                    start_response('200 Ok', [('Content-Type', 'text/html'),
                     (
                      'Content-Length', length)] + cache_additions)
                    del forward_forms[url.geturl()]
                    return [
                     response]
                if self.fmgr.is_forward_mapped(url):
                    orig_url = self.fmgr.forward_unmap(url)
                    environ = self.fmgr.change_environ_domain(url, orig_url, environ)
                    url = orig_url
                elif not self.fmgr.is_forward_mapped(url) and referer is not None and self.fmgr.is_forward_mapped(urlparse(referer)):
                    orig_referer = self.fmgr.forward_unmap(urlparse(referer))
                    orig_url = self.fmgr.forward_to(url, orig_referer)
                    environ = self.fmgr.change_environ_domain(url, orig_url, environ)
                    url = orig_url
                    self.fmgr.forward(orig_url, {})

        def make_remote_connection(url, environ):
            try:
                connection = self.get_connection(url)
                path = url.geturl().replace(url.scheme + '://' + url.netloc, '')
            except Exception, e:
                logger.exception('Could not Connect')
                return [('501 Gateway error', [('Content-Type', 'text/html')]),
                 '<H1>Could not connect:</H1><pre>%s</pre>' % (str(e),)]
            else:
                body = None
                if environ.has_key('body'):
                    body = environ['body']
                elif environ.get('CONTENT_LENGTH'):
                    length = int(environ['CONTENT_LENGTH'])
                    body = environ['wsgi.input'].read(length)
                    environ['body'] = body
                headers = {}
                logger.debug('Environ ; %s' % str(environ))
                for key in environ.keys():
                    if key.startswith('HTTP_'):
                        value = environ[key]
                        key = key.replace('HTTP_', '', 1).swapcase().replace('_', '-')
                        if is_hop_by_hop(key) is False:
                            headers[key] = value
                        if key.lower() == 'location':
                            if '/windmill-serv' in value:
                                value = value.split('/windmill-serv')[0]

                if environ.get('CONTENT_TYPE'):
                    headers['content-type'] = environ['CONTENT_TYPE']
                if not headers.has_key('host'):
                    headers['host'] = environ['SERVER_NAME']
                try:
                    logger.debug('%s %s %s' % (environ['REQUEST_METHOD'], path,
                     str(headers)))
                    connection.request(environ['REQUEST_METHOD'], path, body=body, headers=headers)
                    connection.url = url
                    return connection
                except Exception, e:
                    return [('501 Gateway error', [('Content-Type', 'text/html')]),
                     '<H1>Could not make request:</H1><pre>%s</pre>' % (str(e),)]

            return

        def retry_known_hosts(url, environ):
            if self.fmgr is None:
                return
            else:
                for host in self.fmgr.known_hosts():
                    orig_url = self.fmgr.forward_to(url, host)
                    new_environ = self.fmgr.change_environ_domain(self.fmgr.forward_map(orig_url), orig_url, environ)
                    connection = make_remote_connection(orig_url, new_environ)
                    if isinstance(connection, HTTPConnection):
                        try:
                            new_response = connection.getresponse()
                        except:
                            return
                        else:
                            if new_response.status > 199 and new_response.status < 399:
                                logger.info('Retry success, ' + url.geturl() + ' to ' + host.geturl())
                                new_response.url = connection.url
                                return new_response

                return

        connection = make_remote_connection(url, environ)
        if isinstance(connection, HTTPConnection):
            response = connection.getresponse()
            response.url = connection.url
        if environ['REQUEST_METHOD'] == 'POST':
            threshold = 399
        else:
            threshold = 399
        if not isinstance(connection, HTTPConnection) or response.status > threshold:
            new_response = retry_known_hosts(url, environ)
            if new_response is not None:
                response = new_response
            elif not isinstance(connection, HTTPConnection):
                status = connection[0][0]
                headers = connection[0][1]
                body = connection[1]
                for header in copy.copy(headers):
                    if header[0].lower() == 'content-length':
                        body.length = int(header[1].strip())
                    if header[0].lower() in cache_removal:
                        headers.remove(header)

                start_response(status, headers + cache_additions)
                return get_wsgi_response(body)
        headers = self.parse_headers(response)
        if response.status == 404:
            logger.info('Could not fullfill proxy request to ' + url.geturl())
        for header in copy.copy(headers):
            if header[0].lower() == 'content-length':
                response.length = int(header[1].strip())
            if header[0].lower() in cache_removal:
                headers.remove(header)

        start_response(response.status.__str__() + ' ' + response.reason, headers + cache_additions)
        return get_wsgi_response(response)

    def parse_headers(self, response):
        headers = [ (x.lower(), y) for (x, y) in [ z.split(':', 1) for z in str(response.msg).splitlines() if ':' in z
                                                 ]
                  ]
        for header in headers:
            if is_hop_by_hop(header[0]):
                headers.remove(header)
            elif header[0] == 'location':
                if '/windmill-serv' in header[1]:
                    i = headers.index(header)
                    location = header[1]
                    headers.remove(header)
                    headers.insert(i, ('location',
                     location.split('/windmill-serv')[0]))

        return headers

    def get_connection(self, url):
        """ Factory method for connections """
        connection = self.ConnectionClass(url.netloc)
        return connection

    def clearForwardingRegistry(self):
        if self.fmgr is not None:
            self.fmgr.clear()
        return

    def __call__(self, environ, start_response):
        return self.handler(environ, start_response)


proxyInstances = []

def clearForwardingRegistry():
    for p in proxyInstances:
        p.clearForwardingRegistry()