# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/plone-production-nbf-1/zeocluster/src/Products.BlobNewsItem/Paste-1.7.5.1-py2.6.egg/paste/httpexceptions.py
# Compiled at: 2012-02-27 07:41:58
__doc__ = "\nHTTP Exception Middleware\n\nThis module processes Python exceptions that relate to HTTP exceptions\nby defining a set of exceptions, all subclasses of HTTPException, and a\nrequest handler (`middleware`) that catches these exceptions and turns\nthem into proper responses.\n\nThis module defines exceptions according to RFC 2068 [1]_ : codes with\n100-300 are not really errors; 400's are client errors, and 500's are\nserver errors.  According to the WSGI specification [2]_ , the application\ncan call ``start_response`` more then once only under two conditions:\n(a) the response has not yet been sent, or (b) if the second and\nsubsequent invocations of ``start_response`` have a valid ``exc_info``\nargument obtained from ``sys.exc_info()``.  The WSGI specification then\nrequires the server or gateway to handle the case where content has been\nsent and then an exception was encountered.\n\nExceptions in the 5xx range and those raised after ``start_response``\nhas been called are treated as serious errors and the ``exc_info`` is\nfilled-in with information needed for a lower level module to generate a\nstack trace and log information.\n\nException\n  HTTPException\n    HTTPRedirection\n      * 300 - HTTPMultipleChoices\n      * 301 - HTTPMovedPermanently\n      * 302 - HTTPFound\n      * 303 - HTTPSeeOther\n      * 304 - HTTPNotModified\n      * 305 - HTTPUseProxy\n      * 306 - Unused (not implemented, obviously)\n      * 307 - HTTPTemporaryRedirect\n    HTTPError\n      HTTPClientError\n        * 400 - HTTPBadRequest\n        * 401 - HTTPUnauthorized\n        * 402 - HTTPPaymentRequired\n        * 403 - HTTPForbidden\n        * 404 - HTTPNotFound\n        * 405 - HTTPMethodNotAllowed\n        * 406 - HTTPNotAcceptable\n        * 407 - HTTPProxyAuthenticationRequired\n        * 408 - HTTPRequestTimeout\n        * 409 - HTTPConfict\n        * 410 - HTTPGone\n        * 411 - HTTPLengthRequired\n        * 412 - HTTPPreconditionFailed\n        * 413 - HTTPRequestEntityTooLarge\n        * 414 - HTTPRequestURITooLong\n        * 415 - HTTPUnsupportedMediaType\n        * 416 - HTTPRequestRangeNotSatisfiable\n        * 417 - HTTPExpectationFailed\n      HTTPServerError\n        * 500 - HTTPInternalServerError\n        * 501 - HTTPNotImplemented\n        * 502 - HTTPBadGateway\n        * 503 - HTTPServiceUnavailable\n        * 504 - HTTPGatewayTimeout\n        * 505 - HTTPVersionNotSupported\n\nReferences:\n\n.. [1] http://www.python.org/peps/pep-0333.html#error-handling\n.. [2] http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.5\n\n"
import types
from paste.wsgilib import catch_errors_app
from paste.response import has_header, header_value, replace_header
from paste.request import resolve_relative_url
from paste.util.quoting import strip_html, html_quote, no_quote, comment_quote
SERVER_NAME = 'WSGI Server'
TEMPLATE = '<html>\r\n  <head><title>%(title)s</title></head>\r\n  <body>\r\n    <h1>%(title)s</h1>\r\n    <p>%(body)s</p>\r\n    <hr noshade>\r\n    <div align="right">%(server)s</div>\r\n  </body>\r\n</html>\r\n'

