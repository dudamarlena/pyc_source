# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/test/client.py
# Compiled at: 2019-02-14 00:35:17
from __future__ import unicode_literals
import json, mimetypes, os, re, sys
from copy import copy
from importlib import import_module
from io import BytesIO
from django.conf import settings
from django.core.handlers.base import BaseHandler
from django.core.handlers.wsgi import ISO_8859_1, UTF_8, WSGIRequest
from django.core.signals import got_request_exception, request_finished, request_started
from django.db import close_old_connections
from django.http import HttpRequest, QueryDict, SimpleCookie
from django.template import TemplateDoesNotExist
from django.test import signals
from django.test.utils import ContextList
from django.urls import resolve
from django.utils import six
from django.utils.encoding import force_bytes, force_str, uri_to_iri
from django.utils.functional import SimpleLazyObject, curry
from django.utils.http import urlencode
from django.utils.itercompat import is_iterable
from django.utils.six.moves.urllib.parse import urljoin, urlparse, urlsplit
__all__ = ('Client', 'RedirectCycleError', 'RequestFactory', 'encode_file', 'encode_multipart')
BOUNDARY = b'BoUnDaRyStRiNg'
MULTIPART_CONTENT = b'multipart/form-data; boundary=%s' % BOUNDARY
CONTENT_TYPE_RE = re.compile(b'.*; charset=([\\w\\d-]+);?')
JSON_CONTENT_TYPE_RE = re.compile(b'^application\\/(vnd\\..+\\+)?json')

class RedirectCycleError(Exception):
    """
    The test client has been asked to follow a redirect loop.
    """

    def __init__(self, message, last_response):
        super(RedirectCycleError, self).__init__(message)
        self.last_response = last_response
        self.redirect_chain = last_response.redirect_chain


class FakePayload(object):
    """
    A wrapper around BytesIO that restricts what can be read since data from
    the network can't be seeked and cannot be read outside of its content
    length. This makes sure that views can't do anything under the test client
    that wouldn't work in Real Life.
    """

    def __init__(self, content=None):
        self.__content = BytesIO()
        self.__len = 0
        self.read_started = False
        if content is not None:
            self.write(content)
        return

    def __len__(self):
        return self.__len

    def read(self, num_bytes=None):
        if not self.read_started:
            self.__content.seek(0)
            self.read_started = True
        if num_bytes is None:
            num_bytes = self.__len or 0
        assert self.__len >= num_bytes, b'Cannot read more than the available bytes from the HTTP incoming data.'
        content = self.__content.read(num_bytes)
        self.__len -= num_bytes
        return content

    def write(self, content):
        if self.read_started:
            raise ValueError(b"Unable to write a payload after he's been read")
        content = force_bytes(content)
        self.__content.write(content)
        self.__len += len(content)


def closing_iterator_wrapper(iterable, close):
    try:
        for item in iterable:
            yield item

    finally:
        request_finished.disconnect(close_old_connections)
        close()
        request_finished.connect(close_old_connections)


def conditional_content_removal(request, response):
    """
    Simulate the behavior of most Web servers by removing the content of
    responses for HEAD requests, 1xx, 204, and 304 responses. Ensures
    compliance with RFC 7230, section 3.3.3.
    """
    if 100 <= response.status_code < 200 or response.status_code in (204, 304):
        if response.streaming:
            response.streaming_content = []
        else:
            response.content = b''
        response[b'Content-Length'] = b'0'
    if request.method == b'HEAD':
        if response.streaming:
            response.streaming_content = []
        else:
            response.content = b''
    return response


class ClientHandler(BaseHandler):
    """
    A HTTP Handler that can be used for testing purposes. Uses the WSGI
    interface to compose requests, but returns the raw HttpResponse object with
    the originating WSGIRequest attached to its ``wsgi_request`` attribute.
    """

    def __init__(self, enforce_csrf_checks=True, *args, **kwargs):
        self.enforce_csrf_checks = enforce_csrf_checks
        super(ClientHandler, self).__init__(*args, **kwargs)

    def __call__(self, environ):
        if self._middleware_chain is None:
            self.load_middleware()
        request_started.disconnect(close_old_connections)
        request_started.send(sender=self.__class__, environ=environ)
        request_started.connect(close_old_connections)
        request = WSGIRequest(environ)
        request._dont_enforce_csrf_checks = not self.enforce_csrf_checks
        response = self.get_response(request)
        conditional_content_removal(request, response)
        response.wsgi_request = request
        if response.streaming:
            response.streaming_content = closing_iterator_wrapper(response.streaming_content, response.close)
        else:
            request_finished.disconnect(close_old_connections)
            response.close()
            request_finished.connect(close_old_connections)
        return response


