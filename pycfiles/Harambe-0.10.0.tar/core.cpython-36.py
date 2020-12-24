# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Mardix/Dropbox/Projects/Python/shaft/shaft/core.py
# Compiled at: 2017-01-27 02:04:19
# Size of source mod 2**32: 38787 bytes
"""
Shaft

"""
import re, os, sys, arrow, jinja2, inspect, logging, datetime, functools, pkg_resources, logging.config, active_alchemy
from six import string_types
from werkzeug import import_string
from importlib import import_module
from flask_assets import Environment
from sqlalchemy.engine.url import make_url as sa_make_url
from werkzeug.contrib.fixers import ProxyFix
from werkzeug.routing import BaseConverter, parse_rule
from flask import Flask, g, render_template, flash, session, make_response, Response, request, abort, url_for as f_url_for, redirect as f_redirect
from . import utils, exceptions
from .__about__ import *
_py2 = sys.version_info[0] == 2
__all__ = [
 'Shaft',
 'ShaftInit',
 'db',
 'models',
 'views',
 'get_env',
 'set_env',
 'get_app_env',
 'get_env_config',
 'get_config',
 'page_meta',
 'page_title',
 'flash_success',
 'flash_error',
 'flash_info',
 'flash_data',
 'get_flash_data',
 'init_app',
 'register_package',
 'register_models',
 'abort',
 'redirect',
 'url_for',
 'local_datetime',
 'flash',
 'session',
 'request',
 'import_module']
views = type('', (), {})
models = type('', (), {})

def register_models(**kwargs):
    """
    Alias to register model
    :param kwargs:
    :return:
    """
    [setattr(models, k, v) for k, v in kwargs.items()]


__ENV__ = None

def set_env(env):
    """
    Set the envrionment manually
    :param env:
    :return:
    """
    global __ENV__
    __ENV__ = env.lower().capitalize()


def get_env():
    """
    Return the Capitalize environment name
    It can be used to retrieve class base config
    Default: Development
    :returns: str Capitalized
    """
    if not __ENV__:
        env = os.environ['env'] if 'env' in os.environ else 'Dev'
        set_env(env)
    return __ENV__


def get_app_env():
    """
    if the app and the envi are passed in the command line as 'app=$app:$env'
    :return: tuple app, env
    """
    app, env = None, get_env()
    if 'app' in os.environ:
        app = os.environ['app'].lower()
        if ':' in app:
            app, env = os.environ['app'].split(':', 2)
            set_env(env)
    return (
     app, env)


def get_env_config(config):
    """
    Return config class based based on the config
    :param config : Object - The configuration module containing the environment object
    """
    return getattr(config, get_env())


def init_app(kls):
    """
    To bind middlewares, plugins that needs the 'app' object to init
    Bound middlewares will be assigned on cls.init()
    """
    if not hasattr(kls, '__call__'):
        raise exceptions.ShaftError("init_app: '%s' is not callable" % kls)
    Shaft._init_apps.add(kls)
    return kls


def register_package(pkg):
    """
    Allow to register an app packages by loading and exposing: templates, static,
    and exceptions for abort()

    Structure of package
        root
            | $package_name
                | __init__.py
                |
                | /templates
                    |
                    |
                |
                | /static
                    |
                    | assets.yml

    :param pkg: str - __package__
                    or __name__
                    or The root dir
                    or the dotted resource package (package.path.path,
                    usually __name__ of templates and static
    """
    root_pkg_dir = pkg
    if not os.path.isdir(pkg):
        if '.' in pkg:
            root_pkg_dir = pkg_resources.resource_filename(pkg, '')
    template_path = os.path.join(root_pkg_dir, 'templates')
    static_path = os.path.join(root_pkg_dir, 'static')
    logging.info('Registering App: ' + pkg)
    if os.path.isdir(template_path):
        template_path = jinja2.FileSystemLoader(template_path)
        Shaft._template_paths.add(template_path)
    if os.path.isdir(static_path):
        Shaft._static_paths.add(static_path)
        Shaft._add_asset_bundle(static_path)


def get_config(key, default=None):
    """
    Shortcut to access the application's config in your class
    :param key: The key to access
    :param default: The default value when None
    :returns mixed:
    """
    if Shaft._app:
        return Shaft._app.config.get(key, default)
    else:
        return default