class HTTPException(Exception):
    """
    the HTTP exception base class

    This encapsulates an HTTP response that interrupts normal application
    flow; but one which is not necessarly an error condition. For
    example, codes in the 300's are exceptions in that they interrupt
    normal processing; however, they are not considered errors.

    This class is complicated by 4 factors:

      1. The content given to the exception may either be plain-text or
         as html-text.

      2. The template may want to have string-substitutions taken from
         the current ``environ`` or values from incoming headers. This
         is especially troublesome due to case sensitivity.

      3. The final output may either be text/plain or text/html
         mime-type as requested by the client application.

      4. Each exception has a default explanation, but those who
         raise exceptions may want to provide additional detail.

    Attributes:

       ``code``
           the HTTP status code for the exception

       ``title``
           remainder of the status line (stuff after the code)

       ``explanation``
           a plain-text explanation of the error message that is
           not subject to environment or header substitutions;
           it is accessible in the template via %(explanation)s

       ``detail``
           a plain-text message customization that is not subject
           to environment or header substitutions; accessible in
           the template via %(detail)s

       ``template``
           a content fragment (in HTML) used for environment and
           header substitution; the default template includes both
           the explanation and further detail provided in the
           message

       ``required_headers``
           a sequence of headers which are required for proper
           construction of the exception

    Parameters:

       ``detail``
         a plain-text override of the default ``detail``

       ``headers``
         a list of (k,v) header pairs

       ``comment``
         a plain-text additional information which is
         usually stripped/hidden for end-users

    To override the template (which is HTML content) or the plain-text
    explanation, one must subclass the given exception; or customize it
    after it has been created.  This particular breakdown of a message
    into explanation, detail and template allows both the creation of
    plain-text and html messages for various clients as well as
    error-free substitution of environment variables and headers.
    """
    code = None
    title = None
    explanation = ''
    detail = ''
    comment = ''
    template = '%(explanation)s\r\n<br/>%(detail)s\r\n<!-- %(comment)s -->'
    required_headers = ()

    def __init__(self, detail=None, headers=None, comment=None):
        assert self.code, 'Do not directly instantiate abstract exceptions.'
        assert isinstance(headers, (type(None), list)), 'headers must be None or a list: %r' % headers
        assert isinstance(detail, (type(None), basestring)), 'detail must be None or a string: %r' % detail
        assert isinstance(comment, (type(None), basestring)), 'comment must be None or a string: %r' % comment
        self.headers = headers or tuple()
        for req in self.required_headers:
            assert headers and has_header(headers, req), 'Exception %s must be passed the header %r (got headers: %r)' % (
             self.__class__.__name__, req, headers)

        if detail is not None:
            self.detail = detail
        if comment is not None:
            self.comment = comment
        Exception.__init__(self, '%s %s\n%s\n%s\n' % (
         self.code, self.title, self.explanation, self.detail))
        return

    def make_body(self, environ, template, escfunc, comment_escfunc=None):
        comment_escfunc = comment_escfunc or escfunc
        args = {'explanation': escfunc(self.explanation), 'detail': escfunc(self.detail), 
           'comment': comment_escfunc(self.comment)}
        if HTTPException.template != self.template:
            for (k, v) in environ.items():
                args[k] = escfunc(v)

            if self.headers:
                for (k, v) in self.headers:
                    args[k.lower()] = escfunc(v)

        for (key, value) in args.items():
            if isinstance(value, unicode):
                args[key] = value.encode('utf8', 'xmlcharrefreplace')

        return template % args

    def plain(self, environ):
        """ text/plain representation of the exception """
        body = self.make_body(environ, strip_html(self.template), no_quote, comment_quote)
        return '%s %s\r\n%s\r\n' % (self.code, self.title, body)

    def html(self, environ):
        """ text/html representation of the exception """
        body = self.make_body(environ, self.template, html_quote, comment_quote)
        return TEMPLATE % {'title': self.title, 
           'code': self.code, 
           'server': SERVER_NAME, 
           'body': body}

    def prepare_content(self, environ):
        if self.headers:
            headers = list(self.headers)
        else:
            headers = []
        if 'html' in environ.get('HTTP_ACCEPT', '') or '*/*' in environ.get('HTTP_ACCEPT', ''):
            replace_header(headers, 'content-type', 'text/html')
            content = self.html(environ)
        else:
            replace_header(headers, 'content-type', 'text/plain')
            content = self.plain(environ)
        if isinstance(content, unicode):
            content = content.encode('utf8')
            cur_content_type = header_value(headers, 'content-type') or 'text/html'
            replace_header(headers, 'content-type', cur_content_type + '; charset=utf8')
        return (headers, content)

    def response(self, environ):
        from paste.wsgiwrappers import WSGIResponse
        (headers, content) = self.prepare_content(environ)
        resp = WSGIResponse(code=self.code, content=content)
        resp.headers = resp.headers.fromlist(headers)
        return resp

    def wsgi_application(self, environ, start_response, exc_info=None):
        """
        This exception as a WSGI application
        """
        (headers, content) = self.prepare_content(environ)
        start_response('%s %s' % (self.code, self.title), headers, exc_info)
        return [
         content]

    __call__ = wsgi_application

    def __repr__(self):
        return '<%s %s; code=%s>' % (self.__class__.__name__,
         self.title, self.code)


