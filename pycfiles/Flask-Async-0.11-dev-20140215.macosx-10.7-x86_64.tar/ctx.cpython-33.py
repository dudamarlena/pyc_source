# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mrdon/dev/flask-async/venv/lib/python3.3/site-packages/flask/ctx.py
# Compiled at: 2014-02-15 13:00:30
# Size of source mod 2**32: 14667 bytes
"""
    flask.ctx
    ~~~~~~~~~

    Implements the objects required to keep the context.

    :copyright: (c) 2014 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
from __future__ import with_statement
import sys
from functools import update_wrapper
from werkzeug.exceptions import HTTPException
from .globals import _request_ctx_stack, _app_ctx_stack
from .module import blueprint_is_module
from .signals import appcontext_pushed, appcontext_popped
from ._compat import BROKEN_PYPY_CTXMGR_EXIT, reraise

class _AppCtxGlobals(object):
    __doc__ = 'A plain object.'

    def get(self, name, default=None):
        return self.__dict__.get(name, default)

    def __contains__(self, item):
        return item in self.__dict__

    def __iter__(self):
        return iter(self.__dict__)

    def __repr__(self):
        top = _app_ctx_stack.top
        if top is not None:
            return '<flask.g of %r>' % top.app.name
        else:
            return object.__repr__(self)


def after_this_request(f):
    """Executes a function after this request.  This is useful to modify
    response objects.  The function is passed the response object and has
    to return the same or a new one.

    Example::

        @app.route('/')
        def index():
            @after_this_request
            def add_header(response):
                response.headers['X-Foo'] = 'Parachute'
                return response
            return 'Hello World!'

    This is more useful if a function other than the view function wants to
    modify a response.  For instance think of a decorator that wants to add
    some headers without converting the return value into a response object.

    .. versionadded:: 0.9
    """
    _request_ctx_stack.top._after_request_functions.append(f)
    return f


def copy_current_request_context(f):
    """A helper function that decorates a function to retain the current
    request context.  This is useful when working with greenlets.  The moment
    the function is decorated a copy of the request context is created and
    then pushed when the function is called.

    Example::

        import gevent
        from flask import copy_current_request_context

        @app.route('/')
        def index():
            @copy_current_request_context
            def do_some_work():
                # do some work here, it can access flask.request like you
                # would otherwise in the view function.
                ...
            gevent.spawn(do_some_work)
            return 'Regular response'

    .. versionadded:: 0.10
    """
    top = _request_ctx_stack.top
    if top is None:
        raise RuntimeError('This decorator can only be used at local scopes when a request context is on the stack.  For instance within view functions.')
    reqctx = top.copy()

    def wrapper(*args, **kwargs):
        with reqctx:
            return f(*args, **kwargs)

    return update_wrapper(wrapper, f)


def has_request_context():
    """If you have code that wants to test if a request context is there or
    not this function can be used.  For instance, you may want to take advantage
    of request information if the request object is available, but fail
    silently if it is unavailable.

    ::

        class User(db.Model):

            def __init__(self, username, remote_addr=None):
                self.username = username
                if remote_addr is None and has_request_context():
                    remote_addr = request.remote_addr
                self.remote_addr = remote_addr

    Alternatively you can also just test any of the context bound objects
    (such as :class:`request` or :class:`g` for truthness)::

        class User(db.Model):

            def __init__(self, username, remote_addr=None):
                self.username = username
                if remote_addr is None and request:
                    remote_addr = request.remote_addr
                self.remote_addr = remote_addr

    .. versionadded:: 0.7
    """
    return _request_ctx_stack.top is not None


def has_app_context():
    """Works like :func:`has_request_context` but for the application
    context.  You can also just do a boolean check on the
    :data:`current_app` object instead.

    .. versionadded:: 0.9
    """
    return _app_ctx_stack.top is not None


class AppContext(object):
    __doc__ = 'The application context binds an application object implicitly\n    to the current thread or greenlet, similar to how the\n    :class:`RequestContext` binds request information.  The application\n    context is also implicitly created if a request context is created\n    but the application is not on top of the individual application\n    context.\n    '

    def __init__(self, app):
        self.app = app
        self.url_adapter = app.create_url_adapter(None)
        self.g = app.app_ctx_globals_class()
        self._refcnt = 0
        return

    def push(self):
        """Binds the app context to the current context."""
        self._refcnt += 1
        if hasattr(sys, 'exc_clear'):
            sys.exc_clear()
        _app_ctx_stack.push(self)
        appcontext_pushed.send(self.app)

    def pop(self, exc=None):
        """Pops the app context."""
        self._refcnt -= 1
        if self._refcnt <= 0:
            if exc is None:
                exc = sys.exc_info()[1]
            self.app.do_teardown_appcontext(exc)
        rv = _app_ctx_stack.pop()
        assert rv is self, 'Popped wrong app context.  (%r instead of %r)' % (
         rv, self)
        appcontext_popped.send(self.app)
        return

    def __enter__(self):
        self.push()
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.pop(exc_value)
        if BROKEN_PYPY_CTXMGR_EXIT:
            if exc_type is not None:
                reraise(exc_type, exc_value, tb)
        return


class RequestContext(object):
    __doc__ = "The request context contains all request relevant information.  It is\n    created at the beginning of the request and pushed to the\n    `_request_ctx_stack` and removed at the end of it.  It will create the\n    URL adapter and request object for the WSGI environment provided.\n\n    Do not attempt to use this class directly, instead use\n    :meth:`~flask.Flask.test_request_context` and\n    :meth:`~flask.Flask.request_context` to create this object.\n\n    When the request context is popped, it will evaluate all the\n    functions registered on the application for teardown execution\n    (:meth:`~flask.Flask.teardown_request`).\n\n    The request context is automatically popped at the end of the request\n    for you.  In debug mode the request context is kept around if\n    exceptions happen so that interactive debuggers have a chance to\n    introspect the data.  With 0.4 this can also be forced for requests\n    that did not fail and outside of `DEBUG` mode.  By setting\n    ``'flask._preserve_context'`` to `True` on the WSGI environment the\n    context will not pop itself at the end of the request.  This is used by\n    the :meth:`~flask.Flask.test_client` for example to implement the\n    deferred cleanup functionality.\n\n    You might find this helpful for unittests where you need the\n    information from the context local around for a little longer.  Make\n    sure to properly :meth:`~werkzeug.LocalStack.pop` the stack yourself in\n    that situation, otherwise your unittests will leak memory.\n    "

    def __init__(self, app, environ, request=None):
        self.app = app
        if request is None:
            request = app.request_class(environ)
        self.request = request
        self.url_adapter = app.create_url_adapter(self.request)
        self.flashes = None
        self.session = None
        self._implicit_app_ctx_stack = []
        self.preserved = False
        self._preserved_exc = None
        self._after_request_functions = []
        self.match_request()
        blueprint = self.request.blueprint
        if blueprint is not None:
            bp = app.blueprints.get(blueprint)
            if bp is not None:
                if blueprint_is_module(bp):
                    self.request._is_old_module = True
        return

    def _get_g(self):
        return _app_ctx_stack.top.g

    def _set_g(self, value):
        _app_ctx_stack.top.g = value

    g = property(_get_g, _set_g)
    del _get_g
    del _set_g

    def copy(self):
        """Creates a copy of this request context with the same request object.
        This can be used to move a request context to a different greenlet.
        Because the actual request object is the same this cannot be used to
        move a request context to a different thread unless access to the
        request object is locked.

        .. versionadded:: 0.10
        """
        return self.__class__(self.app, environ=self.request.environ, request=self.request)

    def match_request(self):
        """Can be overridden by a subclass to hook into the matching
        of the request.
        """
        try:
            url_rule, self.request.view_args = self.url_adapter.match(return_rule=True)
            self.request.url_rule = url_rule
        except HTTPException as e:
            self.request.routing_exception = e

    def push(self):
        """Binds the request context to the current context."""
        top = _request_ctx_stack.top
        if top is not None:
            if top.preserved:
                top.pop(top._preserved_exc)
        app_ctx = _app_ctx_stack.top
        if app_ctx is None or app_ctx.app != self.app:
            app_ctx = self.app.app_context()
            app_ctx.push()
            self._implicit_app_ctx_stack.append(app_ctx)
        else:
            self._implicit_app_ctx_stack.append(None)
        if hasattr(sys, 'exc_clear'):
            sys.exc_clear()
        _request_ctx_stack.push(self)
        self.session = self.app.open_session(self.request)
        if self.session is None:
            self.session = self.app.make_null_session()
        return

    def pop(self, exc=None):
        """Pops the request context and unbinds it by doing that.  This will
        also trigger the execution of functions registered by the
        :meth:`~flask.Flask.teardown_request` decorator.

        .. versionchanged:: 0.9
           Added the `exc` argument.
        """
        app_ctx = self._implicit_app_ctx_stack.pop()
        clear_request = False
        if not self._implicit_app_ctx_stack:
            self.preserved = False
            self._preserved_exc = None
            if exc is None:
                exc = sys.exc_info()[1]
            self.app.do_teardown_request(exc)
            if hasattr(sys, 'exc_clear'):
                sys.exc_clear()
            request_close = getattr(self.request, 'close', None)
            if request_close is not None:
                request_close()
            clear_request = True
        rv = _request_ctx_stack.pop()
        assert rv is self, 'Popped wrong request context.  (%r instead of %r)' % (
         rv, self)
        if clear_request:
            rv.request.environ['werkzeug.request'] = None
        if app_ctx is not None:
            app_ctx.pop(exc)
        return

    def auto_pop(self, exc):
        if self.request.environ.get('flask._preserve_context') or exc is not None and self.app.preserve_context_on_exception:
            self.preserved = True
            self._preserved_exc = exc
        else:
            self.pop(exc)
        return

    def __enter__(self):
        self.push()
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.auto_pop(exc_value)
        if BROKEN_PYPY_CTXMGR_EXIT:
            if exc_type is not None:
                reraise(exc_type, exc_value, tb)
        return

    def __repr__(self):
        return "<%s '%s' [%s] of %s>" % (
         self.__class__.__name__,
         self.request.url,
         self.request.method,
         self.app.name)