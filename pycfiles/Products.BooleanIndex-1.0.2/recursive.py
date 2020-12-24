# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/plone-production-nbf-1/zeocluster/src/Products.BlobNewsItem/Paste-1.7.5.1-py2.6.egg/paste/recursive.py
# Compiled at: 2012-02-27 07:41:58
__doc__ = "\nMiddleware to make internal requests and forward requests internally.\n\nWhen applied, several keys are added to the environment that will allow\nyou to trigger recursive redirects and forwards.\n\n  paste.recursive.include:\n      When you call\n      ``environ['paste.recursive.include'](new_path_info)`` a response\n      will be returned.  The response has a ``body`` attribute, a\n      ``status`` attribute, and a ``headers`` attribute.\n\n  paste.recursive.script_name:\n      The ``SCRIPT_NAME`` at the point that recursive lives.  Only\n      paths underneath this path can be redirected to.\n\n  paste.recursive.old_path_info:\n      A list of previous ``PATH_INFO`` values from previous redirects.\n\nRaise ``ForwardRequestException(new_path_info)`` to do a forward\n(aborting the current request).\n"
from cStringIO import StringIO
import warnings
__all__ = [
 'RecursiveMiddleware']
__pudge_all__ = ['RecursiveMiddleware', 'ForwardRequestException']

class RecursionLoop(AssertionError):
    """Raised when a recursion enters into a loop"""


class CheckForRecursionMiddleware(object):

    def __init__(self, app, env):
        self.app = app
        self.env = env

    def __call__(self, environ, start_response):
        path_info = environ.get('PATH_INFO', '')
        if path_info in self.env.get('paste.recursive.old_path_info', []):
            raise RecursionLoop('Forwarding loop detected; %r visited twice (internal redirect path: %s)' % (
             path_info, self.env['paste.recursive.old_path_info']))
        old_path_info = self.env.setdefault('paste.recursive.old_path_info', [])
        old_path_info.append(self.env.get('PATH_INFO', ''))
        return self.app(environ, start_response)


class RecursiveMiddleware(object):
    """
    A WSGI middleware that allows for recursive and forwarded calls.
    All these calls go to the same 'application', but presumably that
    application acts differently with different URLs.  The forwarded
    URLs must be relative to this container.

    Interface is entirely through the ``paste.recursive.forward`` and
    ``paste.recursive.include`` environmental keys.
    """

    def __init__(self, application, global_conf=None):
        self.application = application

    def __call__(self, environ, start_response):
        environ['paste.recursive.forward'] = Forwarder(self.application, environ, start_response)
        environ['paste.recursive.include'] = Includer(self.application, environ, start_response)
        environ['paste.recursive.include_app_iter'] = IncluderAppIter(self.application, environ, start_response)
        my_script_name = environ.get('SCRIPT_NAME', '')
        environ['paste.recursive.script_name'] = my_script_name
        try:
            return self.application(environ, start_response)
        except ForwardRequestException, e:
            middleware = CheckForRecursionMiddleware(e.factory(self), environ)
            return middleware(environ, start_response)