def store_rendered_templates(store, signal, sender, template, context, **kwargs):
    """
    Stores templates and contexts that are rendered.

    The context is copied so that it is an accurate representation at the time
    of rendering.
    """
    store.setdefault(b'templates', []).append(template)
    if b'context' not in store:
        store[b'context'] = ContextList()
    store[b'context'].append(copy(context))


def encode_multipart(boundary, data):
    """
    Encodes multipart POST data from a dictionary of form values.

    The key will be used as the form data name; the value will be transmitted
    as content. If the value is a file, the contents of the file will be sent
    as an application/octet-stream; otherwise, str(value) will be sent.
    """
    lines = []

    def to_bytes(s):
        return force_bytes(s, settings.DEFAULT_CHARSET)

    def is_file(thing):
        return hasattr(thing, b'read') and callable(thing.read)

    for key, value in data.items():
        if is_file(value):
            lines.extend(encode_file(boundary, key, value))
        elif not isinstance(value, six.string_types) and is_iterable(value):
            for item in value:
                if is_file(item):
                    lines.extend(encode_file(boundary, key, item))
                else:
                    lines.extend(to_bytes(val) for val in [
                     b'--%s' % boundary,
                     b'Content-Disposition: form-data; name="%s"' % key,
                     b'',
                     item])

        else:
            lines.extend(to_bytes(val) for val in [
             b'--%s' % boundary,
             b'Content-Disposition: form-data; name="%s"' % key,
             b'',
             value])

    lines.extend([
     to_bytes(b'--%s--' % boundary),
     b''])
    return (b'\r\n').join(lines)


def encode_file(boundary, key, file):

    def to_bytes(s):
        return force_bytes(s, settings.DEFAULT_CHARSET)

    file_has_string_name = hasattr(file, b'name') and isinstance(file.name, six.string_types)
    filename = os.path.basename(file.name) if file_has_string_name else b''
    if hasattr(file, b'content_type'):
        content_type = file.content_type
    elif filename:
        content_type = mimetypes.guess_type(filename)[0]
    else:
        content_type = None
    if content_type is None:
        content_type = b'application/octet-stream'
    if not filename:
        filename = key
    return [to_bytes(b'--%s' % boundary),
     to_bytes(b'Content-Disposition: form-data; name="%s"; filename="%s"' % (
      key, filename)),
     to_bytes(b'Content-Type: %s' % content_type),
     b'',
     to_bytes(file.read())]


