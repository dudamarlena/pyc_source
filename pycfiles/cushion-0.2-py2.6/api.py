# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/cushion/api.py
# Compiled at: 2011-01-25 23:43:05
import httplib2, base64, functools, simplejson as json
from urllib import urlencode

class Cushion(object):
    """
    Cushion is the primary interface to CouchDB
    """

    def __init__(self, base_uri, **kwargs):
        self.base_uri = base_uri
        self.username = kwargs.get('username', None)
        self.password = kwargs.get('password', None)
        self.timeout = kwargs.get('timeout', None)
        return

    def _get_request_builder(self):
        return RequestBuilder(self.username, self.password, self.base_uri, self.timeout)

    def __getattr__(self, name):
        return Part([
         name], self._get_request_builder())


class RequestBuilder(object):
    """
    RequestBuilder is responsible for building
    the http request based on the http method type
    and URL that is being accessed
    """

    def __init__(self, username, password, base_uri, timeout):
        self.username = username
        self.password = password
        self.http_client = httplib2.Http(timeout=timeout)
        self.base_uri = base_uri

    def create_auth_header(self):
        if self.username and self.password:
            base64string = base64.b64encode('%s:%s' % (
             self.username, self.password))
            header = 'Basic %s' % (base64string,)
            return dict(Authorization=header)
        else:
            return dict()

    def build(self, uri_parts, options):
        """
        Build the request, returns callable which in turn
        returns the http response and the http content body
        """
        if len(uri_parts):
            method = uri_parts[0].upper()
        headers = self.create_auth_header()
        the_parts = [self.base_uri]
        the_parts.extend(uri_parts[1:])
        if method == 'GET':
            headers.update({'Accept': 'application/json'})
            make_request = functools.partial(self.http_client.request, headers=headers)
            return ReadDocumentRequest(make_request, method, the_parts, options)
        else:
            headers = {'Content-Type': 'application/json'}
            make_request = functools.partial(self.http_client.request, headers=headers)
            return WriteDocumentRequest(make_request, method, the_parts, options)


class WriteDocumentRequest(object):

    def __init__(self, requestor, method, uri_parts, options=None):
        self.requestor = requestor
        self.uri_parts = uri_parts
        self.method = method
        self.options = dict()
        if options:
            self.options = options

    @property
    def uri(self):
        elements = []
        for part in self.uri_parts:
            elements.append(part)

        if self.method in ('PUT', 'DELETE'):
            elements.append(self.options.get('id', ''))
        uri = ('/').join(elements)
        if self.method == 'DELETE':
            return uri + '?%s' % urlencode(self.options)
        else:
            return uri

    def __call__(self):
        if self.method == 'PUT' or self.method == 'DELETE':
            body = dict([ (k, v) for (k, v) in self.options.iteritems() if k != 'id' ])
        else:
            body = self.options
        return self.requestor(self.uri, self.method, body=json.dumps(body))


class ReadDocumentRequest(object):

    def __init__(self, requestor, method, uri_parts, options=None):
        self.requestor = requestor
        self.method = method
        self.uri_parts = uri_parts
        self.options = dict()
        if options:
            self.options = options

    @property
    def uri(self):
        """Create the URI with the parameters"""
        elements = []
        for part in self.uri_parts:
            elements.append(part)

        if not self.uri_parts[(-1)].startswith('_'):
            elements.append(self.options.get('id', ''))
            del self.options['id']
        uri = ('/').join(elements)
        if len(self.options):
            if self.options.has_key('startkey'):
                self.options['startkey'] = '"' + self.options['startkey'] + '"'
            uri = uri + '?%s' % urlencode(self.options)
        return uri

    def __call__(self):
        return self.requestor(self.uri, 'GET')


class Part(object):

    def __init__(self, parts, request_builder):
        self.parts = parts
        self.request_builder = request_builder

    def __call__(self, **kwargs):
        request = self.request_builder.build(self.parts, kwargs)
        (response, content) = request()
        status = int(response['status'])
        if status < 200 or status >= 300:
            raise ValueError, 'Invalid return code. %s' % (str(response),)
        else:
            return json.loads(content)

    def __getattr__(self, name):
        return Part(self.parts + [name], self.request_builder)