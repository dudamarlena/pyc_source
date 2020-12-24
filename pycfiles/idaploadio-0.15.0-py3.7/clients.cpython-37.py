# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/idapload/clients.py
# Compiled at: 2020-04-15 05:31:36
# Size of source mod 2**32: 12313 bytes
import re, time, requests
from requests import Request, Response
from requests.auth import HTTPBasicAuth
from requests.exceptions import InvalidSchema, InvalidURL, MissingSchema, RequestException
from urllib.parse import urlparse, urlunparse
from .exception import CatchResponseError, ResponseError
absolute_http_url_regexp = re.compile('^https?://', re.I)

class LocustResponse(Response):

    def raise_for_status(self):
        if hasattr(self, 'error'):
            if self.error:
                raise self.error
        Response.raise_for_status(self)


class HttpSession(requests.Session):
    __doc__ = "\n    Class for performing web requests and holding (session-) cookies between requests (in order\n    to be able to log in and out of websites). Each request is logged so that idapload can display \n    statistics.\n    \n    This is a slightly extended version of `python-request <http://python-requests.org>`_'s\n    :py:class:`requests.Session` class and mostly this class works exactly the same. However \n    the methods for making requests (get, post, delete, put, head, options, patch, request) \n    can now take a *url* argument that's only the path part of the URL, in which case the host \n    part of the URL will be prepended with the HttpSession.base_url which is normally inherited\n    from a Locust class' host property.\n    \n    Each of the methods for making requests also takes two additional optional arguments which \n    are Locust specific and doesn't exist in python-requests. These are:\n    \n    :param name: (optional) An argument that can be specified to use as label in Locust's statistics instead of the URL path. \n                 This can be used to group different URL's that are requested into a single entry in Locust's statistics.\n    :param catch_response: (optional) Boolean argument that, if set, can be used to make a request return a context manager \n                           to work as argument to a with statement. This will allow the request to be marked as a fail based on the content of the \n                           response, even if the response code is ok (2xx). The opposite also works, one can use catch_response to catch a request\n                           and then mark it as successful even if the response code was not (i.e 500 or 404).\n    "

    def __init__(self, base_url, request_success, request_failure, *args, **kwargs):
        (super(HttpSession, self).__init__)(*args, **kwargs)
        self.base_url = base_url
        self.request_success = request_success
        self.request_failure = request_failure
        parsed_url = urlparse(self.base_url)
        if parsed_url.username:
            if parsed_url.password:
                netloc = parsed_url.hostname
                if parsed_url.port:
                    netloc += ':%d' % parsed_url.port
                self.base_url = urlunparse((parsed_url.scheme, netloc, parsed_url.path, parsed_url.params, parsed_url.query, parsed_url.fragment))
                self.auth = HTTPBasicAuth(parsed_url.username, parsed_url.password)

    def _build_url(self, path):
        """ prepend url with hostname unless it's already an absolute URL """
        if absolute_http_url_regexp.match(path):
            return path
        return '%s%s' % (self.base_url, path)

    def request(self, method, url, name=None, catch_response=False, **kwargs):
        """
        Constructs and sends a :py:class:`requests.Request`.
        Returns :py:class:`requests.Response` object.

        :param method: method for the new :class:`Request` object.
        :param url: URL for the new :class:`Request` object.
        :param name: (optional) An argument that can be specified to use as label in Locust's statistics instead of the URL path. 
          This can be used to group different URL's that are requested into a single entry in Locust's statistics.
        :param catch_response: (optional) Boolean argument that, if set, can be used to make a request return a context manager 
          to work as argument to a with statement. This will allow the request to be marked as a fail based on the content of the 
          response, even if the response code is ok (2xx). The opposite also works, one can use catch_response to catch a request
          and then mark it as successful even if the response code was not (i.e 500 or 404).
        :param params: (optional) Dictionary or bytes to be sent in the query string for the :class:`Request`.
        :param data: (optional) Dictionary or bytes to send in the body of the :class:`Request`.
        :param headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
        :param cookies: (optional) Dict or CookieJar object to send with the :class:`Request`.
        :param files: (optional) Dictionary of ``'filename': file-like-objects`` for multipart encoding upload.
        :param auth: (optional) Auth tuple or callable to enable Basic/Digest/Custom HTTP Auth.
        :param timeout: (optional) How long in seconds to wait for the server to send data before giving up, as a float, 
            or a (`connect timeout, read timeout <user/advanced.html#timeouts>`_) tuple.
        :type timeout: float or tuple
        :param allow_redirects: (optional) Set to True by default.
        :type allow_redirects: bool
        :param proxies: (optional) Dictionary mapping protocol to the URL of the proxy.
        :param stream: (optional) whether to immediately download the response content. Defaults to ``False``.
        :param verify: (optional) if ``True``, the SSL cert will be verified. A CA_BUNDLE path can also be provided.
        :param cert: (optional) if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair.
        """
        url = self._build_url(url)
        request_meta = {}
        request_meta['method'] = method
        request_meta['start_time'] = time.time()
        response = (self._send_request_safe_mode)(method, url, **kwargs)
        request_meta['response_time'] = (time.time() - request_meta['start_time']) * 1000
        request_meta['name'] = name or (response.history and response.history[0] or response).request.path_url
        if kwargs.get('stream', False):
            request_meta['content_size'] = int(response.headers.get('content-length') or 0)
        else:
            request_meta['content_size'] = len(response.content or b'')
        if catch_response:
            response.idapload_request_meta = request_meta
            return ResponseContextManager(response, request_success=(self.request_success), request_failure=(self.request_failure))
        if name:
            orig_url = response.url
            response.url = name
        try:
            response.raise_for_status()
        except RequestException as e:
            try:
                self.request_failure.fire(request_type=(request_meta['method']),
                  name=(request_meta['name']),
                  response_time=(request_meta['response_time']),
                  response_length=(request_meta['content_size']),
                  exception=e)
            finally:
                e = None
                del e

        else:
            self.request_success.fire(request_type=(request_meta['method']),
              name=(request_meta['name']),
              response_time=(request_meta['response_time']),
              response_length=(request_meta['content_size']))
        if name:
            response.url = orig_url
        return response

    def _send_request_safe_mode(self, method, url, **kwargs):
        """
        Send an HTTP request, and catch any exception that might occur due to connection problems.
        
        Safe mode has been removed from requests 1.x.
        """
        try:
            return (requests.Session.request)(self, method, url, **kwargs)
        except (MissingSchema, InvalidSchema, InvalidURL):
            raise
        except RequestException as e:
            try:
                r = LocustResponse()
                r.error = e
                r.status_code = 0
                r.request = Request(method, url).prepare()
                return r
            finally:
                e = None
                del e