class HTTPError(HTTPException):
    """
    base class for status codes in the 400's and 500's

    This is an exception which indicates that an error has occurred,
    and that any work in progress should not be committed.  These are
    typically results in the 400's and 500's.
    """


class HTTPRedirection(HTTPException):
    """
    base class for 300's status code (redirections)

    This is an abstract base class for 3xx redirection.  It indicates
    that further action needs to be taken by the user agent in order
    to fulfill the request.  It does not necessarly signal an error
    condition.
    """


class _HTTPMove(HTTPRedirection):
    """
    redirections which require a Location field

    Since a 'Location' header is a required attribute of 301, 302, 303,
    305 and 307 (but not 304), this base class provides the mechanics to
    make this easy.  While this has the same parameters as HTTPException,
    if a location is not provided in the headers; it is assumed that the
    detail _is_ the location (this for backward compatibility, otherwise
    we'd add a new attribute).
    """
    required_headers = ('location', )
    explanation = 'The resource has been moved to'
    template = '%(explanation)s <a href="%(location)s">%(location)s</a>;\r\nyou should be redirected automatically.\r\n%(detail)s\r\n<!-- %(comment)s -->'

    def __init__(self, detail=None, headers=None, comment=None):
        assert isinstance(headers, (type(None), list))
        headers = headers or []
        location = header_value(headers, 'location')
        if not location:
            location = detail
            detail = ''
            headers.append(('location', location))
        assert location, 'HTTPRedirection specified neither a location in the headers nor did it provide a detail argument.'
        HTTPRedirection.__init__(self, location, headers, comment)
        if detail is not None:
            self.detail = detail
        return

    def relative_redirect(cls, dest_uri, environ, detail=None, headers=None, comment=None):
        """
        Create a redirect object with the dest_uri, which may be relative,
        considering it relative to the uri implied by the given environ.
        """
        location = resolve_relative_url(dest_uri, environ)
        headers = headers or []
        headers.append(('Location', location))
        return cls(detail=detail, headers=headers, comment=comment)

    relative_redirect = classmethod(relative_redirect)

    def location(self):
        for (name, value) in self.headers:
            if name.lower() == 'location':
                return value
        else:
            raise KeyError('No location set for %s' % self)


class HTTPMultipleChoices(_HTTPMove):
    code = 300
    title = 'Multiple Choices'


class HTTPMovedPermanently(_HTTPMove):
    code = 301
    title = 'Moved Permanently'


class HTTPFound(_HTTPMove):
    code = 302
    title = 'Found'
    explanation = 'The resource was found at'


class HTTPSeeOther(_HTTPMove):
    code = 303
    title = 'See Other'


