# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mrdon/dev/flask-async/venv/lib/python3.3/site-packages/werkzeug/exceptions.py
# Compiled at: 2014-01-20 15:46:16
# Size of source mod 2**32: 17799 bytes
"""
    werkzeug.exceptions
    ~~~~~~~~~~~~~~~~~~~

    This module implements a number of Python exceptions you can raise from
    within your views to trigger a standard non-200 response.

    Usage Example
    -------------

    ::

        from werkzeug.wrappers import BaseRequest
        from werkzeug.wsgi import responder
        from werkzeug.exceptions import HTTPException, NotFound

        def view(request):
            raise NotFound()

        @responder
        def application(environ, start_response):
            request = BaseRequest(environ)
            try:
                return view(request)
            except HTTPException as e:
                return e

    As you can see from this example those exceptions are callable WSGI
    applications.  Because of Python 2.4 compatibility those do not extend
    from the response objects but only from the python exception class.

    As a matter of fact they are not Werkzeug response objects.  However you
    can get a response object by calling ``get_response()`` on a HTTP
    exception.

    Keep in mind that you have to pass an environment to ``get_response()``
    because some errors fetch additional information from the WSGI
    environment.

    If you want to hook in a different exception page to say, a 404 status
    code, you can add a second except for a specific subclass of an error::

        @responder
        def application(environ, start_response):
            request = BaseRequest(environ)
            try:
                return view(request)
            except NotFound, e:
                return not_found(request)
            except HTTPException, e:
                return e

    :copyright: (c) 2013 by the Werkzeug Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""
import sys, werkzeug
werkzeug.exceptions = sys.modules[__name__]
from werkzeug._internal import _get_environ
from werkzeug._compat import iteritems, integer_types, text_type, implements_to_string
from werkzeug.wrappers import Response

@implements_to_string
class HTTPException(Exception):
    __doc__ = '\n    Baseclass for all HTTP exceptions.  This exception can be called as WSGI\n    application to render a default error page or you can catch the subclasses\n    of it independently and render nicer error messages.\n    '
    code = None
    description = None

    def __init__(self, description=None, response=None):
        Exception.__init__(self)
        if description is not None:
            self.description = description
        self.response = response
        return

    @classmethod
    def wrap(cls, exception, name=None):
        """This method returns a new subclass of the exception provided that
        also is a subclass of `BadRequest`.
        """

        class newcls(cls):

            def __init__(self, arg=None, *args, **kwargs):
                cls.__init__(self, *args, **kwargs)
                exception.__init__(self, arg)

        newcls.__module__ = sys._getframe(1).f_globals.get('__name__')
        newcls.__name__ = name or cls.__name__ + exception.__name__
        return newcls

    @property
    def name(self):
        """The status name."""
        return HTTP_STATUS_CODES.get(self.code, 'Unknown Error')

    def get_description(self, environ=None):
        """Get the description."""
        return '<p>%s</p>' % escape(self.description)

    def get_body(self, environ=None):
        """Get the HTML body."""
        return text_type('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n<title>%(code)s %(name)s</title>\n<h1>%(name)s</h1>\n%(description)s\n' % {'code': self.code, 
         'name': escape(self.name), 
         'description': self.get_description(environ)})

    def get_headers(self, environ=None):
        """Get a list of headers."""
        return [
         ('Content-Type', 'text/html')]

    def get_response(self, environ=None):
        """Get a response object.  If one was passed to the exception
        it's returned directly.

        :param environ: the optional environ for the request.  This
                        can be used to modify the response depending
                        on how the request looked like.
        :return: a :class:`Response` object or a subclass thereof.
        """
        if self.response is not None:
            return self.response
        else:
            if environ is not None:
                environ = _get_environ(environ)
            headers = self.get_headers(environ)
            return Response(self.get_body(environ), self.code, headers)

    def __call__(self, environ, start_response):
        """Call the exception as WSGI application.

        :param environ: the WSGI environment.
        :param start_response: the response callable provided by the WSGI
                               server.
        """
        response = self.get_response(environ)
        return response(environ, start_response)

    def __str__(self):
        return '%d: %s' % (self.code, self.name)

    def __repr__(self):
        return "<%s '%s'>" % (self.__class__.__name__, self)


class BadRequest(HTTPException):
    __doc__ = '*400* `Bad Request`\n\n    Raise if the browser sends something to the application the application\n    or server cannot handle.\n    '
    code = 400
    description = 'The browser (or proxy) sent a request that this server could not understand.'


class ClientDisconnected(BadRequest):
    __doc__ = 'Internal exception that is raised if Werkzeug detects a disconnected\n    client.  Since the client is already gone at that point attempting to\n    send the error message to the client might not work and might ultimately\n    result in another exception in the server.  Mainly this is here so that\n    it is silenced by default as far as Werkzeug is concerned.\n\n    Since disconnections cannot be reliably detected and are unspecified\n    by WSGI to a large extend this might or might not be raised if a client\n    is gone.\n\n    .. versionadded:: 0.8\n    '


class SecurityError(BadRequest):
    __doc__ = 'Raised if something triggers a security error.  This is otherwise\n    exactly like a bad request error.\n\n    .. versionadded:: 0.9\n    '


class Unauthorized(HTTPException):
    __doc__ = '*401* `Unauthorized`\n\n    Raise if the user is not authorized.  Also used if you want to use HTTP\n    basic auth.\n    '
    code = 401
    description = "The server could not verify that you are authorized to access the URL requested.  You either supplied the wrong credentials (e.g. a bad password), or your browser doesn't understand how to supply the credentials required."


class Forbidden(HTTPException):
    __doc__ = "*403* `Forbidden`\n\n    Raise if the user doesn't have the permission for the requested resource\n    but was authenticated.\n    "
    code = 403
    description = "You don't have the permission to access the requested resource. It is either read-protected or not readable by the server."


class NotFound(HTTPException):
    __doc__ = '*404* `Not Found`\n\n    Raise if a resource does not exist and never existed.\n    '
    code = 404
    description = 'The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.'


class MethodNotAllowed(HTTPException):
    __doc__ = "*405* `Method Not Allowed`\n\n    Raise if the server used a method the resource does not handle.  For\n    example `POST` if the resource is view only.  Especially useful for REST.\n\n    The first argument for this exception should be a list of allowed methods.\n    Strictly speaking the response would be invalid if you don't provide valid\n    methods in the header which you can do with that list.\n    "
    code = 405
    description = 'The method is not allowed for the requested URL.'

    def __init__(self, valid_methods=None, description=None):
        """Takes an optional list of valid http methods
        starting with werkzeug 0.3 the list will be mandatory."""
        HTTPException.__init__(self, description)
        self.valid_methods = valid_methods

    def get_headers(self, environ):
        headers = HTTPException.get_headers(self, environ)
        if self.valid_methods:
            headers.append(('Allow', ', '.join(self.valid_methods)))
        return headers


class NotAcceptable(HTTPException):
    __doc__ = "*406* `Not Acceptable`\n\n    Raise if the server can't return any content conforming to the\n    `Accept` headers of the client.\n    "
    code = 406
    description = 'The resource identified by the request is only capable of generating response entities which have content characteristics not acceptable according to the accept headers sent in the request.'


class RequestTimeout(HTTPException):
    __doc__ = '*408* `Request Timeout`\n\n    Raise to signalize a timeout.\n    '
    code = 408
    description = "The server closed the network connection because the browser didn't finish the request within the specified time."


class Conflict(HTTPException):
    __doc__ = '*409* `Conflict`\n\n    Raise to signal that a request cannot be completed because it conflicts\n    with the current state on the server.\n\n    .. versionadded:: 0.7\n    '
    code = 409
    description = 'A conflict happened while processing the request.  The resource might have been modified while the request was being processed.'


class Gone(HTTPException):
    __doc__ = '*410* `Gone`\n\n    Raise if a resource existed previously and went away without new location.\n    '
    code = 410
    description = 'The requested URL is no longer available on this server and there is no forwarding address.</p><p>If you followed a link from a foreign page, please contact the author of this page.'


class LengthRequired(HTTPException):
    __doc__ = '*411* `Length Required`\n\n    Raise if the browser submitted data but no ``Content-Length`` header which\n    is required for the kind of processing the server does.\n    '
    code = 411
    description = 'A request with this method requires a valid <code>Content-Length</code> header.'


class PreconditionFailed(HTTPException):
    __doc__ = '*412* `Precondition Failed`\n\n    Status code used in combination with ``If-Match``, ``If-None-Match``, or\n    ``If-Unmodified-Since``.\n    '
    code = 412
    description = 'The precondition on the request for the URL failed positive evaluation.'


class RequestEntityTooLarge(HTTPException):
    __doc__ = '*413* `Request Entity Too Large`\n\n    The status code one should return if the data submitted exceeded a given\n    limit.\n    '
    code = 413
    description = 'The data value transmitted exceeds the capacity limit.'


class RequestURITooLarge(HTTPException):
    __doc__ = '*414* `Request URI Too Large`\n\n    Like *413* but for too long URLs.\n    '
    code = 414
    description = 'The length of the requested URL exceeds the capacity limit for this server.  The request cannot be processed.'


class UnsupportedMediaType(HTTPException):
    __doc__ = '*415* `Unsupported Media Type`\n\n    The status code returned if the server is unable to handle the media type\n    the client transmitted.\n    '
    code = 415
    description = 'The server does not support the media type transmitted in the request.'


class RequestedRangeNotSatisfiable(HTTPException):
    __doc__ = '*416* `Requested Range Not Satisfiable`\n\n    The client asked for a part of the file that lies beyond the end\n    of the file.\n\n    .. versionadded:: 0.7\n    '
    code = 416
    description = 'The server cannot provide the requested range.'


class ExpectationFailed(HTTPException):
    __doc__ = '*417* `Expectation Failed`\n\n    The server cannot meet the requirements of the Expect request-header.\n\n    .. versionadded:: 0.7\n    '
    code = 417
    description = 'The server could not meet the requirements of the Expect header'


class ImATeapot(HTTPException):
    __doc__ = "*418* `I'm a teapot`\n\n    The server should return this if it is a teapot and someone attempted\n    to brew coffee with it.\n\n    .. versionadded:: 0.7\n    "
    code = 418
    description = 'This server is a teapot, not a coffee machine'


class UnprocessableEntity(HTTPException):
    __doc__ = '*422* `Unprocessable Entity`\n\n    Used if the request is well formed, but the instructions are otherwise\n    incorrect.\n    '
    code = 422
    description = 'The request was well-formed but was unable to be followed due to semantic errors.'


class PreconditionRequired(HTTPException):
    __doc__ = '*428* `Precondition Required`\n\n    The server requires this request to be conditional, typically to prevent\n    the lost update problem, which is a race condition between two or more\n    clients attempting to update a resource through PUT or DELETE. By requiring\n    each client to include a conditional header ("If-Match" or "If-Unmodified-\n    Since") with the proper value retained from a recent GET request, the\n    server ensures that each client has at least seen the previous revision of\n    the resource.\n    '
    code = 428
    description = 'This request is required to be conditional; try using "If-Match" or "If-Unmodified-Since".'


class TooManyRequests(HTTPException):
    __doc__ = '*429* `Too Many Requests`\n\n    The server is limiting the rate at which this user receives responses, and\n    this request exceeds that rate. (The server may use any convenient method\n    to identify users and their request rates). The server may include a\n    "Retry-After" header to indicate how long the user should wait before\n    retrying.\n    '
    code = 429
    description = 'This user has exceeded an allotted request count. Try again later.'


class RequestHeaderFieldsTooLarge(HTTPException):
    __doc__ = '*431* `Request Header Fields Too Large`\n\n    The server refuses to process the request because the header fields are too\n    large. One or more individual fields may be too large, or the set of all\n    headers is too large.\n    '
    code = 431
    description = 'One or more header fields exceeds the maximum size.'


class InternalServerError(HTTPException):
    __doc__ = '*500* `Internal Server Error`\n\n    Raise if an internal server error occurred.  This is a good fallback if an\n    unknown error occurred in the dispatcher.\n    '
    code = 500
    description = 'The server encountered an internal error and was unable to complete your request.  Either the server is overloaded or there is an error in the application.'


class NotImplemented(HTTPException):
    __doc__ = '*501* `Not Implemented`\n\n    Raise if the application does not support the action requested by the\n    browser.\n    '
    code = 501
    description = 'The server does not support the action requested by the browser.'


class BadGateway(HTTPException):
    __doc__ = '*502* `Bad Gateway`\n\n    If you do proxying in your application you should return this status code\n    if you received an invalid response from the upstream server it accessed\n    in attempting to fulfill the request.\n    '
    code = 502
    description = 'The proxy server received an invalid response from an upstream server.'


class ServiceUnavailable(HTTPException):
    __doc__ = '*503* `Service Unavailable`\n\n    Status code you should return if a service is temporarily unavailable.\n    '
    code = 503
    description = 'The server is temporarily unable to service your request due to maintenance downtime or capacity problems.  Please try again later.'


default_exceptions = {}
__all__ = [
 'HTTPException']

def _find_exceptions():
    for name, obj in iteritems(globals()):
        try:
            if getattr(obj, 'code', None) is not None:
                default_exceptions[obj.code] = obj
                __all__.append(obj.__name__)
        except TypeError:
            continue

    return


_find_exceptions()
del _find_exceptions

class Aborter(object):
    __doc__ = "\n    When passed a dict of code -> exception items it can be used as\n    callable that raises exceptions.  If the first argument to the\n    callable is an integer it will be looked up in the mapping, if it's\n    a WSGI application it will be raised in a proxy exception.\n\n    The rest of the arguments are forwarded to the exception constructor.\n    "

    def __init__(self, mapping=None, extra=None):
        if mapping is None:
            mapping = default_exceptions
        self.mapping = dict(mapping)
        if extra is not None:
            self.mapping.update(extra)
        return

    def __call__(self, code, *args, **kwargs):
        if not args:
            if not kwargs and not isinstance(code, integer_types):
                raise HTTPException(response=code)
        if code not in self.mapping:
            raise LookupError('no exception for %r' % code)
        raise self.mapping[code](*args, **kwargs)


abort = Aborter()
BadRequestKeyError = BadRequest.wrap(KeyError)
from werkzeug.utils import escape
from werkzeug.http import HTTP_STATUS_CODES