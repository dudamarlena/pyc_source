# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/idapload/contrib/fasthttp.py
# Compiled at: 2020-04-13 02:37:12
# Size of source mod 2**32: 16174 bytes
from __future__ import absolute_import
import re, socket, json
from base64 import b64encode
from urllib.parse import urlparse, urlunparse
from ssl import SSLError
from timeit import default_timer
from http.cookiejar import CookieJar
import gevent
from gevent.timeout import Timeout
from geventhttpclient.useragent import UserAgent, CompatRequest, CompatResponse, ConnectionError
from geventhttpclient.response import HTTPConnectionClosed
from locust.core import Locust
from locust.exception import LocustError, CatchResponseError, ResponseError
CompatRequest.unverifiable = False
CompatRequest.type = 'https'
absolute_http_url_regexp = re.compile('^https?://', re.I)
FAILURE_EXCEPTIONS = (
 ConnectionError, ConnectionRefusedError, socket.error,
 SSLError, Timeout, HTTPConnectionClosed)

def _construct_basic_auth_str(username, password):
    """Construct Authorization header value to be used in HTTP Basic Auth"""
    if isinstance(username, str):
        username = username.encode('latin1')
    if isinstance(password, str):
        password = password.encode('latin1')
    return 'Basic ' + b64encode((b':').join((username, password))).strip().decode('ascii')


class FastHttpLocust(Locust):
    __doc__ = '\n    Represents an HTTP "user" which is to be hatched and attack the system that is to be load tested.\n    \n    The behaviour of this user is defined by the task_set attribute, which should point to a \n    :py:class:`TaskSet <locust.core.TaskSet>` class.\n    \n    This class creates a *client* attribute on instantiation which is an HTTP client with support \n    for keeping a user session between requests.\n    '
    client = None

    def __init__(self, environment):
        super().__init__(environment)
        if self.host is None:
            raise LocustError('You must specify the base host. Either in the host attribute in the Locust class, or on the command line using the --host option.')
        if not re.match('^https?://[^/]+', self.host, re.I):
            raise LocustError('Invalid host (`%s`), must be a valid base URL. E.g. http://example.com' % self.host)
        self.client = FastHttpSession((self.environment), base_url=(self.host))