class HTTPNotModified(HTTPRedirection):
    code = 304
    title = 'Not Modified'
    message = ''

    def plain(self, environ):
        return ''

    def html(self, environ):
        """ text/html representation of the exception """
        return ''


class HTTPUseProxy(_HTTPMove):
    code = 305
    title = 'Use Proxy'
    explanation = 'The resource must be accessed through a proxy located at'


class HTTPTemporaryRedirect(_HTTPMove):
    code = 307
    title = 'Temporary Redirect'


class HTTPClientError(HTTPError):
    """
    base class for the 400's, where the client is in-error

    This is an error condition in which the client is presumed to be
    in-error.  This is an expected problem, and thus is not considered
    a bug.  A server-side traceback is not warranted.  Unless specialized,
    this is a '400 Bad Request'
    """
    code = 400
    title = 'Bad Request'
    explanation = 'The server could not comply with the request since\r\nit is either malformed or otherwise incorrect.\r\n'


class HTTPBadRequest(HTTPClientError):
    pass


class HTTPUnauthorized(HTTPClientError):
    code = 401
    title = 'Unauthorized'
    explanation = 'This server could not verify that you are authorized to\r\naccess the document you requested.  Either you supplied the\r\nwrong credentials (e.g., bad password), or your browser\r\ndoes not understand how to supply the credentials required.\r\n'


class HTTPPaymentRequired(HTTPClientError):
    code = 402
    title = 'Payment Required'
    explanation = 'Access was denied for financial reasons.'


class HTTPForbidden(HTTPClientError):
    code = 403
    title = 'Forbidden'
    explanation = 'Access was denied to this resource.'


class HTTPNotFound(HTTPClientError):
    code = 404
    title = 'Not Found'
    explanation = 'The resource could not be found.'


class HTTPMethodNotAllowed(HTTPClientError):
    required_headers = ('allow', )
    code = 405
    title = 'Method Not Allowed'
    template = 'The method %(REQUEST_METHOD)s is not allowed for this resource.\r\n%(detail)s'


class HTTPNotAcceptable(HTTPClientError):
    code = 406
    title = 'Not Acceptable'
    template = 'The resource could not be generated that was acceptable to your browser (content\r\nof type %(HTTP_ACCEPT)s).\r\n%(detail)s'


class HTTPProxyAuthenticationRequired(HTTPClientError):
    code = 407
    title = 'Proxy Authentication Required'
    explanation = 'Authentication /w a local proxy is needed.'


class HTTPRequestTimeout(HTTPClientError):
    code = 408
    title = 'Request Timeout'
    explanation = 'The server has waited too long for the request to be sent by the client.'


class HTTPConflict(HTTPClientError):
    code = 409
    title = 'Conflict'
    explanation = 'There was a conflict when trying to complete your request.'


class HTTPGone(HTTPClientError):
    code = 410
    title = 'Gone'
    explanation = 'This resource is no longer available.  No forwarding address is given.'


class HTTPLengthRequired(HTTPClientError):
    code = 411
    title = 'Length Required'
    explanation = 'Content-Length header required.'


class HTTPPreconditionFailed(HTTPClientError):
    code = 412
    title = 'Precondition Failed'
    explanation = 'Request precondition failed.'


class HTTPRequestEntityTooLarge(HTTPClientError):
    code = 413
    title = 'Request Entity Too Large'
    explanation = 'The body of your request was too large for this server.'


class HTTPRequestURITooLong(HTTPClientError):
    code = 414
    title = 'Request-URI Too Long'
    explanation = 'The request URI was too long for this server.'


class HTTPUnsupportedMediaType(HTTPClientError):
    code = 415
    title = 'Unsupported Media Type'
    template = 'The request media type %(CONTENT_TYPE)s is not supported by this server.\r\n%(detail)s'


class HTTPRequestRangeNotSatisfiable(HTTPClientError):
    code = 416
    title = 'Request Range Not Satisfiable'
    explanation = 'The Range requested is not available.'


