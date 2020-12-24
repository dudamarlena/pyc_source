# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/swaggerpy/http_client.py
# Compiled at: 2016-11-21 09:04:54
# Size of source mod 2**32: 6675 bytes
"""HTTP client abstractions.
"""
import logging, requests, requests.auth, urllib.parse, websocket
log = logging.getLogger(__name__)

class HttpClient(object):
    __doc__ = 'Interface for a minimal HTTP client.\n    '

    def close(self):
        """Close this client resource.
        """
        raise NotImplementedError('%s: Method not implemented', self.__class__.__name__)

    def request(self, method, url, params=None, data=None):
        """Issue an HTTP request.

        :param method: HTTP method (GET, POST, DELETE, etc.)
        :type  method: str
        :param url: URL to request
        :type  url: str
        :param params: Query parameters (?key=value)
        :type  params: dict
        :param data: Request body
        :type  data: Dictionary, bytes, or file-like object
        :return: Implementation specific response object
        """
        raise NotImplementedError('%s: Method not implemented', self.__class__.__name__)

    def ws_connect(self, url, params=None):
        """Create a WebSocket connection.

        :param url: WebSocket URL.
        :type  url: str
        :param params: Query parameters (?key=value)
        :type  params: dict
        :return: Implmentation specific WebSocket connection object
        """
        raise NotImplementedError('%s: Method not implemented', self.__class__.__name__)

    def set_basic_auth(self, host, username, password):
        """Configures client to use HTTP Basic authentication.

        :param host: Hostname to limit authentication to.
        :param username: Username
        :param password: Password
        """
        raise NotImplementedError('%s: Method not implemented', self.__class__.__name__)

    def set_api_key(self, host, api_key, param_name='api_key'):
        """Configures client to use api_key authentication.

        The api_key is added to every query parameter sent.

        :param host: Hostname to limit authentication to.
        :param api_key: Value for api_key.
        :param param_name: Parameter name to use in query string.
        """
        raise NotImplementedError('%s: Method not implemented', self.__class__.__name__)


class Authenticator(object):
    __doc__ = 'Authenticates requests.\n\n    :param host: Host to authenticate for.\n    '

    def __init__(self, host):
        self.host = host

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self.host)

    def matches(self, url):
        """Returns true if this authenticator applies to the given url.

        :param url: URL to check.
        :return: True if matches host, port and scheme, False otherwise.
        """
        split = urllib.parse.urlsplit(url)
        return self.host == split.hostname

    def apply(self, request):
        """Apply authentication to a request.

        :param request: Request to add authentication information to.
        """
        raise NotImplementedError('%s: Method not implemented', self.__class__.__name__)


class BasicAuthenticator(Authenticator):
    __doc__ = 'HTTP Basic authenticator.\n\n    :param host: Host to authenticate for.\n    :param username: Username.\n    :param password: Password\n    '

    def __init__(self, host, username, password):
        super(BasicAuthenticator, self).__init__(host)
        self.auth = requests.auth.HTTPBasicAuth(username, password)

    def apply(self, request):
        request.auth = self.auth


class ApiKeyAuthenticator(Authenticator):
    __doc__ = '?api_key authenticator.\n\n    This authenticator adds a query parameter to specify an API key.\n\n    :param host: Host to authenticate for.\n    :param api_key: API key.\n    :param param_name: Query parameter specifying the API key.\n    '

    def __init__(self, host, api_key, param_name='api_key'):
        super(ApiKeyAuthenticator, self).__init__(host)
        self.param_name = param_name
        self.api_key = api_key

    def apply(self, request):
        request.params[self.param_name] = self.api_key


class SynchronousHttpClient(HttpClient):
    __doc__ = 'Synchronous HTTP client implementation.\n    '

    def __init__(self):
        self.session = requests.Session()
        self.authenticator = None
        self.websockets = set()

    def close(self):
        self.session.close()

    def set_basic_auth(self, host, username, password):
        self.authenticator = BasicAuthenticator(host=host, username=username, password=password)

    def set_api_key(self, host, api_key, param_name='api_key'):
        self.authenticator = ApiKeyAuthenticator(host=host, api_key=api_key, param_name=param_name)

    def request(self, method, url, params=None, data=None, headers=None):
        """Requests based implementation.

        :return: Requests response
        :rtype:  requests.Response
        """
        req = requests.Request(method=method, url=url, params=params, data=data, headers=headers)
        self.apply_authentication(req)
        return self.session.send(self.session.prepare_request(req))

    def ws_connect(self, url, params=None):
        """Websocket-client based implementation.

        :return: WebSocket connection
        :rtype:  websocket.WebSocket
        """
        proto_req = requests.Request('GET', url, params=params)
        self.apply_authentication(proto_req)
        preped_req = proto_req.prepare()
        header = ['%s: %s' % (k, v) for k, v in list(preped_req.headers.items()) if k == 'Authorization']
        url = preped_req.url
        if params:
            joined_params = '&'.join(['%s=%s' % (k, v) for k, v in list(params.items())])
            url += '?%s' % joined_params
        return websocket.create_connection(url, header=header)

    def apply_authentication(self, req):
        if self.authenticator and self.authenticator.matches(req.url):
            self.authenticator.apply(req)