class FastHttpSession(object):
    auth_header = None

    def __init__(self, environment, base_url, **kwargs):
        self.environment = environment
        self.base_url = base_url
        self.cookiejar = CookieJar()
        self.client = LocustUserAgent(max_retries=1, 
         cookiejar=self.cookiejar, 
         insecure=True, 
         ssl_options={'cert_reqs': gevent.ssl.CERT_NONE}, **kwargs)
        parsed_url = urlparse(self.base_url)
        if parsed_url.username:
            if parsed_url.password:
                netloc = parsed_url.hostname
                if parsed_url.port:
                    netloc += ':%d' % parsed_url.port
                self.base_url = urlunparse((parsed_url.scheme, netloc, parsed_url.path, parsed_url.params, parsed_url.query, parsed_url.fragment))
                self.auth_header = _construct_basic_auth_str(parsed_url.username, parsed_url.password)

    def _build_url(self, path):
        """ prepend url with hostname unless it's already an absolute URL """
        if absolute_http_url_regexp.match(path):
            return path
        return '%s%s' % (self.base_url, path)

    def _send_request_safe_mode(self, method, url, **kwargs):
        """
        Send an HTTP request, and catch any exception that might occur due to either 
        connection problems, or invalid HTTP status codes
        """
        try:
            return (self.client.urlopen)(url, method=method, **kwargs)
        except FAILURE_EXCEPTIONS as e:
            try:
                if hasattr(e, 'response'):
                    r = e.response
                else:
                    r = ErrorResponse()
                r.error = e
                return r
            finally:
                e = None
                del e

    def request(self, method, path, name=None, data=None, catch_response=False, stream=False, headers=None, auth=None, **kwargs):
        """
        Send and HTTP request
        Returns :py:class:`locust.contrib.fasthttp.FastResponse` object.

        :param method: method for the new :class:`Request` object.
        :param path: Path that will be concatenated with the base host URL that has been specified.
            Can also be a full URL, in which case the full URL will be requested, and the base host 
            is ignored.
        :param name: (optional) An argument that can be specified to use as label in Locust's 
            statistics instead of the URL path. This can be used to group different URL's 
            that are requested into a single entry in Locust's statistics.
        :param catch_response: (optional) Boolean argument that, if set, can be used to make a request 
            return a context manager to work as argument to a with statement. This will allow the 
            request to be marked as a fail based on the content of the response, even if the response 
            code is ok (2xx). The opposite also works, one can use catch_response to catch a request 
            and then mark it as successful even if the response code was not (i.e 500 or 404).
        :param data: (optional) Dictionary or bytes to send in the body of the request.
        :param headers: (optional) Dictionary of HTTP Headers to send with the request.
        :param auth: (optional) Auth (username, password) tuple to enable Basic HTTP Auth.
        :param stream: (optional) If set to true the response body will not be consumed immediately 
            and can instead be consumed by accessing the stream attribute on the Response object.
            Another side effect of setting stream to True is that the time for downloading the response 
            content will not be accounted for in the request time that is reported by Locust.
        """
        url = self._build_url(path)
        request_meta = {}
        request_meta['method'] = method
        request_meta['start_time'] = default_timer()
        request_meta['name'] = name or path
        headers = headers or {}
        if auth:
            headers['Authorization'] = _construct_basic_auth_str(auth[0], auth[1])
        else:
            if self.auth_header:
                headers['Authorization'] = self.auth_header
            else:
                if 'Accept-Encoding' not in headers:
                    headers['Accept-Encoding'] = 'gzip, deflate'
                else:
                    response = (self._send_request_safe_mode)(method, url, payload=data, headers=headers, **kwargs)
                    if stream:
                        request_meta['content_size'] = int(response.headers.get('content-length') or 0)
                    else:
                        request_meta['content_size'] = len(response.content or '')
                request_meta['response_time'] = int((default_timer() - request_meta['start_time']) * 1000)
                if catch_response:
                    response.locust_request_meta = request_meta
                    return ResponseContextManager(response, environment=(self.environment))
                try:
                    response.raise_for_status()
                except FAILURE_EXCEPTIONS as e:
                    try:
                        self.environment.events.request_failure.fire(request_type=(request_meta['method']),
                          name=(request_meta['name']),
                          response_time=(request_meta['response_time']),
                          response_length=(request_meta['content_size']),
                          exception=e)
                    finally:
                        e = None
                        del e

                else:
                    self.environment.events.request_success.fire(request_type=(request_meta['method']),
                      name=(request_meta['name']),
                      response_time=(request_meta['response_time']),
                      response_length=(request_meta['content_size']))
            return response

    def delete(self, path, **kwargs):
        return (self.request)('DELETE', path, **kwargs)

    def get(self, path, **kwargs):
        """Sends a GET request"""
        return (self.request)('GET', path, **kwargs)

    def head(self, path, **kwargs):
        """Sends a HEAD request"""
        return (self.request)('HEAD', path, **kwargs)

    def options(self, path, **kwargs):
        """Sends a OPTIONS request"""
        return (self.request)('OPTIONS', path, **kwargs)

    def patch(self, path, data=None, **kwargs):
        """Sends a POST request"""
        return (self.request)('PATCH', path, data=data, **kwargs)

    def post(self, path, data=None, **kwargs):
        """Sends a POST request"""
        return (self.request)('POST', path, data=data, **kwargs)

    def put(self, path, data=None, **kwargs):
        """Sends a PUT request"""
        return (self.request)('PUT', path, data=data, **kwargs)


