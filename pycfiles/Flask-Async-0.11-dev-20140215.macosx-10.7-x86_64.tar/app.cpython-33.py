# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mrdon/dev/flask-async/venv/lib/python3.3/site-packages/flask/app.py
# Compiled at: 2014-02-15 13:01:04
# Size of source mod 2**32: 77347 bytes
"""
    flask.app
    ~~~~~~~~~

    This module implements the central WSGI application object.

    :copyright: (c) 2014 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
import logging, os, sys
from threading import Lock
from datetime import timedelta
from itertools import chain
from functools import update_wrapper
import asyncio
from werkzeug.datastructures import ImmutableDict
from werkzeug.routing import Map, Rule, RequestRedirect, BuildError
from werkzeug.exceptions import HTTPException, InternalServerError, MethodNotAllowed, BadRequest
from .helpers import _PackageBoundObject, url_for, get_flashed_messages, locked_cached_property, _endpoint_from_view_func, find_package
from . import json
from werkzeug.utils import yields, call_maybe_yield
from .wrappers import Request, Response
from .config import ConfigAttribute, Config
from .ctx import RequestContext, AppContext, _AppCtxGlobals
from .globals import _request_ctx_stack, request, session, g
from .sessions import SecureCookieSessionInterface
from .module import blueprint_is_module
from .templating import DispatchingJinjaLoader, Environment, _default_template_ctx_processor
from .signals import request_started, request_finished, got_request_exception, request_tearing_down, appcontext_tearing_down
from ._compat import reraise, string_types, text_type, integer_types
_logger_lock = Lock()

def _make_timedelta(value):
    if not isinstance(value, timedelta):
        return timedelta(seconds=value)
    return value


def setupmethod(f):
    """Wraps a method so that it performs a check in debug mode if the
    first request was already handled.
    """

    def wrapper_func(self, *args, **kwargs):
        if self.debug:
            if self._got_first_request:
                raise AssertionError('A setup function was called after the first request was handled.  This usually indicates a bug in the application where a module was not imported and decorators or other functionality was called too late.\nTo fix this make sure to import all your view modules, database models and everything related at a central place before the application starts serving requests.')
        return f(self, *args, **kwargs)

    return update_wrapper(wrapper_func, f)


class Flask(_PackageBoundObject):
    __doc__ = "The flask object implements a WSGI application and acts as the central\n    object.  It is passed the name of the module or package of the\n    application.  Once it is created it will act as a central registry for\n    the view functions, the URL rules, template configuration and much more.\n\n    The name of the package is used to resolve resources from inside the\n    package or the folder the module is contained in depending on if the\n    package parameter resolves to an actual python package (a folder with\n    an `__init__.py` file inside) or a standard module (just a `.py` file).\n\n    For more information about resource loading, see :func:`open_resource`.\n\n    Usually you create a :class:`Flask` instance in your main module or\n    in the `__init__.py` file of your package like this::\n\n        from flask import Flask\n        app = Flask(__name__)\n\n    .. admonition:: About the First Parameter\n\n        The idea of the first parameter is to give Flask an idea what\n        belongs to your application.  This name is used to find resources\n        on the file system, can be used by extensions to improve debugging\n        information and a lot more.\n\n        So it's important what you provide there.  If you are using a single\n        module, `__name__` is always the correct value.  If you however are\n        using a package, it's usually recommended to hardcode the name of\n        your package there.\n\n        For example if your application is defined in `yourapplication/app.py`\n        you should create it with one of the two versions below::\n\n            app = Flask('yourapplication')\n            app = Flask(__name__.split('.')[0])\n\n        Why is that?  The application will work even with `__name__`, thanks\n        to how resources are looked up.  However it will make debugging more\n        painful.  Certain extensions can make assumptions based on the\n        import name of your application.  For example the Flask-SQLAlchemy\n        extension will look for the code in your application that triggered\n        an SQL query in debug mode.  If the import name is not properly set\n        up, that debugging information is lost.  (For example it would only\n        pick up SQL queries in `yourapplication.app` and not\n        `yourapplication.views.frontend`)\n\n    .. versionadded:: 0.7\n       The `static_url_path`, `static_folder`, and `template_folder`\n       parameters were added.\n\n    .. versionadded:: 0.8\n       The `instance_path` and `instance_relative_config` parameters were\n       added.\n\n    :param import_name: the name of the application package\n    :param static_url_path: can be used to specify a different path for the\n                            static files on the web.  Defaults to the name\n                            of the `static_folder` folder.\n    :param static_folder: the folder with static files that should be served\n                          at `static_url_path`.  Defaults to the ``'static'``\n                          folder in the root path of the application.\n    :param template_folder: the folder that contains the templates that should\n                            be used by the application.  Defaults to\n                            ``'templates'`` folder in the root path of the\n                            application.\n    :param instance_path: An alternative instance path for the application.\n                          By default the folder ``'instance'`` next to the\n                          package or module is assumed to be the instance\n                          path.\n    :param instance_relative_config: if set to `True` relative filenames\n                                     for loading the config are assumed to\n                                     be relative to the instance path instead\n                                     of the application root.\n    "
    request_class = Request
    response_class = Response
    app_ctx_globals_class = _AppCtxGlobals

    def _get_request_globals_class(self):
        return self.app_ctx_globals_class

    def _set_request_globals_class(self, value):
        from warnings import warn
        warn(DeprecationWarning('request_globals_class attribute is now called app_ctx_globals_class'))
        self.app_ctx_globals_class = value

    request_globals_class = property(_get_request_globals_class, _set_request_globals_class)
    del _get_request_globals_class
    del _set_request_globals_class
    debug = ConfigAttribute('DEBUG')
    testing = ConfigAttribute('TESTING')
    secret_key = ConfigAttribute('SECRET_KEY')
    session_cookie_name = ConfigAttribute('SESSION_COOKIE_NAME')
    permanent_session_lifetime = ConfigAttribute('PERMANENT_SESSION_LIFETIME', get_converter=_make_timedelta)
    use_x_sendfile = ConfigAttribute('USE_X_SENDFILE')
    logger_name = ConfigAttribute('LOGGER_NAME')
    enable_modules = True
    debug_log_format = '-' * 80 + '\n' + '%(levelname)s in %(module)s [%(pathname)s:%(lineno)d]:\n' + '%(message)s\n' + '-' * 80
    json_encoder = json.JSONEncoder
    json_decoder = json.JSONDecoder
    jinja_options = ImmutableDict(extensions=[
     'jinja2.ext.autoescape', 'jinja2.ext.with_'])
    default_config = ImmutableDict({'DEBUG': False, 
     'TESTING': False, 
     'PROPAGATE_EXCEPTIONS': None, 
     'PRESERVE_CONTEXT_ON_EXCEPTION': None, 
     'SECRET_KEY': None, 
     'PERMANENT_SESSION_LIFETIME': timedelta(days=31), 
     'USE_X_SENDFILE': False, 
     'LOGGER_NAME': None, 
     'SERVER_NAME': None, 
     'APPLICATION_ROOT': None, 
     'SESSION_COOKIE_NAME': 'session', 
     'SESSION_COOKIE_DOMAIN': None, 
     'SESSION_COOKIE_PATH': None, 
     'SESSION_COOKIE_HTTPONLY': True, 
     'SESSION_COOKIE_SECURE': False, 
     'SESSION_REFRESH_EACH_REQUEST': True, 
     'MAX_CONTENT_LENGTH': None, 
     'SEND_FILE_MAX_AGE_DEFAULT': 43200, 
     'TRAP_BAD_REQUEST_ERRORS': False, 
     'TRAP_HTTP_EXCEPTIONS': False, 
     'PREFERRED_URL_SCHEME': 'http', 
     'JSON_AS_ASCII': True, 
     'JSON_SORT_KEYS': True, 
     'JSONIFY_PRETTYPRINT_REGULAR': True})
    url_rule_class = Rule
    test_client_class = None
    session_interface = SecureCookieSessionInterface()

    def __init__(self, import_name, static_path=None, static_url_path=None, static_folder='static', template_folder='templates', instance_path=None, instance_relative_config=False):
        _PackageBoundObject.__init__(self, import_name, template_folder=template_folder)
        if static_path is not None:
            from warnings import warn
            warn(DeprecationWarning('static_path is now called static_url_path'), stacklevel=2)
            static_url_path = static_path
        if static_url_path is not None:
            self.static_url_path = static_url_path
        if static_folder is not None:
            self.static_folder = static_folder
        if instance_path is None:
            instance_path = self.auto_find_instance_path()
        elif not os.path.isabs(instance_path):
            raise ValueError('If an instance path is provided it must be absolute.  A relative path was given instead.')
        self.instance_path = instance_path
        self.config = self.make_config(instance_relative_config)
        self._logger = None
        self.logger_name = self.import_name
        self.view_functions = {}
        self._error_handlers = {}
        self.error_handler_spec = {None: self._error_handlers}
        self.url_build_error_handlers = []
        self.before_request_funcs = {}
        self.before_first_request_funcs = []
        self.after_request_funcs = {}
        self.teardown_request_funcs = {}
        self.teardown_appcontext_funcs = []
        self.url_value_preprocessors = {}
        self.url_default_functions = {}
        self.template_context_processors = {None: [
                _default_template_ctx_processor]}
        self.blueprints = {}
        self.extensions = {}
        self.url_map = Map()
        self._got_first_request = False
        self._before_request_lock = Lock()
        if self.has_static_folder:
            self.add_url_rule(self.static_url_path + '/<path:filename>', endpoint='static', view_func=self.send_static_file)
        return

    def _get_error_handlers(self):
        from warnings import warn
        warn(DeprecationWarning('error_handlers is deprecated, use the new error_handler_spec attribute instead.'), stacklevel=1)
        return self._error_handlers

    def _set_error_handlers(self, value):
        self._error_handlers = value
        self.error_handler_spec[None] = value
        return

    error_handlers = property(_get_error_handlers, _set_error_handlers)
    del _get_error_handlers
    del _set_error_handlers

    @locked_cached_property
    def name(self):
        """The name of the application.  This is usually the import name
        with the difference that it's guessed from the run file if the
        import name is main.  This name is used as a display name when
        Flask needs the name of the application.  It can be set and overridden
        to change the value.

        .. versionadded:: 0.8
        """
        if self.import_name == '__main__':
            fn = getattr(sys.modules['__main__'], '__file__', None)
            if fn is None:
                return '__main__'
            return os.path.splitext(os.path.basename(fn))[0]
        else:
            return self.import_name

    @property
    def propagate_exceptions(self):
        """Returns the value of the `PROPAGATE_EXCEPTIONS` configuration
        value in case it's set, otherwise a sensible default is returned.

        .. versionadded:: 0.7
        """
        rv = self.config['PROPAGATE_EXCEPTIONS']
        if rv is not None:
            return rv
        else:
            return self.testing or self.debug

    @property
    def preserve_context_on_exception(self):
        """Returns the value of the `PRESERVE_CONTEXT_ON_EXCEPTION`
        configuration value in case it's set, otherwise a sensible default
        is returned.

        .. versionadded:: 0.7
        """
        rv = self.config['PRESERVE_CONTEXT_ON_EXCEPTION']
        if rv is not None:
            return rv
        else:
            return self.debug

    @property
    def logger(self):
        """A :class:`logging.Logger` object for this application.  The
        default configuration is to log to stderr if the application is
        in debug mode.  This logger can be used to (surprise) log messages.
        Here some examples::

            app.logger.debug('A value for debugging')
            app.logger.warning('A warning occurred (%d apples)', 42)
            app.logger.error('An error occurred')

        .. versionadded:: 0.3
        """
        if self._logger and self._logger.name == self.logger_name:
            return self._logger
        with _logger_lock:
            if self._logger and self._logger.name == self.logger_name:
                return self._logger
            else:
                from flask.logging import create_logger
                self._logger = rv = create_logger(self)
                return rv

    @locked_cached_property
    def jinja_env(self):
        """The Jinja2 environment used to load templates."""
        return self.create_jinja_environment()

    @property
    def got_first_request(self):
        """This attribute is set to `True` if the application started
        handling the first request.

        .. versionadded:: 0.8
        """
        return self._got_first_request

    def make_config(self, instance_relative=False):
        """Used to create the config attribute by the Flask constructor.
        The `instance_relative` parameter is passed in from the constructor
        of Flask (there named `instance_relative_config`) and indicates if
        the config should be relative to the instance path or the root path
        of the application.

        .. versionadded:: 0.8
        """
        root_path = self.root_path
        if instance_relative:
            root_path = self.instance_path
        return Config(root_path, self.default_config)

    def auto_find_instance_path(self):
        """Tries to locate the instance path if it was not provided to the
        constructor of the application class.  It will basically calculate
        the path to a folder named ``instance`` next to your main file or
        the package.

        .. versionadded:: 0.8
        """
        prefix, package_path = find_package(self.import_name)
        if prefix is None:
            return os.path.join(package_path, 'instance')
        else:
            return os.path.join(prefix, 'var', self.name + '-instance')

    def open_instance_resource(self, resource, mode='rb'):
        """Opens a resource from the application's instance folder
        (:attr:`instance_path`).  Otherwise works like
        :meth:`open_resource`.  Instance resources can also be opened for
        writing.

        :param resource: the name of the resource.  To access resources within
                         subfolders use forward slashes as separator.
        :param mode: resource file opening mode, default is 'rb'.
        """
        return open(os.path.join(self.instance_path, resource), mode)

    def create_jinja_environment(self):
        """Creates the Jinja2 environment based on :attr:`jinja_options`
        and :meth:`select_jinja_autoescape`.  Since 0.7 this also adds
        the Jinja2 globals and filters after initialization.  Override
        this function to customize the behavior.

        .. versionadded:: 0.5
        """
        options = dict(self.jinja_options)
        if 'autoescape' not in options:
            options['autoescape'] = self.select_jinja_autoescape
        rv = Environment(self, **options)
        rv.globals.update(url_for=url_for, get_flashed_messages=get_flashed_messages, config=self.config, request=request, session=session, g=g)
        rv.filters['tojson'] = json.tojson_filter
        return rv

    def create_global_jinja_loader(self):
        """Creates the loader for the Jinja2 environment.  Can be used to
        override just the loader and keeping the rest unchanged.  It's
        discouraged to override this function.  Instead one should override
        the :meth:`jinja_loader` function instead.

        The global loader dispatches between the loaders of the application
        and the individual blueprints.

        .. versionadded:: 0.7
        """
        return DispatchingJinjaLoader(self)

    def init_jinja_globals(self):
        """Deprecated.  Used to initialize the Jinja2 globals.

        .. versionadded:: 0.5
        .. versionchanged:: 0.7
           This method is deprecated with 0.7.  Override
           :meth:`create_jinja_environment` instead.
        """
        pass

    def select_jinja_autoescape(self, filename):
        """Returns `True` if autoescaping should be active for the given
        template name.

        .. versionadded:: 0.5
        """
        if filename is None:
            return False
        else:
            return filename.endswith(('.html', '.htm', '.xml', '.xhtml'))

    def update_template_context(self, context):
        """Update the template context with some commonly used variables.
        This injects request, session, config and g into the template
        context as well as everything template context processors want
        to inject.  Note that the as of Flask 0.6, the original values
        in the context will not be overridden if a context processor
        decides to return a value with the same key.

        :param context: the context as a dictionary that is updated in place
                        to add extra variables.
        """
        funcs = self.template_context_processors[None]
        reqctx = _request_ctx_stack.top
        if reqctx is not None:
            bp = reqctx.request.blueprint
            if bp is not None:
                if bp in self.template_context_processors:
                    funcs = chain(funcs, self.template_context_processors[bp])
        orig_ctx = context.copy()
        for func in funcs:
            context.update(func())

        context.update(orig_ctx)
        return

    def run(self, host=None, port=None, debug=None, **options):
        """Runs the application on a local development server.  If the
        :attr:`debug` flag is set the server will automatically reload
        for code changes and show a debugger in case an exception happened.

        If you want to run the application in debug mode, but disable the
        code execution on the interactive debugger, you can pass
        ``use_evalex=False`` as parameter.  This will keep the debugger's
        traceback screen active, but disable code execution.

        .. admonition:: Keep in Mind

           Flask will suppress any server error with a generic error page
           unless it is in debug mode.  As such to enable just the
           interactive debugger without the code reloading, you have to
           invoke :meth:`run` with ``debug=True`` and ``use_reloader=False``.
           Setting ``use_debugger`` to `True` without being in debug mode
           won't catch any exceptions because there won't be any to
           catch.

        .. versionchanged:: 0.10
           The default port is now picked from the ``SERVER_NAME`` variable.

        :param host: the hostname to listen on. Set this to ``'0.0.0.0'`` to
                     have the server available externally as well. Defaults to
                     ``'127.0.0.1'``.
        :param port: the port of the webserver. Defaults to ``5000`` or the
                     port defined in the ``SERVER_NAME`` config variable if
                     present.
        :param debug: if given, enable or disable debug mode.
                      See :attr:`debug`.
        :param options: the options to be forwarded to the underlying
                        Werkzeug server.  See
                        :func:`werkzeug.serving.run_simple` for more
                        information.
        """
        from werkzeug.serving import run_simple
        if host is None:
            host = '127.0.0.1'
        if port is None:
            server_name = self.config['SERVER_NAME']
            if server_name and ':' in server_name:
                port = int(server_name.rsplit(':', 1)[1])
            else:
                port = 5000
        if debug is not None:
            self.debug = bool(debug)
        options.setdefault('use_reloader', self.debug)
        options.setdefault('use_debugger', self.debug)
        try:
            run_simple(host, port, self, **options)
        finally:
            self._got_first_request = False

        return

    def test_client(self, use_cookies=True):
        """Creates a test client for this application.  For information
        about unit testing head over to :ref:`testing`.

        Note that if you are testing for assertions or exceptions in your
        application code, you must set ``app.testing = True`` in order for the
        exceptions to propagate to the test client.  Otherwise, the exception
        will be handled by the application (not visible to the test client) and
        the only indication of an AssertionError or other exception will be a
        500 status code response to the test client.  See the :attr:`testing`
        attribute.  For example::

            app.testing = True
            client = app.test_client()

        The test client can be used in a `with` block to defer the closing down
        of the context until the end of the `with` block.  This is useful if
        you want to access the context locals for testing::

            with app.test_client() as c:
                rv = c.get('/?vodka=42')
                assert request.args['vodka'] == '42'

        See :class:`~flask.testing.FlaskClient` for more information.

        .. versionchanged:: 0.4
           added support for `with` block usage for the client.

        .. versionadded:: 0.7
           The `use_cookies` parameter was added as well as the ability
           to override the client to be used by setting the
           :attr:`test_client_class` attribute.
        """
        cls = self.test_client_class
        if cls is None:
            from flask.testing import FlaskClient as cls
        return cls(self, self.response_class, use_cookies=use_cookies)

    def open_session(self, request):
        """Creates or opens a new session.  Default implementation stores all
        session data in a signed cookie.  This requires that the
        :attr:`secret_key` is set.  Instead of overriding this method
        we recommend replacing the :class:`session_interface`.

        :param request: an instance of :attr:`request_class`.
        """
        return self.session_interface.open_session(self, request)

    def save_session(self, session, response):
        """Saves the session if it needs updates.  For the default
        implementation, check :meth:`open_session`.  Instead of overriding this
        method we recommend replacing the :class:`session_interface`.

        :param session: the session to be saved (a
                        :class:`~werkzeug.contrib.securecookie.SecureCookie`
                        object)
        :param response: an instance of :attr:`response_class`
        """
        return self.session_interface.save_session(self, session, response)

    def make_null_session(self):
        """Creates a new instance of a missing session.  Instead of overriding
        this method we recommend replacing the :class:`session_interface`.

        .. versionadded:: 0.7
        """
        return self.session_interface.make_null_session(self)

    def register_module(self, module, **options):
        """Registers a module with this application.  The keyword argument
        of this function are the same as the ones for the constructor of the
        :class:`Module` class and will override the values of the module if
        provided.

        .. versionchanged:: 0.7
           The module system was deprecated in favor for the blueprint
           system.
        """
        assert blueprint_is_module(module), 'register_module requires actual module objects.  Please upgrade to blueprints though.'
        if not self.enable_modules:
            raise RuntimeError('Module support was disabled but code attempted to register a module named %r' % module)
        else:
            from warnings import warn
            warn(DeprecationWarning('Modules are deprecated.  Upgrade to using blueprints.  Have a look into the documentation for more information.  If this module was registered by a Flask-Extension upgrade the extension or contact the author of that extension instead.  (Registered %r)' % module), stacklevel=2)
        self.register_blueprint(module, **options)

    @setupmethod
    def register_blueprint(self, blueprint, **options):
        """Registers a blueprint on the application.

        .. versionadded:: 0.7
        """
        first_registration = False
        if blueprint.name in self.blueprints:
            assert self.blueprints[blueprint.name] is blueprint, 'A blueprint\'s name collision occurred between %r and %r.  Both share the same name "%s".  Blueprints that are created on the fly need unique names.' % (
             blueprint, self.blueprints[blueprint.name], blueprint.name)
        else:
            self.blueprints[blueprint.name] = blueprint
            first_registration = True
        blueprint.register(self, options, first_registration)

    @setupmethod
    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        """Connects a URL rule.  Works exactly like the :meth:`route`
        decorator.  If a view_func is provided it will be registered with the
        endpoint.

        Basically this example::

            @app.route('/')
            def index():
                pass

        Is equivalent to the following::

            def index():
                pass
            app.add_url_rule('/', 'index', index)

        If the view_func is not provided you will need to connect the endpoint
        to a view function like so::

            app.view_functions['index'] = index

        Internally :meth:`route` invokes :meth:`add_url_rule` so if you want
        to customize the behavior via subclassing you only need to change
        this method.

        For more information refer to :ref:`url-route-registrations`.

        .. versionchanged:: 0.2
           `view_func` parameter added.

        .. versionchanged:: 0.6
           `OPTIONS` is added automatically as method.

        :param rule: the URL rule as string
        :param endpoint: the endpoint for the registered URL rule.  Flask
                         itself assumes the name of the view function as
                         endpoint
        :param view_func: the function to call when serving a request to the
                          provided endpoint
        :param options: the options to be forwarded to the underlying
                        :class:`~werkzeug.routing.Rule` object.  A change
                        to Werkzeug is handling of method options.  methods
                        is a list of methods this rule should be limited
                        to (`GET`, `POST` etc.).  By default a rule
                        just listens for `GET` (and implicitly `HEAD`).
                        Starting with Flask 0.6, `OPTIONS` is implicitly
                        added and handled by the standard request handling.
        """
        if endpoint is None:
            endpoint = _endpoint_from_view_func(view_func)
        options['endpoint'] = endpoint
        methods = options.pop('methods', None)
        if methods is None:
            methods = getattr(view_func, 'methods', None) or ('GET', )
        if isinstance(methods, string_types):
            raise TypeError('Allowed methods have to be iterables of strings, for example: @app.route(..., methods=["POST"])')
        methods = set(methods)
        required_methods = set(getattr(view_func, 'required_methods', ()))
        provide_automatic_options = getattr(view_func, 'provide_automatic_options', None)
        if provide_automatic_options is None:
            if 'OPTIONS' not in methods:
                provide_automatic_options = True
                required_methods.add('OPTIONS')
            else:
                provide_automatic_options = False
        methods |= required_methods
        rule = self.url_rule_class(rule, methods=methods, **options)
        rule.provide_automatic_options = provide_automatic_options
        self.url_map.add(rule)
        if view_func is not None:
            old_func = self.view_functions.get(endpoint)
            if old_func is not None:
                if old_func != view_func:
                    raise AssertionError('View function mapping is overwriting an existing endpoint function: %s' % endpoint)
            self.view_functions[endpoint] = view_func
        return

    def route(self, rule, **options):
        """A decorator that is used to register a view function for a
        given URL rule.  This does the same thing as :meth:`add_url_rule`
        but is intended for decorator usage::

            @app.route('/')
            def index():
                return 'Hello World'

        For more information refer to :ref:`url-route-registrations`.

        :param rule: the URL rule as string
        :param endpoint: the endpoint for the registered URL rule.  Flask
                         itself assumes the name of the view function as
                         endpoint
        :param options: the options to be forwarded to the underlying
                        :class:`~werkzeug.routing.Rule` object.  A change
                        to Werkzeug is handling of method options.  methods
                        is a list of methods this rule should be limited
                        to (`GET`, `POST` etc.).  By default a rule
                        just listens for `GET` (and implicitly `HEAD`).
                        Starting with Flask 0.6, `OPTIONS` is implicitly
                        added and handled by the standard request handling.
        """

        def decorator(f):
            endpoint = options.pop('endpoint', None)
            self.add_url_rule(rule, endpoint, f, **options)
            return f

        return decorator

    @setupmethod
    def endpoint(self, endpoint):
        """A decorator to register a function as an endpoint.
        Example::

            @app.endpoint('example.endpoint')
            def example():
                return "example"

        :param endpoint: the name of the endpoint
        """

        def decorator(f):
            self.view_functions[endpoint] = f
            return f

        return decorator

    @setupmethod
    def errorhandler(self, code_or_exception):
        """A decorator that is used to register a function give a given
        error code.  Example::

            @app.errorhandler(404)
            def page_not_found(error):
                return 'This page does not exist', 404

        You can also register handlers for arbitrary exceptions::

            @app.errorhandler(DatabaseError)
            def special_exception_handler(error):
                return 'Database connection failed', 500

        You can also register a function as error handler without using
        the :meth:`errorhandler` decorator.  The following example is
        equivalent to the one above::

            def page_not_found(error):
                return 'This page does not exist', 404
            app.error_handler_spec[None][404] = page_not_found

        Setting error handlers via assignments to :attr:`error_handler_spec`
        however is discouraged as it requires fiddling with nested dictionaries
        and the special case for arbitrary exception types.

        The first `None` refers to the active blueprint.  If the error
        handler should be application wide `None` shall be used.

        .. versionadded:: 0.7
           One can now additionally also register custom exception types
           that do not necessarily have to be a subclass of the
           :class:`~werkzeug.exceptions.HTTPException` class.

        :param code: the code as integer for the handler
        """

        def decorator(f):
            self._register_error_handler(None, code_or_exception, f)
            return f

        return decorator

    def register_error_handler(self, code_or_exception, f):
        """Alternative error attach function to the :meth:`errorhandler`
        decorator that is more straightforward to use for non decorator
        usage.

        .. versionadded:: 0.7
        """
        self._register_error_handler(None, code_or_exception, f)
        return

    @setupmethod
    def _register_error_handler(self, key, code_or_exception, f):
        if isinstance(code_or_exception, HTTPException):
            code_or_exception = code_or_exception.code
        if isinstance(code_or_exception, integer_types):
            if not code_or_exception != 500:
                assert key is None, 'It is currently not possible to register a 500 internal server error on a per-blueprint level.'
                self.error_handler_spec.setdefault(key, {})[code_or_exception] = f
        else:
            self.error_handler_spec.setdefault(key, {}).setdefault(None, []).append((
             code_or_exception, f))
        return

    @setupmethod
    def template_filter(self, name=None):
        """A decorator that is used to register custom template filter.
        You can specify a name for the filter, otherwise the function
        name will be used. Example::

          @app.template_filter()
          def reverse(s):
              return s[::-1]

        :param name: the optional name of the filter, otherwise the
                     function name will be used.
        """

        def decorator(f):
            self.add_template_filter(f, name=name)
            return f

        return decorator

    @setupmethod
    def add_template_filter(self, f, name=None):
        """Register a custom template filter.  Works exactly like the
        :meth:`template_filter` decorator.

        :param name: the optional name of the filter, otherwise the
                     function name will be used.
        """
        self.jinja_env.filters[name or f.__name__] = f

    @setupmethod
    def template_test(self, name=None):
        """A decorator that is used to register custom template test.
        You can specify a name for the test, otherwise the function
        name will be used. Example::

          @app.template_test()
          def is_prime(n):
              if n == 2:
                  return True
              for i in range(2, int(math.ceil(math.sqrt(n))) + 1):
                  if n % i == 0:
                      return False
              return True

        .. versionadded:: 0.10

        :param name: the optional name of the test, otherwise the
                     function name will be used.
        """

        def decorator(f):
            self.add_template_test(f, name=name)
            return f

        return decorator

    @setupmethod
    def add_template_test(self, f, name=None):
        """Register a custom template test.  Works exactly like the
        :meth:`template_test` decorator.

        .. versionadded:: 0.10

        :param name: the optional name of the test, otherwise the
                     function name will be used.
        """
        self.jinja_env.tests[name or f.__name__] = f

    @setupmethod
    def template_global(self, name=None):
        """A decorator that is used to register a custom template global function.
        You can specify a name for the global function, otherwise the function
        name will be used. Example::

            @app.template_global()
            def double(n):
                return 2 * n

        .. versionadded:: 0.10

        :param name: the optional name of the global function, otherwise the
                     function name will be used.
        """

        def decorator(f):
            self.add_template_global(f, name=name)
            return f

        return decorator

    @setupmethod
    def add_template_global(self, f, name=None):
        """Register a custom template global function. Works exactly like the
        :meth:`template_global` decorator.

        .. versionadded:: 0.10

        :param name: the optional name of the global function, otherwise the
                     function name will be used.
        """
        self.jinja_env.globals[name or f.__name__] = f

    @setupmethod
    def before_request(self, f):
        """Registers a function to run before each request."""
        self.before_request_funcs.setdefault(None, []).append(f)
        return f

    @setupmethod
    def before_first_request(self, f):
        """Registers a function to be run before the first request to this
        instance of the application.

        .. versionadded:: 0.8
        """
        self.before_first_request_funcs.append(f)
        return f

    @setupmethod
    def after_request(self, f):
        """Register a function to be run after each request.  Your function
        must take one parameter, a :attr:`response_class` object and return
        a new response object or the same (see :meth:`process_response`).

        As of Flask 0.7 this function might not be executed at the end of the
        request in case an unhandled exception occurred.
        """
        self.after_request_funcs.setdefault(None, []).append(f)
        return f

    @setupmethod
    def teardown_request(self, f):
        """Register a function to be run at the end of each request,
        regardless of whether there was an exception or not.  These functions
        are executed when the request context is popped, even if not an
        actual request was performed.

        Example::

            ctx = app.test_request_context()
            ctx.push()
            ...
            ctx.pop()

        When ``ctx.pop()`` is executed in the above example, the teardown
        functions are called just before the request context moves from the
        stack of active contexts.  This becomes relevant if you are using
        such constructs in tests.

        Generally teardown functions must take every necessary step to avoid
        that they will fail.  If they do execute code that might fail they
        will have to surround the execution of these code by try/except
        statements and log occurring errors.

        When a teardown function was called because of a exception it will
        be passed an error object.

        .. admonition:: Debug Note

           In debug mode Flask will not tear down a request on an exception
           immediately.  Instead if will keep it alive so that the interactive
           debugger can still access it.  This behavior can be controlled
           by the ``PRESERVE_CONTEXT_ON_EXCEPTION`` configuration variable.
        """
        self.teardown_request_funcs.setdefault(None, []).append(f)
        return f

    @setupmethod
    def teardown_appcontext(self, f):
        """Registers a function to be called when the application context
        ends.  These functions are typically also called when the request
        context is popped.

        Example::

            ctx = app.app_context()
            ctx.push()
            ...
            ctx.pop()

        When ``ctx.pop()`` is executed in the above example, the teardown
        functions are called just before the app context moves from the
        stack of active contexts.  This becomes relevant if you are using
        such constructs in tests.

        Since a request context typically also manages an application
        context it would also be called when you pop a request context.

        When a teardown function was called because of an exception it will
        be passed an error object.

        .. versionadded:: 0.9
        """
        self.teardown_appcontext_funcs.append(f)
        return f

    @setupmethod
    def context_processor(self, f):
        """Registers a template context processor function."""
        self.template_context_processors[None].append(f)
        return f

    @setupmethod
    def url_value_preprocessor(self, f):
        """Registers a function as URL value preprocessor for all view
        functions of the application.  It's called before the view functions
        are called and can modify the url values provided.
        """
        self.url_value_preprocessors.setdefault(None, []).append(f)
        return f

    @setupmethod
    def url_defaults(self, f):
        """Callback function for URL defaults for all view functions of the
        application.  It's called with the endpoint and values and should
        update the values passed in place.
        """
        self.url_default_functions.setdefault(None, []).append(f)
        return f

    def handle_http_exception(self, e):
        """Handles an HTTP exception.  By default this will invoke the
        registered error handlers and fall back to returning the
        exception as response.

        .. versionadded:: 0.3
        """
        handlers = self.error_handler_spec.get(request.blueprint)
        if e.code is None:
            return e
        else:
            if handlers and e.code in handlers:
                handler = handlers[e.code]
            else:
                handler = self.error_handler_spec[None].get(e.code)
            if handler is None:
                return e
            return handler(e)

    def trap_http_exception(self, e):
        """Checks if an HTTP exception should be trapped or not.  By default
        this will return `False` for all exceptions except for a bad request
        key error if ``TRAP_BAD_REQUEST_ERRORS`` is set to `True`.  It
        also returns `True` if ``TRAP_HTTP_EXCEPTIONS`` is set to `True`.

        This is called for all HTTP exceptions raised by a view function.
        If it returns `True` for any exception the error handler for this
        exception is not called and it shows up as regular exception in the
        traceback.  This is helpful for debugging implicitly raised HTTP
        exceptions.

        .. versionadded:: 0.8
        """
        if self.config['TRAP_HTTP_EXCEPTIONS']:
            return True
        if self.config['TRAP_BAD_REQUEST_ERRORS']:
            return isinstance(e, BadRequest)
        return False

    def handle_user_exception(self, e):
        r"""This method is called whenever an exception occurs that should be
        handled.  A special case are
        :class:`~werkzeug.exception.HTTPException`\s which are forwarded by
        this function to the :meth:`handle_http_exception` method.  This
        function will either return a response value or reraise the
        exception with the same traceback.

        .. versionadded:: 0.7
        """
        exc_type, exc_value, tb = sys.exc_info()
        assert exc_value is e
        if isinstance(e, HTTPException) and not self.trap_http_exception(e):
            return self.handle_http_exception(e)
        else:
            blueprint_handlers = ()
            handlers = self.error_handler_spec.get(request.blueprint)
            if handlers is not None:
                blueprint_handlers = handlers.get(None, ())
            app_handlers = self.error_handler_spec[None].get(None, ())
            for typecheck, handler in chain(blueprint_handlers, app_handlers):
                if isinstance(e, typecheck):
                    return handler(e)

            reraise(exc_type, exc_value, tb)
            return

    def handle_exception(self, e):
        """Default exception handling that kicks in when an exception
        occurs that is not caught.  In debug mode the exception will
        be re-raised immediately, otherwise it is logged and the handler
        for a 500 internal server error is used.  If no such handler
        exists, a default 500 internal server error message is displayed.

        .. versionadded:: 0.3
        """
        exc_type, exc_value, tb = sys.exc_info()
        got_request_exception.send(self, exception=e)
        handler = self.error_handler_spec[None].get(500)
        if self.propagate_exceptions:
            if exc_value is e:
                reraise(exc_type, exc_value, tb)
            else:
                raise e
        self.log_exception((exc_type, exc_value, tb))
        if handler is None:
            return InternalServerError()
        else:
            return handler(e)

    def log_exception(self, exc_info):
        """Logs an exception.  This is called by :meth:`handle_exception`
        if debugging is disabled and right before the handler is called.
        The default implementation logs the exception as error on the
        :attr:`logger`.

        .. versionadded:: 0.8
        """
        self.logger.error('Exception on %s [%s]' % (
         request.path,
         request.method), exc_info=exc_info)

    def raise_routing_exception(self, request):
        """Exceptions that are recording during routing are reraised with
        this method.  During debug we are not reraising redirect requests
        for non ``GET``, ``HEAD``, or ``OPTIONS`` requests and we're raising
        a different error instead to help debug situations.

        :internal:
        """
        if not self.debug or not isinstance(request.routing_exception, RequestRedirect) or request.method in ('GET',
                                                                                                              'HEAD',
                                                                                                              'OPTIONS'):
            raise request.routing_exception
        from .debughelpers import FormDataRoutingRedirect
        raise FormDataRoutingRedirect(request)

    def dispatch_request(self):
        """Does the request dispatching.  Matches the URL and returns the
        return value of the view or error handler.  This does not have to
        be a response object.  In order to convert the return value to a
        proper response object, call :func:`make_response`.

        .. versionchanged:: 0.7
           This no longer does the exception handling, this code was
           moved to the new :meth:`full_dispatch_request`.
        """
        req = _request_ctx_stack.top.request
        if req.routing_exception is not None:
            self.raise_routing_exception(req)
        rule = req.url_rule
        if getattr(rule, 'provide_automatic_options', False) and req.method == 'OPTIONS':
            return self.make_default_options_response()
        else:
            return self.view_functions[rule.endpoint](**req.view_args)

    def full_dispatch_request(self):
        """Dispatches the request and on top of that performs request
        pre and postprocessing as well as HTTP exception catching and
        error handling.

        .. versionadded:: 0.7
        """
        yield from self.try_trigger_before_first_request_functions()
        try:
            request_started.send(self)
            rv = self.preprocess_request()
            if rv is None:
                rv = yield from call_maybe_yield(self.dispatch_request)
        except Exception as e:
            rv = self.handle_user_exception(e)

        response = yield from self.make_response(rv)
        response = self.process_response(response)
        request_finished.send(self, response=response)
        return response

    def try_trigger_before_first_request_functions(self):
        """Called before each request and will ensure that it triggers
        the :attr:`before_first_request_funcs` and only exactly once per
        application instance (which means process usually).

        :internal:
        """
        if self._got_first_request:
            return
        with self._before_request_lock:
            if self._got_first_request:
                return
            for func in self.before_first_request_funcs:
                yield from call_maybe_yield(func)

            self._got_first_request = True

    def make_default_options_response(self):
        """This method is called to create the default `OPTIONS` response.
        This can be changed through subclassing to change the default
        behavior of `OPTIONS` responses.

        .. versionadded:: 0.7
        """
        adapter = _request_ctx_stack.top.url_adapter
        if hasattr(adapter, 'allowed_methods'):
            methods = adapter.allowed_methods()
        else:
            methods = []
        try:
            adapter.match(method='--')
        except MethodNotAllowed as e:
            methods = e.valid_methods
        except HTTPException as e:
            pass

        rv = self.response_class()
        rv.allow.update(methods)
        return rv

    def should_ignore_error(self, error):
        """This is called to figure out if an error should be ignored
        or not as far as the teardown system is concerned.  If this
        function returns `True` then the teardown handlers will not be
        passed the error.

        .. versionadded:: 0.10
        """
        return False

    def make_response(self, rv):
        """Converts the return value from a view function to a real
        response object that is an instance of :attr:`response_class`.

        The following types are allowed for `rv`:

        .. tabularcolumns:: |p{3.5cm}|p{9.5cm}|

        ======================= ===========================================
        :attr:`response_class`  the object is returned unchanged
        :class:`str`            a response object is created with the
                                string as body
        :class:`unicode`        a response object is created with the
                                string encoded to utf-8 as body
        a WSGI function         the function is called as WSGI application
                                and buffered as response object
        :class:`tuple`          A tuple in the form ``(response, status,
                                headers)`` or ``(response, headers)``
                                where `response` is any of the
                                types defined here, `status` is a string
                                or an integer and `headers` is a list or
                                a dictionary with header values.
        ======================= ===========================================

        :param rv: the return value from the view function

        .. versionchanged:: 0.9
           Previously a tuple was interpreted as the arguments for the
           response object.
        """
        status_or_headers = headers = None
        if isinstance(rv, tuple):
            rv, status_or_headers, headers = rv + (None, ) * (3 - len(rv))
        if rv is None:
            raise ValueError('View function did not return a response')
        if isinstance(status_or_headers, (dict, list)):
            headers, status_or_headers = status_or_headers, None
        if not isinstance(rv, self.response_class):
            if isinstance(rv, (text_type, bytes, bytearray)):
                rv = self.response_class(rv, headers=headers, status=status_or_headers)
                headers = status_or_headers = None
            else:
                rv = yield from call_maybe_yield(self.response_class.force_type, rv, request.environ)
        if status_or_headers is not None:
            if isinstance(status_or_headers, string_types):
                rv.status = status_or_headers
            else:
                rv.status_code = status_or_headers
        if headers:
            rv.headers.extend(headers)
        return rv

    def create_url_adapter(self, request):
        """Creates a URL adapter for the given request.  The URL adapter
        is created at a point where the request context is not yet set up
        so the request is passed explicitly.

        .. versionadded:: 0.6

        .. versionchanged:: 0.9
           This can now also be called without a request object when the
           URL adapter is created for the application context.
        """
        if request is not None:
            return self.url_map.bind_to_environ(request.environ, server_name=self.config['SERVER_NAME'])
        else:
            if self.config['SERVER_NAME'] is not None:
                return self.url_map.bind(self.config['SERVER_NAME'], script_name=self.config['APPLICATION_ROOT'] or '/', url_scheme=self.config['PREFERRED_URL_SCHEME'])
            return

    def inject_url_defaults(self, endpoint, values):
        """Injects the URL defaults for the given endpoint directly into
        the values dictionary passed.  This is used internally and
        automatically called on URL building.

        .. versionadded:: 0.7
        """
        funcs = self.url_default_functions.get(None, ())
        if '.' in endpoint:
            bp = endpoint.rsplit('.', 1)[0]
            funcs = chain(funcs, self.url_default_functions.get(bp, ()))
        for func in funcs:
            func(endpoint, values)

        return

    def handle_url_build_error(self, error, endpoint, values):
        """Handle :class:`~werkzeug.routing.BuildError` on :meth:`url_for`.
        """
        exc_type, exc_value, tb = sys.exc_info()
        for handler in self.url_build_error_handlers:
            try:
                rv = handler(error, endpoint, values)
                if rv is not None:
                    return rv
            except BuildError as error:
                pass

        if error is exc_value:
            reraise(exc_type, exc_value, tb)
        raise error
        return

    def preprocess_request(self):
        """Called before the actual request dispatching and will
        call every as :meth:`before_request` decorated function.
        If any of these function returns a value it's handled as
        if it was the return value from the view and further
        request handling is stopped.

        This also triggers the :meth:`url_value_processor` functions before
        the actual :meth:`before_request` functions are called.
        """
        bp = _request_ctx_stack.top.request.blueprint
        funcs = self.url_value_preprocessors.get(None, ())
        if bp is not None:
            if bp in self.url_value_preprocessors:
                funcs = chain(funcs, self.url_value_preprocessors[bp])
        for func in funcs:
            func(request.endpoint, request.view_args)

        funcs = self.before_request_funcs.get(None, ())
        if bp is not None:
            if bp in self.before_request_funcs:
                funcs = chain(funcs, self.before_request_funcs[bp])
        for func in funcs:
            rv = func()
            if rv is not None:
                return rv

        return

    def process_response(self, response):
        """Can be overridden in order to modify the response object
        before it's sent to the WSGI server.  By default this will
        call all the :meth:`after_request` decorated functions.

        .. versionchanged:: 0.5
           As of Flask 0.5 the functions registered for after request
           execution are called in reverse order of registration.

        :param response: a :attr:`response_class` object.
        :return: a new response object or the same, has to be an
                 instance of :attr:`response_class`.
        """
        ctx = _request_ctx_stack.top
        bp = ctx.request.blueprint
        funcs = ctx._after_request_functions
        if bp is not None:
            if bp in self.after_request_funcs:
                funcs = chain(funcs, reversed(self.after_request_funcs[bp]))
        if None in self.after_request_funcs:
            funcs = chain(funcs, reversed(self.after_request_funcs[None]))
        for handler in funcs:
            response = handler(response)

        if not self.session_interface.is_null_session(ctx.session):
            self.save_session(ctx.session, response)
        return response

    def do_teardown_request(self, exc=None):
        """Called after the actual request dispatching and will
        call every as :meth:`teardown_request` decorated function.  This is
        not actually called by the :class:`Flask` object itself but is always
        triggered when the request context is popped.  That way we have a
        tighter control over certain resources under testing environments.

        .. versionchanged:: 0.9
           Added the `exc` argument.  Previously this was always using the
           current exception information.
        """
        if exc is None:
            exc = sys.exc_info()[1]
        funcs = reversed(self.teardown_request_funcs.get(None, ()))
        bp = _request_ctx_stack.top.request.blueprint
        if bp is not None:
            if bp in self.teardown_request_funcs:
                funcs = chain(funcs, reversed(self.teardown_request_funcs[bp]))
        for func in funcs:
            func(exc)

        request_tearing_down.send(self, exc=exc)
        return

    def do_teardown_appcontext(self, exc=None):
        """Called when an application context is popped.  This works pretty
        much the same as :meth:`do_teardown_request` but for the application
        context.

        .. versionadded:: 0.9
        """
        if exc is None:
            exc = sys.exc_info()[1]
        for func in reversed(self.teardown_appcontext_funcs):
            func(exc)

        appcontext_tearing_down.send(self, exc=exc)
        return

    def app_context(self):
        """Binds the application only.  For as long as the application is bound
        to the current context the :data:`flask.current_app` points to that
        application.  An application context is automatically created when a
        request context is pushed if necessary.

        Example usage::

            with app.app_context():
                ...

        .. versionadded:: 0.9
        """
        return AppContext(self)

    def request_context(self, environ):
        """Creates a :class:`~flask.ctx.RequestContext` from the given
        environment and binds it to the current context.  This must be used in
        combination with the `with` statement because the request is only bound
        to the current context for the duration of the `with` block.

        Example usage::

            with app.request_context(environ):
                do_something_with(request)

        The object returned can also be used without the `with` statement
        which is useful for working in the shell.  The example above is
        doing exactly the same as this code::

            ctx = app.request_context(environ)
            ctx.push()
            try:
                do_something_with(request)
            finally:
                ctx.pop()

        .. versionchanged:: 0.3
           Added support for non-with statement usage and `with` statement
           is now passed the ctx object.

        :param environ: a WSGI environment
        """
        return RequestContext(self, environ)

    def test_request_context(self, *args, **kwargs):
        """Creates a WSGI environment from the given values (see
        :class:`werkzeug.test.EnvironBuilder` for more information, this
        function accepts the same arguments).
        """
        from flask.testing import make_test_environ_builder
        builder = make_test_environ_builder(self, *args, **kwargs)
        try:
            return self.request_context(builder.get_environ())
        finally:
            builder.close()

    def wsgi_app(self, environ, start_response):
        """The actual WSGI application.  This is not implemented in
        `__call__` so that middlewares can be applied without losing a
        reference to the class.  So instead of doing this::

            app = MyMiddleware(app)

        It's a better idea to do this instead::

            app.wsgi_app = MyMiddleware(app.wsgi_app)

        Then you still have the original application object around and
        can continue to call methods on it.

        .. versionchanged:: 0.7
           The behavior of the before and after request callbacks was changed
           under error conditions and a new callback was added that will
           always execute at the end of the request, independent on if an
           error occurred or not.  See :ref:`callbacks-and-errors`.

        :param environ: a WSGI environment
        :param start_response: a callable accepting a status code,
                               a list of headers and an optional
                               exception context to start the response
        """
        ctx = self.request_context(environ)
        ctx.push()
        error = None
        try:
            try:
                response = yield from self.full_dispatch_request()
            except Exception as e:
                error = e
                response = yield from self.make_response(self.handle_exception(e))

            rv = yield from call_maybe_yield(response, environ, start_response)
            return rv
        finally:
            if self.should_ignore_error(error):
                error = None
            ctx.auto_pop(error)

        return

    @property
    def modules(self):
        from warnings import warn
        warn(DeprecationWarning('Flask.modules is deprecated, use Flask.blueprints instead'), stacklevel=2)
        return self.blueprints

    def __call__(self, environ, start_response):
        """Shortcut for :attr:`wsgi_app`."""
        rv = self.wsgi_app(environ, start_response)
        return rv

    def __repr__(self):
        return '<%s %r>' % (
         self.__class__.__name__,
         self.name)