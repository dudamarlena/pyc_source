# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pocoo/http.py
# Compiled at: 2006-12-26 17:18:07
"""
    pocoo.http
    ~~~~~~~~~~

    HTTP Objects: request and response.

    Basically, a `pocoo.application.RequestHandler` component
    is passed a `Request` instance and must return a `Response`
    instance.  This response is then written back to the web server.

    There are various types of special responses, see the
    individual classes for details.  The most important one
    is the `TemplateResponse` which renders a template to a
    new response.

    :copyright: 2006 by Armin Ronacher.
    :license: GNU GPL, see LICENSE for more details.
"""
from colubrid.request import Request as ColubridRequest
from colubrid.response import HttpResponse as ColubridHttpResponse
from pocoo.utils.net import make_url_context_external

class Request(ColubridRequest):
    """
    Represents one HTTP request.

    :Ivariables:
      `ctx` : `pocoo.context.ApplicationContext`
        Application context for this request.
      `path` : string
        Request path info, relative to the Pocoo root path.
      `method` : string
        Request method ("GET" or "POST").
      `environ` : mapping
        WSGI environment for the request
      `gettext` : callable with one parameter
        translation function for current user language
        (set in `pocoo.pkg.core.i18n`)
      `session` : mapping
        session for current user (set in `pocoo.pkg.core.session`)
    """
    __module__ = __name__

    def __init__(self, environ, start_response, ctx):
        super(Request, self).__init__(environ, start_response, ctx.charset)
        self.path = environ.get('PATH_INFO', '').lstrip('/')
        self.method = environ['REQUEST_METHOD']
        self.handler = None
        self.ctx = ctx
        return

    def __repr__(self):
        path = self.path
        query = self.environ.get('QUERY_STRING')
        if query:
            path = '%s?%s' % (path, query)
        return '<%s %r>' % (self.__class__.__name__, path)


class DirectResponse(Exception):
    """
    Raise this exception if you want to cancel all further request
    processing, directly sending a response. Use::

        raise DirectResponse(Response(...))
    """
    __module__ = __name__

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.args[0])


class Response(ColubridHttpResponse):
    """
    Base for a HTTP Response, use this response type to return a
    simple string of data.
    """
    __module__ = __name__

    def __repr__(self):
        headers = [ k for (k, _) in self.headers.get() ]
        return '<%s %r, %d>' % (self.__class__.__name__, headers, self.status)


class TemplateResponse(Response):
    """
    Use this response type to return a rendered template.

    Usage example::

        from pocoo.http import TemplateResponse
        from pocoo.application import RequestHandler

        class TestPage(RequestHandler):

            handler_regexes = [u'testpage$']

            def handle_request(self, req):
                return TemplateResponse('testpage',
                    key='value',
                    iterable=['list', 'of', 'items']
                )
    """
    __module__ = __name__

    def __init__(self, _templatename_, **context):
        """
        :param _templatename_: Name of the template to render.
        :param context: Variables to add to the template's context.
        """
        super(TemplateResponse, self).__init__([])
        self.templatename = _templatename_
        self.context = context

    def __call__(self, req):
        from pocoo.template import render_template
        self.response = render_template(req, self.templatename, self.context)
        return super(TemplateResponse, self).__call__(req)


class PageNotFound(TemplateResponse):
    """
    Return this response to signal a 404 error.
    """
    __module__ = __name__

    def __init__(self):
        super(PageNotFound, self).__init__('errors/error_404.html')
        self.status = 404

    def __call__(self, req):
        self.context['page'] = req.environ.get('APPLICATION_REQUEST', '')
        return super(PageNotFound, self).__call__(req)


class PageMoved(TemplateResponse):
    """
    Return this response to signal a permanent redirect.
    """
    __module__ = __name__

    def __init__(self, url, local=False):
        super(PageMoved, self).__init__('errors/error_301.html')
        self.status = 301
        self.url = url
        self.local = local

    def __call__(self, req):
        try:
            url = make_url_context_external(req.ctx, self.url)
        except ValueError:
            if self.local:
                return BadRequest()(req)
            url = req.ctx.make_external_url(self.url)

        self['Location'] = url
        self.context['old_url'] = req.path
        self.context['new_url'] = url
        return super(PageMoved, self).__call__(req)


class AccessDeniedResponse(TemplateResponse):
    """
    Return this response to signal "access denied".
    """
    __module__ = __name__

    def __init__(self):
        super(AccessDeniedResponse, self).__init__('errors/error_403.html')
        self.status = 403

    def __call__(self, req):
        loginurl = req.ctx.make_url('login', next=req.path)
        self.context['path'] = req.path
        self.context['loginurl'] = loginurl
        return super(AccessDeniedResponse, self).__call__(req)


class HttpRedirect(TemplateResponse):
    """
    Return this response to signal a temporary redirect.
    """
    __module__ = __name__

    def __init__(self, url, local=True):
        super(HttpRedirect, self).__init__('errors/error_302.html')
        self.status = 302
        self.url = url
        self.local = local

    def __call__(self, req):
        try:
            url = make_url_context_external(req.ctx, self.url)
        except ValueError:
            if self.local:
                return BadRequest()(req)
            url = self.url

        self['Location'] = url
        self.context['old_url'] = req.path
        self.context['new_url'] = url
        return super(HttpRedirect, self).__call__(req)


class BadRequest(TemplateResponse):
    """
    Return this response to signal a bad request (HTTP protocol error).
    """
    __module__ = __name__

    def __init__(self):
        super(BadRequest, self).__init__('errors/error_400.html')
        self.status = 400


class InternalServerError(TemplateResponse):
    """
    Return this response to signal "internal server error", i.e.
    a script failure.
    """
    __module__ = __name__

    def __init__(self):
        super(InternalServerError, self).__init__('errors/error_500.html')
        self.status = 500