class RequestFactory(object):
    """
    Class that lets you create mock Request objects for use in testing.

    Usage:

    rf = RequestFactory()
    get_request = rf.get('/hello/')
    post_request = rf.post('/submit/', {'foo': 'bar'})

    Once you have a request object you can pass it to any view function,
    just as if that view had been hooked up using a URLconf.
    """

    def __init__(self, **defaults):
        self.defaults = defaults
        self.cookies = SimpleCookie()
        self.errors = BytesIO()

    def _base_environ(self, **request):
        """
        The base environment for a request.
        """
        environ = {b'HTTP_COOKIE': self.cookies.output(header=b'', sep=b'; '), 
           b'PATH_INFO': str(b'/'), 
           b'REMOTE_ADDR': str(b'127.0.0.1'), 
           b'REQUEST_METHOD': str(b'GET'), 
           b'SCRIPT_NAME': str(b''), 
           b'SERVER_NAME': str(b'testserver'), 
           b'SERVER_PORT': str(b'80'), 
           b'SERVER_PROTOCOL': str(b'HTTP/1.1'), 
           b'wsgi.version': (1, 0), 
           b'wsgi.url_scheme': str(b'http'), 
           b'wsgi.input': FakePayload(b''), 
           b'wsgi.errors': self.errors, 
           b'wsgi.multiprocess': True, 
           b'wsgi.multithread': False, 
           b'wsgi.run_once': False}
        environ.update(self.defaults)
        environ.update(request)
        return environ

    def request(self, **request):
        """Construct a generic request object."""
        return WSGIRequest(self._base_environ(**request))

    def _encode_data(self, data, content_type):
        if content_type is MULTIPART_CONTENT:
            return encode_multipart(BOUNDARY, data)
        else:
            match = CONTENT_TYPE_RE.match(content_type)
            if match:
                charset = match.group(1)
            else:
                charset = settings.DEFAULT_CHARSET
            return force_bytes(data, encoding=charset)

    def _get_path(self, parsed):
        path = force_str(parsed[2])
        if parsed[3]:
            path += str(b';') + force_str(parsed[3])
        path = uri_to_iri(path).encode(UTF_8)
        if six.PY3:
            return path.decode(ISO_8859_1)
        return path

    def get(self, path, data=None, secure=False, **extra):
        """Construct a GET request."""
        data = {} if data is None else data
        r = {b'QUERY_STRING': urlencode(data, doseq=True)}
        r.update(extra)
        return self.generic(b'GET', path, secure=secure, **r)

    def post(self, path, data=None, content_type=MULTIPART_CONTENT, secure=False, **extra):
        """Construct a POST request."""
        data = {} if data is None else data
        post_data = self._encode_data(data, content_type)
        return self.generic(b'POST', path, post_data, content_type, secure=secure, **extra)

    def head(self, path, data=None, secure=False, **extra):
        """Construct a HEAD request."""
        data = {} if data is None else data
        r = {b'QUERY_STRING': urlencode(data, doseq=True)}
        r.update(extra)
        return self.generic(b'HEAD', path, secure=secure, **r)

    def trace(self, path, secure=False, **extra):
        """Construct a TRACE request."""
        return self.generic(b'TRACE', path, secure=secure, **extra)

    def options(self, path, data=b'', content_type=b'application/octet-stream', secure=False, **extra):
        """Construct an OPTIONS request."""
        return self.generic(b'OPTIONS', path, data, content_type, secure=secure, **extra)

    def put(self, path, data=b'', content_type=b'application/octet-stream', secure=False, **extra):
        """Construct a PUT request."""
        return self.generic(b'PUT', path, data, content_type, secure=secure, **extra)

    def patch(self, path, data=b'', content_type=b'application/octet-stream', secure=False, **extra):
        """Construct a PATCH request."""
        return self.generic(b'PATCH', path, data, content_type, secure=secure, **extra)

    def delete(self, path, data=b'', content_type=b'application/octet-stream', secure=False, **extra):
        """Construct a DELETE request."""
        return self.generic(b'DELETE', path, data, content_type, secure=secure, **extra)

    def generic(self, method, path, data=b'', content_type=b'application/octet-stream', secure=False, **extra):
        """Constructs an arbitrary HTTP request."""
        parsed = urlparse(force_str(path))
        data = force_bytes(data, settings.DEFAULT_CHARSET)
        r = {b'PATH_INFO': self._get_path(parsed), 
           b'REQUEST_METHOD': str(method), 
           b'SERVER_PORT': str(b'443') if secure else str(b'80'), 
           b'wsgi.url_scheme': str(b'https') if secure else str(b'http')}
        if data:
            r.update({b'CONTENT_LENGTH': len(data), 
               b'CONTENT_TYPE': str(content_type), 
               b'wsgi.input': FakePayload(data)})
        r.update(extra)
        if not r.get(b'QUERY_STRING'):
            query_string = force_bytes(parsed[4])
            if six.PY3:
                query_string = query_string.decode(b'iso-8859-1')
            r[b'QUERY_STRING'] = query_string
        return self.request(**r)