class ResponseContextManager(LocustResponse):
    __doc__ = "\n    A Response class that also acts as a context manager that provides the ability to manually \n    control if an HTTP request should be marked as successful or a failure in Locust's statistics\n    \n    This class is a subclass of :py:class:`Response <requests.Response>` with two additional \n    methods: :py:meth:`success <idapload.clients.ResponseContextManager.success>` and \n    :py:meth:`failure <idapload.clients.ResponseContextManager.failure>`.\n    "
    _is_reported = False

    def __init__(self, response, request_success, request_failure):
        self.__dict__ = response.__dict__
        self._request_success = request_success
        self._request_failure = request_failure

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
            except requests.exceptions.RequestException as e:
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
        self._request_success.fire(request_type=(self.idapload_request_meta['method']),
          name=(self.idapload_request_meta['name']),
          response_time=(self.idapload_request_meta['response_time']),
          response_length=(self.idapload_request_meta['content_size']))
        self._is_reported = True

    def failure(self, exc):
        """
        Report the response as a failure.
        
        exc can be either a python exception, or a string in which case it will
        be wrapped inside a CatchResponseError. 
        
        Example::
        
            with self.client.get("/", catch_response=True) as response:
                if response.content == b"":
                    response.failure("No data")
        """
        if isinstance(exc, str):
            exc = CatchResponseError(exc)
        self._request_failure.fire(request_type=(self.idapload_request_meta['method']),
          name=(self.idapload_request_meta['name']),
          response_time=(self.idapload_request_meta['response_time']),
          response_length=(self.idapload_request_meta['content_size']),
          exception=exc)
        self._is_reported = True