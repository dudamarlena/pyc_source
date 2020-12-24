# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mrdon/dev/flask-async/venv/lib/python3.3/site-packages/flask/views.py
# Compiled at: 2014-01-20 12:41:11
# Size of source mod 2**32: 5642 bytes
"""
    flask.views
    ~~~~~~~~~~~

    This module provides class-based views inspired by the ones in Django.

    :copyright: (c) 2014 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
from .globals import request
from ._compat import with_metaclass
http_method_funcs = frozenset(['get', 'post', 'head', 'options',
 'delete', 'put', 'trace', 'patch'])

class View(object):
    __doc__ = "Alternative way to use view functions.  A subclass has to implement\n    :meth:`dispatch_request` which is called with the view arguments from\n    the URL routing system.  If :attr:`methods` is provided the methods\n    do not have to be passed to the :meth:`~flask.Flask.add_url_rule`\n    method explicitly::\n\n        class MyView(View):\n            methods = ['GET']\n\n            def dispatch_request(self, name):\n                return 'Hello %s!' % name\n\n        app.add_url_rule('/hello/<name>', view_func=MyView.as_view('myview'))\n\n    When you want to decorate a pluggable view you will have to either do that\n    when the view function is created (by wrapping the return value of\n    :meth:`as_view`) or you can use the :attr:`decorators` attribute::\n\n        class SecretView(View):\n            methods = ['GET']\n            decorators = [superuser_required]\n\n            def dispatch_request(self):\n                ...\n\n    The decorators stored in the decorators list are applied one after another\n    when the view function is created.  Note that you can *not* use the class\n    based decorators since those would decorate the view class and not the\n    generated view function!\n    "
    methods = None
    decorators = []

    def dispatch_request(self):
        """Subclasses have to override this method to implement the
        actual view function code.  This method is called with all
        the arguments from the URL rule.
        """
        raise NotImplementedError()

    @classmethod
    def as_view(cls, name, *class_args, **class_kwargs):
        """Converts the class into an actual view function that can be used
        with the routing system.  Internally this generates a function on the
        fly which will instantiate the :class:`View` on each request and call
        the :meth:`dispatch_request` method on it.

        The arguments passed to :meth:`as_view` are forwarded to the
        constructor of the class.
        """

        def view(*args, **kwargs):
            self = view.view_class(*class_args, **class_kwargs)
            return self.dispatch_request(*args, **kwargs)

        if cls.decorators:
            view.__name__ = name
            view.__module__ = cls.__module__
            for decorator in cls.decorators:
                view = decorator(view)

        view.view_class = cls
        view.__name__ = name
        view.__doc__ = cls.__doc__
        view.__module__ = cls.__module__
        view.methods = cls.methods
        return view


class MethodViewType(type):

    def __new__(cls, name, bases, d):
        rv = type.__new__(cls, name, bases, d)
        if 'methods' not in d:
            methods = set(rv.methods or [])
            for key in d:
                if key in http_method_funcs:
                    methods.add(key.upper())
                    continue

            if methods:
                rv.methods = sorted(methods)
        return rv


class MethodView(with_metaclass(MethodViewType, View)):
    __doc__ = "Like a regular class-based view but that dispatches requests to\n    particular methods.  For instance if you implement a method called\n    :meth:`get` it means you will response to ``'GET'`` requests and\n    the :meth:`dispatch_request` implementation will automatically\n    forward your request to that.  Also :attr:`options` is set for you\n    automatically::\n\n        class CounterAPI(MethodView):\n\n            def get(self):\n                return session.get('counter', 0)\n\n            def post(self):\n                session['counter'] = session.get('counter', 0) + 1\n                return 'OK'\n\n        app.add_url_rule('/counter', view_func=CounterAPI.as_view('counter'))\n    "

    def dispatch_request(self, *args, **kwargs):
        meth = getattr(self, request.method.lower(), None)
        if meth is None:
            if request.method == 'HEAD':
                meth = getattr(self, 'get', None)
        assert meth is not None, 'Unimplemented method %r' % request.method
        return meth(*args, **kwargs)