def page_meta(**kwargs):
    """
    Meta allows you to add page meta data
    :params **kwargs:

    meta keys we're expecting:
        title (str)
        description (str)
        url (str) (Will pick it up by itself if not set)
        image (str)
        site_name (str) (but can pick it up from config file)
        object_type (str)
        keywords (list)
        locale (str)
        card (str)

        **Boolean By default these keys are True
        use_opengraph
        use_twitter
        use_googleplus
python
    """
    meta = Shaft._global.get('__META__', {})
    (meta.update)(**kwargs)
    Shaft.g(__META__=meta)


def page_title(title):
    pass


def flash_success(msg):
    """
    Alias to flash, but set a success message
    :param msg:
    :return:
    """
    return flash(msg, 'success')


def flash_error(msg):
    """
    Alias to flash, but set an error message
    :param msg:
    :return:
    """
    return flash(msg, 'error')


def flash_info(msg):
    """
    Alias to flash, but set an info message
    :param msg:
    :return:
    """
    return flash(msg, 'info')


def flash_data(data):
    """
    Just like flash, but will save data
    :param data:
    :return:
    """
    session['_flash_data'] = data


def get_flash_data():
    """
    Retrieved
    :return: mixed
    """
    return session.pop('_flash_data', None)


is_method = lambda x: inspect.ismethod if _py2 else inspect.isfunction

def local_datetime(utcdatetime, timezone=None):
    """
    Return local datetime based on the timezone
    :param utcdatetime:
    :param timezone:
    :return:
    """
    timezone = timezone or get_config('DATETIME_TIMEZONE')
    return arrow.get(utcdatetime, timezone)


def utcnow():
    """
    Return the UTC NOW
    :return: Arrow
    """
    return arrow.utcnow()


def _get_action_endpoint(action):
    """
    Return the endpoint base on the view's action
    :param action:
    :return:
    """
    _endpoint = None
    if is_method(action):
        if hasattr(action, '_rule_cache'):
            rc = action._rule_cache
            if rc:
                k = list(rc.keys())[0]
                rules = rc[k]
                len_rules = len(rules)
                if len_rules == 1:
                    rc_kw = rules[0][1]
                    _endpoint = rc_kw.get('endpoint', None)
                    if not _endpoint:
                        _endpoint = _build_endpoint_route_name(action)
                elif len_rules > 1:
                    _prefix = _build_endpoint_route_name(action)
                    for r in Shaft._app.url_map.iter_rules():
                        if 'GET' in r.methods or 'POST' in r.methods:
                            if _prefix in r.endpoint:
                                _endpoint = r.endpoint
                                break

    return _endpoint


def url_for(endpoint, **kw):
    """
    Shaft url_for is an alias to the flask url_for, with the ability of
    passing the function signature to build the url, without knowing the endpoint
    :param endpoint:
    :param kw:
    :return:
    """
    _endpoint = None
    if isinstance(endpoint, string_types):
        return f_url_for(endpoint, **kw)
    if isinstance(endpoint, Shaft):
        fn = sys._getframe().f_back.f_code.co_name
        endpoint = getattr(endpoint, fn)
    if is_method(endpoint):
        _endpoint = _get_action_endpoint(endpoint)
        if not _endpoint:
            _endpoint = _build_endpoint_route_name(endpoint)
    if _endpoint:
        return f_url_for(_endpoint, **kw)
    raise exceptions.ShaftError('Shaft `url_for` received an invalid endpoint')


def redirect(endpoint, **kw):
    """
    Redirect allow to redirect dynamically using the classes methods without
    knowing the right endpoint.
    Expecting all endpoint have GET as method, it will try to pick the first
    match, based on the endpoint provided or the based on the Rule map_url

    An endpoint can also be passed along with **kw

    An http: or https: can also be passed, and will redirect to that site.

    example:
        redirect(self.hello_world)
        redirect(self.other_page, name="x", value="v")
        redirect("https://google.com")
        redirect(views.ContactPage.index)
    :param endpoint:
    :return: redirect url
    """
    _endpoint = None
    if isinstance(endpoint, string_types):
        _endpoint = endpoint
        if '/' in endpoint:
            return f_redirect(endpoint)
        for r in Shaft._app.url_map.iter_rules():
            _endpoint = endpoint
            if 'GET' in r.methods:
                if endpoint in r.endpoint:
                    _endpoint = r.endpoint
                    break

    else:
        if isinstance(endpoint, Shaft):
            fn = sys._getframe().f_back.f_code.co_name
            endpoint = getattr(endpoint, fn)
    if is_method(endpoint):
        _endpoint = _get_action_endpoint(endpoint)
        if not _endpoint:
            _endpoint = _build_endpoint_route_name(endpoint)
    if _endpoint:
        return f_redirect(url_for(_endpoint, **kw))
    raise exceptions.ShaftError('Invalid endpoint')