class FastResponse(CompatResponse):
    headers = None
    _response = None
    encoding = None

    @property
    def text(self):
        """
        Returns the text content of the response as a decoded string
        """
        if self.content is None:
            return
            if self.encoding is None:
                if self.headers is None:
                    self.encoding = 'utf-8'
        else:
            self.encoding = self.headers.get('content-type', '').partition('charset=')[2] or 'utf-8'
        return str((self.content), (self.encoding), errors='replace')

    def json(self):
        return json.loads(self.text)

    def raise_for_status(self):
        """Raise any connection errors that occured during the request"""
        if hasattr(self, 'error'):
            if self.error:
                raise self.error

    @property
    def status_code(self):
        """
        We override status_code in order to return None if no valid response was 
        returned. E.g. in the case of connection errors
        """
        return self._response is not None and self._response.get_code() or 0

    def _content(self):
        if self.headers is None:
            return
        return super(FastResponse, self)._content()


class ErrorResponse(object):
    __doc__ = "\n    This is used as a dummy response object when geventhttpclient raises an error \n    that doesn't have a real Response object attached. E.g. a socket error or similar\n    "
    headers = None
    content = None
    status_code = 0
    error = None
    text = None

    def raise_for_status(self):
        raise self.error


class LocustUserAgent(UserAgent):
    response_type = FastResponse
    valid_response_codes = frozenset([200, 201, 202, 203, 204, 205, 206, 207, 208, 226, 301, 302, 303, 307])

    def __init__(self, **kwargs):
        (super(LocustUserAgent, self).__init__)(network_timeout=60.0, connection_timeout=60.0, **kwargs)

    def _urlopen(self, request):
        """Override _urlopen() in order to make it use the response_type attribute"""
        client = self.clientpool.get_client(request.url_split)
        resp = client.request((request.method), (request.url_split.request_uri), body=(request.payload),
          headers=(request.headers))
        return self.response_type(resp, request=request, sent_request=(resp._sent_request))


class ResponseContextManager(FastResponse):
    __doc__ = "\n    A Response class that also acts as a context manager that provides the ability to manually \n    control if an HTTP request should be marked as successful or a failure in Locust's statistics\n    \n    This class is a subclass of :py:class:`FastResponse <locust.contrib.fasthttp.FastResponse>` \n    with two additional methods: :py:meth:`success <locust.contrib.fasthttp.ResponseContextManager.success>`\n    and :py:meth:`failure <locust.contrib.fasthttp.ResponseContextManager.failure>`.\n    "
    _is_reported = False

    def __init__(self, response, environment):
        self.__dict__ = response.__dict__
        self._cached_content = response.content
        self.environment = environment

    def __enter__(self):
        return self

    def __exit__(self, exc, value, traceback):
        if self._is_reported:
            return exc is None
        if exc:
            if isinstance(value, ResponseError):
                self.failure(value)
            else:
                return False
        else:
            try:
                self.raise_for_status()
            except FAILURE_EXCEPTIONS as e:
                try:
                    self.failure(e)
                finally:
                    e = None
                    del e

            else:
                self.success()
        return True

    def success(self):
        """
        Report the response as successful
        
        Example::
        
            with self.client.get("/does/not/exist", catch_response=True) as response:
                if response.status_code == 404:
                    response.success()
        """
        self.environment.events.request_success.fire(request_type=(self.locust_request_meta['method']),
          name=(self.locust_request_meta['name']),
          response_time=(self.locust_request_meta['response_time']),
          response_length=(self.locust_request_meta['content_size']))
        self._is_reported = True

    def failure(self, exc):
        """
        Report the response as a failure.
        
        exc can be either a python exception, or a string in which case it will
        be wrapped inside a CatchResponseError. 
        
        Example::
        
            with self.client.get("/", catch_response=True) as response:
                if response.content == "":
                    response.failure("No data")
        """
        if isinstance(exc, str):
            exc = CatchResponseError(exc)
        self.environment.events.request_failure.fire(request_type=(self.locust_request_meta['method']),
          name=(self.locust_request_meta['name']),
          response_time=(self.locust_request_meta['response_time']),
          response_length=(self.locust_request_meta['content_size']),
          exception=exc)
        self._is_reported = True