class HTTPExpectationFailed(HTTPClientError):
    code = 417
    title = 'Expectation Failed'
    explanation = 'Expectation failed.'


class HTTPServerError(HTTPError):
    """
    base class for the 500's, where the server is in-error

    This is an error condition in which the server is presumed to be
    in-error.  This is usually unexpected, and thus requires a traceback;
    ideally, opening a support ticket for the customer. Unless specialized,
    this is a '500 Internal Server Error'
    """
    code = 500
    title = 'Internal Server Error'
    explanation = 'The server has either erred or is incapable of performing\r\nthe requested operation.\r\n'


class HTTPInternalServerError(HTTPServerError):
    pass


class HTTPNotImplemented(HTTPServerError):
    code = 501
    title = 'Not Implemented'
    template = 'The request method %(REQUEST_METHOD)s is not implemented for this server.\r\n%(detail)s'


class HTTPBadGateway(HTTPServerError):
    code = 502
    title = 'Bad Gateway'
    explanation = 'Bad gateway.'


class HTTPServiceUnavailable(HTTPServerError):
    code = 503
    title = 'Service Unavailable'
    explanation = 'The server is currently unavailable. Please try again at a later time.'


class HTTPGatewayTimeout(HTTPServerError):
    code = 504
    title = 'Gateway Timeout'
    explanation = 'The gateway has timed out.'


class HTTPVersionNotSupported(HTTPServerError):
    code = 505
    title = 'HTTP Version Not Supported'
    explanation = 'The HTTP version is not supported.'


__all__ = [
 'HTTPException', 'HTTPRedirection', 'HTTPError']
_exceptions = {}
for (name, value) in globals().items():
    if isinstance(value, (type, types.ClassType)) and issubclass(value, HTTPException) and value.code:
        _exceptions[value.code] = value
        __all__.append(name)

def get_exception(code):
    return _exceptions[code]


class HTTPExceptionHandler(object):
    """
    catches exceptions and turns them into proper HTTP responses

    This middleware catches any exceptions (which are subclasses of
    ``HTTPException``) and turns them into proper HTTP responses.
    Note if the headers have already been sent, the stack trace is
    always maintained as this indicates a programming error.

    Note that you must raise the exception before returning the
    app_iter, and you cannot use this with generator apps that don't
    raise an exception until after their app_iter is iterated over.
    """

    def __init__(self, application, warning_level=None):
        assert not warning_level or warning_level > 99 and warning_level < 600
        if warning_level is not None:
            import warnings
            warnings.warn('The warning_level parameter is not used or supported', DeprecationWarning, 2)
        self.warning_level = warning_level or 500
        self.application = application
        return

    def __call__(self, environ, start_response):
        environ['paste.httpexceptions'] = self
        environ.setdefault('paste.expected_exceptions', []).append(HTTPException)
        try:
            return self.application(environ, start_response)
        except HTTPException, exc:
            return exc(environ, start_response)


def middleware(*args, **kw):
    import warnings
    warnings.warn('httpexceptions.middleware is deprecated; use make_middleware or HTTPExceptionHandler instead', DeprecationWarning, 2)
    return make_middleware(*args, **kw)


def make_middleware(app, global_conf=None, warning_level=None):
    """
    ``httpexceptions`` middleware; this catches any
    ``paste.httpexceptions.HTTPException`` exceptions (exceptions like
    ``HTTPNotFound``, ``HTTPMovedPermanently``, etc) and turns them
    into proper HTTP responses.

    ``warning_level`` can be an integer corresponding to an HTTP code.
    Any code over that value will be passed 'up' the chain, potentially
    reported on by another piece of middleware.
    """
    if warning_level:
        warning_level = int(warning_level)
    return HTTPExceptionHandler(app, warning_level=warning_level)


__all__.extend(['HTTPExceptionHandler', 'get_exception'])