class ForwardRequestException(Exception):
    """
    Used to signal that a request should be forwarded to a different location.

    ``url``
        The URL to forward to starting with a ``/`` and relative to
        ``RecursiveMiddleware``. URL fragments can also contain query strings
        so ``/error?code=404`` would be a valid URL fragment.

    ``environ``
        An altertative WSGI environment dictionary to use for the forwarded
        request. If specified is used *instead* of the ``url_fragment``

    ``factory``
        If specifed ``factory`` is used instead of ``url`` or ``environ``.
        ``factory`` is a callable that takes a WSGI application object
        as the first argument and returns an initialised WSGI middleware
        which can alter the forwarded response.

    Basic usage (must have ``RecursiveMiddleware`` present) :

    .. code-block:: python

        from paste.recursive import ForwardRequestException
        def app(environ, start_response):
            if environ['PATH_INFO'] == '/hello':
                start_response("200 OK", [('Content-type', 'text/plain')])
                return ['Hello World!']
            elif environ['PATH_INFO'] == '/error':
                start_response("404 Not Found", [('Content-type', 'text/plain')])
                return ['Page not found']
            else:
                raise ForwardRequestException('/error')

        from paste.recursive import RecursiveMiddleware
        app = RecursiveMiddleware(app)

    If you ran this application and visited ``/hello`` you would get a
    ``Hello World!`` message. If you ran the application and visited
    ``/not_found`` a ``ForwardRequestException`` would be raised and the caught
    by the ``RecursiveMiddleware``. The ``RecursiveMiddleware`` would then
    return the headers and response from the ``/error`` URL but would display
    a ``404 Not found`` status message.

    You could also specify an ``environ`` dictionary instead of a url. Using
    the same example as before:

    .. code-block:: python

        def app(environ, start_response):
            ... same as previous example ...
            else:
                new_environ = environ.copy()
                new_environ['PATH_INFO'] = '/error'
                raise ForwardRequestException(environ=new_environ)

    Finally, if you want complete control over every aspect of the forward you
    can specify a middleware factory. For example to keep the old status code
    but use the headers and resposne body from the forwarded response you might
    do this:

    .. code-block:: python

        from paste.recursive import ForwardRequestException
        from paste.recursive import RecursiveMiddleware
        from paste.errordocument import StatusKeeper

        def app(environ, start_response):
            if environ['PATH_INFO'] == '/hello':
                start_response("200 OK", [('Content-type', 'text/plain')])
                return ['Hello World!']
            elif environ['PATH_INFO'] == '/error':
                start_response("404 Not Found", [('Content-type', 'text/plain')])
                return ['Page not found']
            else:
                def factory(app):
                    return StatusKeeper(app, status='404 Not Found', url='/error')
                raise ForwardRequestException(factory=factory)

        app = RecursiveMiddleware(app)
    """

    def __init__(self, url=None, environ={}, factory=None, path_info=None):
        if factory:
            if url:
                raise TypeError('You cannot specify factory and a url in ForwardRequestException')
            elif factory and environ:
                raise TypeError('You cannot specify factory and environ in ForwardRequestException')
            if url and environ:
                raise TypeError('You cannot specify environ and url in ForwardRequestException')
            if path_info:
                url or warnings.warn('ForwardRequestException(path_info=...) has been deprecated; please use ForwardRequestException(url=...)', DeprecationWarning, 2)
            else:
                raise TypeError('You cannot use url and path_info in ForwardRequestException')
            self.path_info = path_info
        if url and '?' not in str(url):
            self.path_info = url

        class ForwardRequestExceptionMiddleware(object):

            def __init__(self, app):
                self.app = app

        if hasattr(self, 'path_info'):
            p = self.path_info

            def factory_(app):

                class PathInfoForward(ForwardRequestExceptionMiddleware):

                    def __call__(self, environ, start_response):
                        environ['PATH_INFO'] = p
                        return self.app(environ, start_response)

                return PathInfoForward(app)

            self.factory = factory_
        elif url:

            def factory_(app):

                class URLForward(ForwardRequestExceptionMiddleware):

                    def __call__(self, environ, start_response):
                        environ['PATH_INFO'] = url.split('?')[0]
                        environ['QUERY_STRING'] = url.split('?')[1]
                        return self.app(environ, start_response)

                return URLForward(app)

            self.factory = factory_
        elif environ:

            def factory_(app):

                class EnvironForward(ForwardRequestExceptionMiddleware):

                    def __call__(self, environ_, start_response):
                        return self.app(environ, start_response)

                return EnvironForward(app)

            self.factory = factory_
        else:
            self.factory = factory