def _build_endpoint_route_name(endpoint):
    cls = endpoint.im_class() if not hasattr(endpoint, '__self__') or endpoint.__self__ is None else endpoint.__self__
    return cls.build_route_name(endpoint.__name__)


class _ShaftAlchemy(active_alchemy.ActiveAlchemy):
    __doc__ = '\n    A custom ActiveAlchemy wrapper which defers the connection\n    '

    def __init__(self):
        self.Model = active_alchemy.declarative_base(cls=(active_alchemy.Model), name='Model')
        self.BaseModel = active_alchemy.declarative_base(cls=(active_alchemy.BaseModel), name='BaseModel')

    def _connect(self, uri, app):
        self.uri = uri
        self.info = sa_make_url(uri)
        self.options = self._cleanup_options(echo=False,
          pool_size=None,
          pool_timeout=None,
          pool_recycle=None,
          convert_unicode=True)
        self.connector = None
        self._engine_lock = active_alchemy.threading.Lock()
        self.session = active_alchemy._create_scoped_session(self, query_cls=(active_alchemy.BaseQuery))
        self.Model.db, self.BaseModel.db = self, self
        self.Model._query, self.BaseModel._query = self.session.query, self.session.query
        self.init_app(app)
        active_alchemy._include_sqlalchemy(self)


db = _ShaftAlchemy()

