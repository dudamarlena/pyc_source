# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pocoo/application.py
# Compiled at: 2006-12-26 17:18:07
__doc__ = '\n    pocoo.application\n    ~~~~~~~~~~~~~~~~~\n\n    Pocoo WSGI application and base component types.\n\n    :copyright: 2006 by Armin Ronacher, Georg Brandl.\n    :license: GNU GPL, see LICENSE for more details.\n'
import re, time, urllib
from pocoo import Component
from pocoo.http import Request, Response, DirectResponse, PageNotFound, PageMoved
from pocoo.utils.debug import dtk

class RequestHandler(Component):
    """
    Component for URL <-> handler mapping.

    For each request, `Pocoo.__call__` loops through the
    `handler_regexes` of all registered `RequestHandler` components
    and calls `handle_request` on the first match.
    """
    __module__ = __name__
    handler_regexes = None

    def handle_request(self, req, *args):
        """
        Called if the current request path matches one of the
        `handler_regexes`.

        In all normal cases this must return a `pocoo.http.Response`
        (or a subclass thereof) or raise `pocoo.http.DirectResponse`.
        It can also return ``None`` to signal "page not found".
        """
        pass


class RequestWrapper(Component):
    """
    RequestWrappers process the request before it is given
    to the RequestHandler and process the response before
    it is given back to Colubrid.
    """
    __module__ = __name__

    def process_request(self, req):
        """
        Process the request.

        Can return a Response to bypass further request handling
        (especially any `pocoo.application.RequestHandler` components),
        else ``None``.
        """
        pass

    def process_response(self, req, resp):
        """
        Process the response.

        Must return the same or a new response object.
        """
        pass

    def get_priority(self):
        """
        Return an integer priority that indicates when the RequestWrapper
        should be applied:

        1
          before all others on request, after all others on response
        100
          after all others on request, before all others on response

        Levels 1 to 10 are reserved for pocoo core.
        """
        pass


class LinkableMixin(object):
    """
    Provides support for easy link creation.
    """
    __module__ = __name__
    relative_url = ''

    @property
    def external_url(self):
        return '%s%s%s' % (self.ctx.servername, self.ctx.scriptname, self.relative_url)

    @property
    def url(self):
        return '%s%s' % (self.ctx.scriptname, self.relative_url)


class Pocoo(object):
    """
    The main Pocoo WSGI application.
    """
    __module__ = __name__
    url_wrappers = None
    url_mapping = None

    def __init__(self, ctx):
        """
        Setup the application.

        This is done after all components are registered, so we can already
        collect the RequestHandlers here.
        """
        self.ctx = ctx
        mapping = {}
        for comp in ctx.get_components(RequestHandler):
            for regex in comp.handler_regexes:
                if not isinstance(regex, basestring):
                    (regex, args) = regex
                else:
                    args = {}
                mapping[(re.compile(regex), regex)] = (
                 comp, args)

        self.url_mapping = mapping
        self.url_wrappers = ctx.get_components(RequestWrapper)
        self.url_wrappers.sort(key=lambda wr: wr.get_priority() or 100)

    def __call__(self, environ, start_response):
        """
        The main request dispatching machinery.

        This tries to call `RequestHandler.handle_request` on the first
        RequestHandler for which one of the handler regexes matches the
        relative part of the request URL.
        Additionally, it calls the ``process_request`` and ``process_response``
        methods of `RequestWrapper` components in the right order.
        If it doesn't find a handler, a 404 response is returned.
        """
        req = Request(environ, start_response, self.ctx)
        environ['colubrid.request'] = req
        t_1 = time.time()
        if req.path.split('/')[(-1)] == 'favicon.ico':
            return Response('', status=404)(req)
        for wrapper in self.url_wrappers:
            ret = wrapper.process_request(req)
            if isinstance(ret, Response):
                return ret(req)

        if not req.environ.get('PATH_INFO', '').startswith('/'):
            resp = PageMoved('')
        else:
            try:
                for ((r, _), (handler, default)) in self.url_mapping.iteritems():
                    m = r.match(req.path)
                    if m is None:
                        continue
                    args = m.groupdict()
                    args.update(default)
                    resp = handler.handle_request(req, **args)
                    if resp is None:
                        resp = PageNotFound()
                    break
                else:
                    resp = PageNotFound()

            except DirectResponse, exc:
                resp = exc.args[0]

            if resp.status == 404 and not req.path.endswith('/'):
                test = req.path + '/'
                for ((regex, _), _) in self.url_mapping.iteritems():
                    if regex.match(test) is not None:
                        url = ('').join([urllib.quote(environ.get('SCRIPT_NAME', '')), urllib.quote(environ.get('PATH_INFO', ''))])
                        query = environ.get('QUERY_STRING', '')
                        if query:
                            url = '%s/?%s' % (url, query)
                        else:
                            url += '/'
                        resp = PageMoved(url)
                        break

        for wrapper in reversed(self.url_wrappers):
            resp = wrapper.process_response(req, resp)

        t_2 = time.time()
        dtk.log('app', 'handled request to %r in %0.5f sec', req.path, t_2 - t_1)
        return resp(req)


def setup_app(ctx):
    """
    Create the application object, wrap it in the requested debug middleware
    and return it to the context.

    Also wrap the application in all middlewares registered to the context
    via ``register_middleware`` or ``package.conf`` files.
    """
    app = Pocoo(ctx)
    debug = ctx.cfg.get_bool('development', 'debug', False)
    evalex = debug and ctx.cfg.get_bool('development', 'enable_evalexception', False)
    if debug:
        from colubrid.debug import DebuggedApplication
        app = DebuggedApplication(app, evalex)
    for mware in ctx.middlewares:
        app = mware(app, ctx)

    return app