class Recursive(object):

    def __init__(self, application, environ, start_response):
        self.application = application
        self.original_environ = environ.copy()
        self.previous_environ = environ
        self.start_response = start_response

    def __call__(self, path, extra_environ=None):
        """
        `extra_environ` is an optional dictionary that is also added
        to the forwarded request.  E.g., ``{'HTTP_HOST': 'new.host'}``
        could be used to forward to a different virtual host.
        """
        environ = self.original_environ.copy()
        if extra_environ:
            environ.update(extra_environ)
        environ['paste.recursive.previous_environ'] = self.previous_environ
        base_path = self.original_environ.get('SCRIPT_NAME')
        if path.startswith('/'):
            assert path.startswith(base_path), 'You can only forward requests to resources under the path %r (not %r)' % (
             base_path, path)
            path = path[len(base_path) + 1:]
        assert not path.startswith('/')
        path_info = '/' + path
        environ['PATH_INFO'] = path_info
        environ['REQUEST_METHOD'] = 'GET'
        environ['CONTENT_LENGTH'] = '0'
        environ['CONTENT_TYPE'] = ''
        environ['wsgi.input'] = StringIO('')
        return self.activate(environ)

    def activate(self, environ):
        raise NotImplementedError

    def __repr__(self):
        return '<%s.%s from %s>' % (
         self.__class__.__module__,
         self.__class__.__name__,
         self.original_environ.get('SCRIPT_NAME') or '/')


class Forwarder(Recursive):
    """
    The forwarder will try to restart the request, except with
    the new `path` (replacing ``PATH_INFO`` in the request).

    It must not be called after and headers have been returned.
    It returns an iterator that must be returned back up the call
    stack, so it must be used like:

    .. code-block:: python

        return environ['paste.recursive.forward'](path)

    Meaningful transformations cannot be done, since headers are
    sent directly to the server and cannot be inspected or
    rewritten.
    """

    def activate(self, environ):
        warnings.warn('recursive.Forwarder has been deprecated; please use ForwardRequestException', DeprecationWarning, 2)
        return self.application(environ, self.start_response)


class Includer(Recursive):
    """
    Starts another request with the given path and adding or
    overwriting any values in the `extra_environ` dictionary.
    Returns an IncludeResponse object.
    """

    def activate(self, environ):
        response = IncludedResponse()

        def start_response(status, headers, exc_info=None):
            if exc_info:
                raise exc_info[0], exc_info[1], exc_info[2]
            response.status = status
            response.headers = headers
            return response.write

        app_iter = self.application(environ, start_response)
        try:
            for s in app_iter:
                response.write(s)

        finally:
            if hasattr(app_iter, 'close'):
                app_iter.close()

        response.close()
        return response


class IncludedResponse(object):

    def __init__(self):
        self.headers = None
        self.status = None
        self.output = StringIO()
        self.str = None
        return

    def close(self):
        self.str = self.output.getvalue()
        self.output.close()
        self.output = None
        return

    def write(self, s):
        assert self.output is not None, 'This response has already been closed and no further data can be written.'
        self.output.write(s)
        return

    def __str__(self):
        return self.body

    def body__get(self):
        if self.str is None:
            return self.output.getvalue()
        else:
            return self.str
            return

    body = property(body__get)


class IncluderAppIter(Recursive):
    """
    Like Includer, but just stores the app_iter response
    (be sure to call close on the response!)
    """

    def activate(self, environ):
        response = IncludedAppIterResponse()

        def start_response(status, headers, exc_info=None):
            if exc_info:
                raise exc_info[0], exc_info[1], exc_info[2]
            response.status = status
            response.headers = headers
            return response.write

        app_iter = self.application(environ, start_response)
        response.app_iter = app_iter
        return response


class IncludedAppIterResponse(object):

    def __init__(self):
        self.status = None
        self.headers = None
        self.accumulated = []
        self.app_iter = None
        self._closed = False
        return

    def close(self):
        assert not self._closed, 'Tried to close twice'
        if hasattr(self.app_iter, 'close'):
            self.app_iter.close()

    def write(self, s):
        self.accumulated.append


def make_recursive_middleware(app, global_conf):
    return RecursiveMiddleware(app)


make_recursive_middleware.__doc__ = __doc__