class Shaft(object):
    __doc__ = 'Base view for any class based views implemented with Flask-Classy. Will\n    automatically configure routes when registered with a Flask app instance.\n    Credit: Shout out to Flask-Classy for the greatest logic in this class\n    Flask-Classy -> https://github.com/apiguy/flask-classy\n    '
    decorators = []
    base_route = None
    route_prefix = None
    trailing_slash = True
    base_layout = 'layouts/base.jade'
    template_markup = 'jade'
    assets = None
    logger = None
    _ext = set()
    _Shaft__special_methods = ['get', 'put', 'patch', 'post', 'delete', 'index']
    _installed_apps = []
    _app = None
    _init_apps = set()
    _template_paths = set()
    _static_paths = set()
    _asset_bundles = set()
    _default_page_title = ''
    _default_page_meta = dict(description='',
      url='',
      image='',
      site_name='',
      object_type='article',
      locale='',
      keywords=[],
      use_opengraph=True,
      use_googleplus=True,
      use_twitter=True,
      properties={})
    _global = dict(__NAME__=__title__,
      __VERSION__=__version__,
      __YEAR__=(utcnow().year),
      __META__=_default_page_meta)

    @classmethod
    def __call__(cls, flask_or_import_name, projects=None, app_name=None, app_directory=None, load_app=True):
        """
        Allow to register all subclasses of Shaft at once

        If a class doesn't have a route base, it will create a dasherize version
        of the class name.

        So we call it once initiating
        :param flask_or_import_name: Flask instance or import name -> __name__
        :param app_name: name of the project. If the directory and config is empty, it will guess them from here
        :param app_directory: the directory name relative to the current execution path
        :param implicit_import: when True, it will automatically load the views, models
        :param load_app: when True it will load your application
        :param load_installed_apps: bool - When True it will load the installed apps
        """
        if not app_directory:
            app_directory = 'app'
        else:
            if not app_name:
                app_name = get_app_env()[0] or 'main'
            app_env = get_env()
            app = flask_or_import_name if isinstance(flask_or_import_name, Flask) else Flask(flask_or_import_name)
            app.wsgi_app = ProxyFix(app.wsgi_app)
            app.url_map.converters['regex'] = RegexConverter
            app.template_folder = '%s/templates' % app_directory
            app.static_folder = '%s/static' % app_directory
            c = '%s.config.%s' % (app_directory, app_env)
            app.config.from_object(c)
            cls._app = app
            cls._load_extensions()
            cls._setup_logger()
            cls._setup_db()
            cls.assets = Environment(cls._app)
            _ = cls.setup_installed_apps()
            cls._expose_models()
            try:
                m = '%s.models' % app_directory
                import_module(m)
                cls._expose_models()
                if not projects:
                    projects = {'main': 'main'}
                if app_name not in projects:
                    raise ValueError('Missing project: %s' % app_name)
                _projects = projects.get(app_name)
                if isinstance(_projects, string_types):
                    _projects = [
                     _projects]
                for _ in _projects:
                    import_module('%s.views.%s' % (app_directory, _))

            except ImportError as ie1:
                pass

        cls._expose_models()
        [_app(cls._app) for _app in cls._init_apps]
        if load_app:
            cls._add_asset_bundle(cls._app.static_folder)
            if cls._template_paths:
                loader = [
                 cls._app.jinja_loader] + list(cls._template_paths)
                cls._app.jinja_loader = jinja2.ChoiceLoader(loader)
            if cls._static_paths:
                cls.assets.load_path = [
                 cls._app.static_folder] + list(cls._static_paths)
                [cls.assets.from_yaml(a) for a in cls._asset_bundles]
            for subcls in cls.__subclasses__():
                base_route = subcls.base_route
                if not base_route:
                    base_route = utils.dasherize(utils.underscore(subcls.__name__))
                    if subcls.__name__.lower() == 'index':
                        base_route = '/'
                subcls._register((cls._app), base_route=base_route)

        @cls._app.after_request
        def _after_request_cleanup(response):
            cls._global['__META__'] = cls._default_page_meta.copy()
            return response

        return cls._app

    @classmethod
    def setup_installed_apps(cls):
        """
        To import 3rd party applications along with associated properties

        It is a list of dict or string.

        When a dict, it contains the `app` key and the configuration,
        if it's a string, it is just the app name

        If you require dependencies from other packages, dependencies
        must be placed before the calling package.

        It is required that __init__ in the package app has an entry point method
        -> 'main(**kw)' which will be used to setup the default app.

        By default the following **kwargs are passed to the main function:
            app: (object)[always] object of the flask app
            route: (string) the base route for the app. default: /
            nav_menu: (dict) the navigation config for navigation menu. By default the title is set to None
            decorators: (list) list of decorators (as string) to use
            options: (dict) all the app's customs options

        As a dict
        INSTALLED_APPS = [
            "my.contrib.app",
            "my.other.contrib.app",
            {
                "app": "my.contrib.app3",
                "options": {

                },
                "modules": {
                    "module_a": {
                        "route": "/",
                        "nav_menu": {

                        }
                    },
                    "module_b": {
                        "route": "/",
                        "decorators": []
                    }
                }
            }
        ]
        :return:
        """
        cls._installed_apps = cls._app.config.get('INSTALLED_APPS', [])
        if cls._installed_apps:
            _ = []

            def import_app(app, kwargs):
                try:
                    _.append((import_string('%s.main' % app))(**kwargs))
                except ImportError as e:
                    raise e

            for k in cls._installed_apps:
                if isinstance(k, string_types):
                    a = k
                    prop = {}
                else:
                    if isinstance(k, dict):
                        a = k.get('app')
                        k['name'] = a
                        prop = k
                _kwargs = {'app':cls._app,  'name':prop.get('name'), 
                 'route':prop.get('route') or '/', 
                 'nav_menu':prop.get('nav_menu') or {'title': None}, 
                 'decorators':[import_string(d) for d in prop.get('decorators')] if 'decorators' in prop else [], 
                 'options':prop.get('options') or {}}
                try:
                    _impm = import_string(a)
                    try:
                        import_string('%s.models' % a)
                        cls._expose_models()
                    except ImportError as ie:
                        pass

                    import_app(a, _kwargs)
                except ImportError as e:
                    raise e

                modules = prop['modules'] if 'modules' in prop else None
                if modules:
                    if isinstance(modules, list):
                        for m in modules:
                            import_app('%s.%s' % (a, m), _kwargs)

                    elif isinstance(modules, dict):
                        for n, kw in modules.items():
                            kw2 = {'app':_kwargs['app'], 
                             'name':'%s.%s' % (a, n), 
                             'route':kw.get('route') or '/', 
                             'nav_menu':kw.get('nav_menu') or {'title': None}, 
                             'decorators':_kwargs['decorators'], 
                             'options':_kwargs['options']}
                            import_app('%s.%s' % (a, n), kw2)

            return _

    @classmethod
    def render(cls, data={}, _template=None, _layout=None, **kwargs):
        """
        Render the view template based on the class and the method being invoked
        :param data: The context data to pass to the template
        :param _template: The file template to use. By default it will map the classname/action.html
        :param _layout: The body layout, must contain {% include __template__ %}
        """
        if not _template:
            stack = inspect.stack()[1]
            module = inspect.getmodule(cls).__name__
            module_name = module.split('.')[(-1)]
            action_name = stack[3]
            view_name = cls.__name__
            if view_name.endswith('View'):
                view_name = view_name[:-4]
            _template = '%s/%s.%s' % (view_name, action_name, cls.template_markup)
        data = data or dict()
        if kwargs:
            data.update(kwargs)
        data['__'] = cls._global
        data['__template__'] = _template
        return render_template((_layout or cls.base_layout), **data)

    @classmethod
    def g(cls, **kwargs):
        """
        Assign a global view context to be used in the template
        :params **kwargs:
        """
        cls._global.update(kwargs)

    @classmethod
    def _add_asset_bundle(cls, path):
        """
        Add a webassets bundle yml file
        """
        f = '%s/assets.yml' % path
        if os.path.isfile(f):
            cls._asset_bundles.add(f)

    @classmethod
    def _setup_logger(cls):
        logging_config = cls._app.config.get('LOGGING')
        if not logging_config:
            logging_config = {'version':1,  'handlers':{'default': {'class': cls._app.config.get('LOGGING_CLASS', 'logging.StreamHandler')}}, 
             'loggers':{'': {'handlers':[
                    'default'], 
                   'level':'WARN'}}}
        logging.config.dictConfig(logging_config)
        cls.logger = logging.getLogger('root')
        cls._app._logger = cls.logger
        cls._app._loger_name = cls.logger.name

    @classmethod
    def _setup_db(cls):
        cls._app.db = None
        uri = cls._app.config.get('DB_URI')
        if uri:
            db._connect(uri, cls._app)
            cls._app.db = db

    @classmethod
    def _expose_models(cls):
        if cls._app.db:
            register_models(**)

    @classmethod
    def _register(cls, app, base_route=None, subdomain=None, route_prefix=None, trailing_slash=None):
        """Registers a Shaft class for use with a specific instance of a
        Flask app. Any methods not prefixes with an underscore are candidates
        to be routed and will have routes registered when this method is
        called.

        :param app: an instance of a Flask application

        :param base_route: The base path to use for all routes registered for
                           this class. Overrides the base_route attribute if
                           it has been set.

        :param subdomain:  A subdomain that this registration should use when
                           configuring routes.

        :param route_prefix: A prefix to be applied to all routes registered
                             for this class. Precedes base_route. Overrides
                             the class' route_prefix if it has been set.
        """
        if cls is Shaft:
            raise TypeError('cls must be a subclass of Shaft, not Shaft itself')
        else:
            setattr(views, cls.__name__, cls)
            if base_route:
                cls.orig_base_route = cls.base_route
                cls.base_route = base_route
            if route_prefix:
                cls.orig_route_prefix = cls.route_prefix
                cls.route_prefix = route_prefix
            if not subdomain:
                if hasattr(app, 'subdomain'):
                    if app.subdomain is not None:
                        subdomain = app.subdomain
                if hasattr(cls, 'subdomain'):
                    subdomain = cls.subdomain
            if trailing_slash is not None:
                cls.orig_trailing_slash = cls.trailing_slash
                cls.trailing_slash = trailing_slash
            for name, value in get_interesting_members(Shaft, cls):
                proxy = cls.make_proxy_method(name)
                route_name = cls.build_route_name(name)
                try:
                    if hasattr(value, '_rule_cache') and name in value._rule_cache:
                        for idx, cached_rule in enumerate(value._rule_cache[name]):
                            rule, options = cached_rule
                            rule = cls.build_rule(rule)
                            sub, ep, options = cls.parse_options(options)
                            if not subdomain:
                                if sub:
                                    subdomain = sub
                            if ep:
                                endpoint = ep
                            else:
                                if len(value._rule_cache[name]) == 1:
                                    endpoint = route_name
                                else:
                                    endpoint = '%s_%d' % (route_name, idx)
                            (app.add_url_rule)(rule, endpoint, proxy, subdomain=subdomain, **options)

                    else:
                        if name in cls._Shaft__special_methods:
                            if name in ('get', 'index'):
                                methods = [
                                 'GET']
                                if name == 'index':
                                    if hasattr(value, '_methods_cache'):
                                        methods = value._methods_cache
                            else:
                                methods = [
                                 name.upper()]
                            rule = cls.build_rule('/', value)
                            if not cls.trailing_slash:
                                rule = rule.rstrip('/')
                            app.add_url_rule(rule, route_name, proxy, methods=methods,
                              subdomain=subdomain)
                        else:
                            methods = value._methods_cache if hasattr(value, '_methods_cache') else [
                             'GET']
                            name = utils.dasherize(name)
                            route_str = '/%s/' % name
                            if not cls.trailing_slash:
                                route_str = route_str.rstrip('/')
                            rule = cls.build_rule(route_str, value)
                            app.add_url_rule(rule, route_name, proxy, subdomain=subdomain,
                              methods=methods)
                except DecoratorCompatibilityError:
                    raise DecoratorCompatibilityError('Incompatible decorator detected on %s in class %s' % (name, cls.__name__))

            if hasattr(cls, 'orig_base_route'):
                cls.base_route = cls.orig_base_route
                del cls.orig_base_route
            if hasattr(cls, 'orig_route_prefix'):
                cls.route_prefix = cls.orig_route_prefix
                del cls.orig_route_prefix
            if hasattr(cls, 'orig_trailing_slash'):
                cls.trailing_slash = cls.orig_trailing_slash
                del cls.orig_trailing_slash

    @classmethod
    def parse_options(cls, options):
        """Extracts subdomain and endpoint values from the options dict and returns
           them along with a new dict without those values.
        """
        options = options.copy()
        subdomain = options.pop('subdomain', None)
        endpoint = options.pop('endpoint', None)
        return (subdomain, endpoint, options)

    @classmethod
    def make_proxy_method(cls, name):
        """Creates a proxy function that can be used by Flasks routing. The
        proxy instantiates the Shaft subclass and calls the appropriate
        method.
        :param name: the name of the method to create a proxy for
        """
        i = cls()
        view = getattr(i, name)
        for decorator in cls.decorators:
            view = decorator(view)

        @functools.wraps(view)
        def proxy(**forgettable_view_args):
            del forgettable_view_args
            if hasattr(i, 'before_request'):
                response = (i.before_request)(name, **request.view_args)
                if response is not None:
                    return response
            before_view_name = 'before_' + name
            if hasattr(i, before_view_name):
                before_view = getattr(i, before_view_name)
                response = before_view(**request.view_args)
                if response is not None:
                    return response
            response = view(**request.view_args)
            if isinstance(response, dict) or response is None:
                response = response or {}
                if hasattr(i, '_renderer'):
                    response = i._renderer(response)
                else:
                    df_v_t = '%s/%s.%s' % (cls.__name__, view.__name__, cls.template_markup)
                    response.setdefault('_template', df_v_t)
                    response = (i.render)(**response)
            if not isinstance(response, Response):
                response = make_response(response)
            for ext in cls._ext:
                response = ext(response)

            after_view_name = 'after_' + name
            if hasattr(i, after_view_name):
                after_view = getattr(i, after_view_name)
                response = after_view(response)
            if hasattr(i, 'after_request'):
                response = i.after_request(name, response)
            return response

        return proxy

    @classmethod
    def build_rule(cls, rule, method=None):
        """Creates a routing rule based on either the class name (minus the
        'View' suffix) or the defined `base_route` attribute of the class

        :param rule: the path portion that should be appended to the
                     route base

        :param method: if a method's arguments should be considered when
                       constructing the rule, provide a reference to the
                       method here. arguments named "self" will be ignored
        """
        rule_parts = []
        if cls.route_prefix:
            rule_parts.append(cls.route_prefix)
        base_route = cls.get_base_route()
        if base_route:
            rule_parts.append(base_route)
        rule_parts.append(rule)
        ignored_rule_args = ['self']
        if hasattr(cls, 'base_args'):
            ignored_rule_args += cls.base_args
        if method:
            args = get_true_argspec(method)[0]
            for arg in args:
                if arg not in ignored_rule_args:
                    rule_parts.append('<%s>' % arg)

        result = '/%s' % '/'.join(rule_parts)
        return re.sub('(/)\\1+', '\\1', result)

    @classmethod
    def get_base_route(cls):
        """Returns the route base to use for the current class."""
        base_route = cls.__name__.lower()
        if cls.base_route is not None:
            base_route = cls.base_route
            base_rule = parse_rule(base_route)
            cls.base_args = [r[2] for r in base_rule]
        return base_route.strip('/')

    @classmethod
    def build_route_name(cls, method_name):
        """Creates a unique route name based on the combination of the class
        name with the method name.

        :param method_name: the method name to use when building a route name
        """
        return cls.__name__ + ':%s' % method_name

    @staticmethod
    def _bind_route_rule_cache(f, rule, append_method=False, **kwargs):
        if rule is None:
            rule = utils.dasherize(f.__name__) + '/'
        else:
            if not hasattr(f, '_rule_cache') or f._rule_cache is None:
                f._rule_cache = {f.__name__: [(rule, kwargs)]}
            else:
                if f.__name__ not in f._rule_cache:
                    f._rule_cache[f.__name__] = [
                     (
                      rule, kwargs)]
                else:
                    if append_method:
                        for r in f._rule_cache[f.__name__]:
                            if r[0] == rule and 'methods' in r[1] and 'methods' in kwargs:
                                r[1]['methods'] = list(set(r[1]['methods'] + kwargs['methods']))

                    else:
                        f._rule_cache[f.__name__].append((rule, kwargs))
        return f

    @classmethod
    def _load_extensions(cls):
        extensions = [
         'pyjade.ext.jinja.PyJadeExtension',
         'shaft.extras.jade.JadeTagExtension',
         'shaft.extras.md.MarkdownExtension',
         'shaft.extras.md.MarkdownTagExtension']
        if cls._app.config.get('COMPRESS_HTML'):
            extensions.append('shaft.extras.htmlcompress.HTMLCompress')
        for ext in extensions:
            cls._app.jinja_env.add_extension(ext)