class Client(RequestFactory):
    """
    A class that can act as a client for testing purposes.

    It allows the user to compose GET and POST requests, and
    obtain the response that the server gave to those requests.
    The server Response objects are annotated with the details
    of the contexts and templates that were rendered during the
    process of serving the request.

    Client objects are stateful - they will retain cookie (and
    thus session) details for the lifetime of the Client instance.

    This is not intended as a replacement for Twill/Selenium or
    the like - it is here to allow testing against the
    contexts and templates produced by a view, rather than the
    HTML rendered to the end-user.
    """

    def __init__(self, enforce_csrf_checks=False, **defaults):
        super(Client, self).__init__(**defaults)
        self.handler = ClientHandler(enforce_csrf_checks)
        self.exc_info = None
        return

    def store_exc_info(self, **kwargs):
        """
        Stores exceptions when they are generated by a view.
        """
        self.exc_info = sys.exc_info()

    @property
    def session(self):
        """
        Obtains the current session variables.
        """
        engine = import_module(settings.SESSION_ENGINE)
        cookie = self.cookies.get(settings.SESSION_COOKIE_NAME)
        if cookie:
            return engine.SessionStore(cookie.value)
        session = engine.SessionStore()
        session.save()
        self.cookies[settings.SESSION_COOKIE_NAME] = session.session_key
        return session

    def request(self, **request):
        """
        The master request method. Composes the environment dictionary
        and passes to the handler, returning the result of the handler.
        Assumes defaults for the query environment, which can be overridden
        using the arguments to the request.
        """
        environ = self._base_environ(**request)
        data = {}
        on_template_render = curry(store_rendered_templates, data)
        signal_uid = b'template-render-%s' % id(request)
        signals.template_rendered.connect(on_template_render, dispatch_uid=signal_uid)
        exception_uid = b'request-exception-%s' % id(request)
        got_request_exception.connect(self.store_exc_info, dispatch_uid=exception_uid)
        try:
            try:
                response = self.handler(environ)
            except TemplateDoesNotExist as e:
                if e.args != ('500.html', ):
                    raise

            if self.exc_info:
                exc_info = self.exc_info
                self.exc_info = None
                six.reraise(*exc_info)
            response.client = self
            response.request = request
            response.templates = data.get(b'templates', [])
            response.context = data.get(b'context')
            response.json = curry(self._parse_json, response)
            response.resolver_match = SimpleLazyObject(lambda : resolve(request[b'PATH_INFO']))
            if response.context and len(response.context) == 1:
                response.context = response.context[0]
            if response.cookies:
                self.cookies.update(response.cookies)
            return response
        finally:
            signals.template_rendered.disconnect(dispatch_uid=signal_uid)
            got_request_exception.disconnect(dispatch_uid=exception_uid)

        return

    def get(self, path, data=None, follow=False, secure=False, **extra):
        """
        Requests a response from the server using GET.
        """
        response = super(Client, self).get(path, data=data, secure=secure, **extra)
        if follow:
            response = self._handle_redirects(response, **extra)
        return response

    def post(self, path, data=None, content_type=MULTIPART_CONTENT, follow=False, secure=False, **extra):
        """
        Requests a response from the server using POST.
        """
        response = super(Client, self).post(path, data=data, content_type=content_type, secure=secure, **extra)
        if follow:
            response = self._handle_redirects(response, **extra)
        return response

    def head(self, path, data=None, follow=False, secure=False, **extra):
        """
        Request a response from the server using HEAD.
        """
        response = super(Client, self).head(path, data=data, secure=secure, **extra)
        if follow:
            response = self._handle_redirects(response, **extra)
        return response

    def options(self, path, data=b'', content_type=b'application/octet-stream', follow=False, secure=False, **extra):
        """
        Request a response from the server using OPTIONS.
        """
        response = super(Client, self).options(path, data=data, content_type=content_type, secure=secure, **extra)
        if follow:
            response = self._handle_redirects(response, **extra)
        return response

    def put(self, path, data=b'', content_type=b'application/octet-stream', follow=False, secure=False, **extra):
        """
        Send a resource to the server using PUT.
        """
        response = super(Client, self).put(path, data=data, content_type=content_type, secure=secure, **extra)
        if follow:
            response = self._handle_redirects(response, **extra)
        return response

    def patch(self, path, data=b'', content_type=b'application/octet-stream', follow=False, secure=False, **extra):
        """
        Send a resource to the server using PATCH.
        """
        response = super(Client, self).patch(path, data=data, content_type=content_type, secure=secure, **extra)
        if follow:
            response = self._handle_redirects(response, **extra)
        return response

    def delete(self, path, data=b'', content_type=b'application/octet-stream', follow=False, secure=False, **extra):
        """
        Send a DELETE request to the server.
        """
        response = super(Client, self).delete(path, data=data, content_type=content_type, secure=secure, **extra)
        if follow:
            response = self._handle_redirects(response, **extra)
        return response

    def trace(self, path, data=b'', follow=False, secure=False, **extra):
        """
        Send a TRACE request to the server.
        """
        response = super(Client, self).trace(path, data=data, secure=secure, **extra)
        if follow:
            response = self._handle_redirects(response, **extra)
        return response

    def login(self, **credentials):
        """
        Sets the Factory to appear as if it has successfully logged into a site.

        Returns True if login is possible; False if the provided credentials
        are incorrect.
        """
        from django.contrib.auth import authenticate
        user = authenticate(**credentials)
        if user:
            self._login(user)
            return True
        else:
            return False

    def force_login(self, user, backend=None):

        def get_backend():
            from django.contrib.auth import load_backend
            for backend_path in settings.AUTHENTICATION_BACKENDS:
                backend = load_backend(backend_path)
                if hasattr(backend, b'get_user'):
                    return backend_path

        if backend is None:
            backend = get_backend()
        user.backend = backend
        self._login(user, backend)
        return

    def _login(self, user, backend=None):
        from django.contrib.auth import login
        engine = import_module(settings.SESSION_ENGINE)
        request = HttpRequest()
        if self.session:
            request.session = self.session
        else:
            request.session = engine.SessionStore()
        login(request, user, backend)
        request.session.save()
        session_cookie = settings.SESSION_COOKIE_NAME
        self.cookies[session_cookie] = request.session.session_key
        cookie_data = {b'max-age': None, 
           b'path': b'/', 
           b'domain': settings.SESSION_COOKIE_DOMAIN, 
           b'secure': settings.SESSION_COOKIE_SECURE or None, 
           b'expires': None}
        self.cookies[session_cookie].update(cookie_data)
        return

    def logout(self):
        """
        Removes the authenticated user's cookies and session object.

        Causes the authenticated user to be logged out.
        """
        from django.contrib.auth import get_user, logout
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        if self.session:
            request.session = self.session
            request.user = get_user(request)
        else:
            request.session = engine.SessionStore()
        logout(request)
        self.cookies = SimpleCookie()

    def _parse_json(self, response, **extra):
        if not hasattr(response, b'_json'):
            if not JSON_CONTENT_TYPE_RE.match(response.get(b'Content-Type')):
                raise ValueError((b'Content-Type header is "{0}", not "application/json"').format(response.get(b'Content-Type')))
            response._json = json.loads(response.content.decode(), **extra)
        return response._json

    def _handle_redirects(self, response, **extra):
        """Follows any redirects by requesting responses from the server using GET."""
        response.redirect_chain = []
        while response.status_code in (301, 302, 303, 307):
            response_url = response.url
            redirect_chain = response.redirect_chain
            redirect_chain.append((response_url, response.status_code))
            url = urlsplit(response_url)
            if url.scheme:
                extra[b'wsgi.url_scheme'] = url.scheme
            if url.hostname:
                extra[b'SERVER_NAME'] = url.hostname
            if url.port:
                extra[b'SERVER_PORT'] = str(url.port)
            path = url.path
            if not path.startswith(b'/'):
                path = urljoin(response.request[b'PATH_INFO'], path)
            response = self.get(path, QueryDict(url.query), follow=False, **extra)
            response.redirect_chain = redirect_chain
            if redirect_chain[(-1)] in redirect_chain[:-1]:
                raise RedirectCycleError(b'Redirect loop detected.', last_response=response)
            if len(redirect_chain) > 20:
                raise RedirectCycleError(b'Too many redirects.', last_response=response)

        return response