ShaftInit = Shaft()

def get_interesting_members(base_class, cls):
    """Returns a generator of methods that can be routed to"""
    base_members = dir(base_class)
    predicate = inspect.ismethod if _py2 else inspect.isfunction
    all_members = inspect.getmembers(cls, predicate=predicate)
    return (member for member in all_members if member[0] not in base_members if (hasattr(member[1], '__self__') and member[1].__self__ not in inspect.getmro(cls) if _py2 else True) if not member[0].startswith('_') if not member[0].startswith('before_') if not member[0].startswith('after_'))


def apply_function_to_members(cls, fn):
    for name, method in get_interesting_members(Shaft, cls):
        setattr(cls, name, fn(method))


def get_true_argspec(method):
    """Drills through layers of decorators attempting to locate the actual argspec for the method."""
    argspec = inspect.getargspec(method)
    args = argspec[0]
    if args:
        if args[0] == 'self':
            return argspec
    if hasattr(method, '__func__'):
        method = method.__func__
    if not hasattr(method, '__closure__') or method.__closure__ is None:
        raise DecoratorCompatibilityError
    closure = method.__closure__
    for cell in closure:
        inner_method = cell.cell_contents
        if inner_method is method:
            continue
        if not inspect.isfunction(inner_method):
            if not inspect.ismethod(inner_method):
                continue
            else:
                true_argspec = get_true_argspec(inner_method)
                if true_argspec:
                    return true_argspec


class DecoratorCompatibilityError(Exception):
    pass


class RegexConverter(BaseConverter):

    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


def get_installed_app_options(app):
    """
    Get the app's options
    :param app: the app, ie: __name__
    :return:
    """
    options = {}
    if Shaft._installed_apps:
        for k in Shaft._installed_apps:
            if isinstance(k, dict):
                if 'name' in k:
                    if k['name'] == app:
                        options = k['options'] if 'options' in k else {}
                        break

    return options


def __make_class_decorator(function_decorator):
    """
    Turn a function decorator, to a class decorator. It applies on individual
    method too
    :param function_decorator:
    :return:

    @make_class_decorator
    def function_decorator(fn):
        def gn(*args, **kwargs):
            print 'hi'
            fn(*args, **kwargs)
        gn.__name__ = fn.__name__
        return gn

    @function_decorator
    class Foo:
        def f(self):
            print 'hey'
    """

    def class_decorator(cls):
        if inspect.isclass(cls):
            for name, method in get_interesting_members(Shaft, cls):
                setattr(cls, name, function_decorator(method))

        else:
            return function_decorator(cls)
        return cls

    return class_decorator