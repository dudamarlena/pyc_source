# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Mardix/Dropbox/Projects/Python/harambe/harambe/core.py
# Compiled at: 2017-05-03 01:10:35
"""
Harambe

"""
import re, os, sys, arrow, jinja2, inspect, logging, functools, pkg_resources, logging.config
from six import string_types
from werkzeug import import_string
from flask_assets import Environment
from werkzeug.contrib.fixers import ProxyFix
from werkzeug.routing import BaseConverter, parse_rule
from flask import Flask, g, render_template, flash, session, make_response, Response, request, abort, url_for as f_url_for, redirect as f_redirect
from . import utils, exceptions
from .extras.harambe_db import HarambeDB
from .__about__ import *
_py2 = sys.version_info[0] == 2
__all__ = [
 'Harambe',
 'HarambeApp',
 'db',
 'models',
 'views',
 'get_env',
 'set_env',
 'get_app_env',
 'get_env_config',
 'get_config',
 'page_meta',
 'flash_success',
 'flash_error',
 'flash_info',
 'flash_data',
 'get_flash_data',
 'init_app',
 'register_package',
 'register_models',
 'utc_now',
 'local_datetime',
 'local_now',
 'to_local_datetime',
 'flash',
 'session',
 'request',
 'abort',
 'g',
 'redirect',
 'url_for']
__ENV__ = None
is_method = lambda x: inspect.ismethod if _py2 else inspect.isfunction
views = type('', (), {})
models = type('', (), {})
db = HarambeDB()

def register_models(**kwargs):
    """
    Alias to register model
    :param kwargs:
    :return:
    """
    [ setattr(models, k, v) for k, v in kwargs.items() ]


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
        raise exceptions.HarambeError("init_app: '%s' is not callable" % kls)
    Harambe._init_apps.add(kls)
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
    if not os.path.isdir(pkg) and '.' in pkg:
        root_pkg_dir = pkg_resources.resource_filename(pkg, '')
    template_path = os.path.join(root_pkg_dir, 'templates')
    static_path = os.path.join(root_pkg_dir, 'static')
    logging.info('Registering App: ' + pkg)
    if os.path.isdir(template_path):
        template_path = jinja2.FileSystemLoader(template_path)
        Harambe._template_paths.add(template_path)
    if os.path.isdir(static_path):
        Harambe._static_paths.add(static_path)
        Harambe._add_asset_bundle(static_path)


def get_config(key, default=None):
    """
    Shortcut to access the application's config in your class
    :param key: The key to access
    :param default: The default value when None
    :returns mixed:
    """
    if Harambe._app:
        return Harambe._app.config.get(key, default)
    return default


def page_meta(title=None, **kwargs):
    """
    Meta allows you to add page meta data in the request `g` context
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
    default = dict(title='', description='', url='', image='', site_name='', object_type='article', locale='', keywords=[], use_opengraph=True, use_googleplus=True, use_twitter=True, properties={})
    meta = getattr(g, '__META__', default)
    if title:
        kwargs['title'] = title
    meta.update(**kwargs)
    setattr(g, '__META__', meta)


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


def utc_now():
    """
    Return the utcnow arrow object
    :return: Arrow
    """
    return arrow.utcnow()


def local_datetime(utcdatetime, format=None, timezone=None):
    """
    Return local datetime based on the timezone
    Also can format the date
    :param utcdatetime: Arrow or string
    :param format: string of format
    :param timezone: string, ie: US/Eastern
    :return:
    """
    timezone = timezone or get_config('DATETIME_TIMEZONE', 'US/Eastern')
    dt = utcdatetime.to(timezone) if isinstance(utcdatetime, arrow.Arrow) else arrow.get(utcdatetime, timezone)
    if format is None:
        return dt
    else:
        _ = get_config('DATETIME_FORMAT')
        format = format or _.get('default') or 'MM/DD/YYYY' if 1 else _.get(format)
        return dt.format(format)


def to_local_datetime(dt, tz=None):
    """
    DEPRECATED
    :param dt: 
    :param tz: 
    :return: 
    """
    return local_datetime(dt, tz)


def local_now():
    """
    DEPRECATED
    :return: 
    """
    return to_local_datetime(utc_now())


def url_for(endpoint, **kw):
    """
    Harambe url_for is an alias to the flask url_for, with the ability of
    passing the function signature to build the url, without knowing the endpoint
    :param endpoint:
    :param kw:
    :return:
    """
    _endpoint = None
    if isinstance(endpoint, string_types):
        return f_url_for(endpoint, **kw)
    else:
        if isinstance(endpoint, Harambe):
            fn = sys._getframe().f_back.f_code.co_name
            endpoint = getattr(endpoint, fn)
        if is_method(endpoint):
            _endpoint = _get_action_endpoint(endpoint)
            if not _endpoint:
                _endpoint = _build_endpoint_route_name(endpoint)
        if _endpoint:
            return f_url_for(_endpoint, **kw)
        raise exceptions.HarambeError('Harambe `url_for` received an invalid endpoint')
        return


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
        for r in Harambe._app.url_map.iter_rules():
            _endpoint = endpoint
            if 'GET' in r.methods and endpoint in r.endpoint:
                _endpoint = r.endpoint
                break

    else:
        if isinstance(endpoint, Harambe):
            fn = sys._getframe().f_back.f_code.co_name
            endpoint = getattr(endpoint, fn)
        if is_method(endpoint):
            _endpoint = _get_action_endpoint(endpoint)
            if not _endpoint:
                _endpoint = _build_endpoint_route_name(endpoint)
    if _endpoint:
        return f_redirect(url_for(_endpoint, **kw))
    else:
        raise exceptions.HarambeError('Invalid endpoint')
        return


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
                    for r in Harambe._app.url_map.iter_rules():
                        if ('GET' in r.methods or 'POST' in r.methods) and _prefix in r.endpoint:
                            _endpoint = r.endpoint
                            break

    return _endpoint


def _build_endpoint_route_name(endpoint):
    is_class = inspect.isclass(endpoint)
    class_name = (is_class or endpoint.im_class).__name__ if 1 else endpoint.__name__
    method_name = endpoint.__name__
    cls = endpoint.im_class() if not hasattr(endpoint, '__self__') or endpoint.__self__ is None else endpoint.__self__
    return build_endpoint_route_name(cls, method_name, class_name)


class Harambe(object):
    decorators = []
    base_route = None
    route_prefix = None
    trailing_slash = True
    base_layout = 'layouts/base.jade'
    template_markup = 'jade'
    assets = None
    logger = None
    _ext = set()
    __special_methods = ['get', 'put', 'patch', 'post', 'delete', 'index']
    _installed_apps = []
    _app = None
    _init_apps = set()
    _template_paths = set()
    _static_paths = set()
    _asset_bundles = set()

    @classmethod
    def __call__(cls, flask_or_import_name, projects=None, project_name=None, app_directory=None):
        """

        :param flask_or_import_name: Flask instance or import name -> __name__
        :param projects: dict of app and views to load. ie:
            {
                "main": [
                    "main",
                    "api"
                ]
            }
        :param project_name: name of the project. If empty, it will try to get
                             it from the app_env(). By default it is "main"
                             The app main is set as environment variable
                             ie: app=PROJECT_NAME:CONFIG -> app=main:production
        :param app_directory: the directory name relative to the current execution path
        :return:
        """
        if not app_directory:
            app_directory = 'app'
        if not project_name:
            project_name = get_app_env()[0] or 'main'
        app_env = get_env()
        app = flask_or_import_name if isinstance(flask_or_import_name, Flask) else Flask(flask_or_import_name)
        app.url_map.converters['regex'] = RegexConverter
        app.template_folder = '%s/templates' % app_directory
        app.static_folder = '%s/static' % app_directory
        c = '%s.config.%s' % (app_directory, app_env)
        app.config.from_object(c)
        if app.config.get('USE_PROXY_FIX') is not False:
            app.wsgi_app = ProxyFix(app.wsgi_app)
        cls._app = app
        cls.assets = Environment(cls._app)
        cls._load_extensions()
        cls._setup_logger()
        cls._setup_db()
        cls.setup_installed_apps()
        cls._expose_models()
        try:
            m = '%s.models' % app_directory
            import_string(m)
            cls._expose_models()
            if not projects:
                projects = {'main': 'main'}
            if project_name not in projects:
                raise ValueError('Missing project: %s' % project_name)
            _projects = projects.get(project_name)
            if isinstance(_projects, string_types):
                _projects = [
                 _projects]
            for _ in _projects:
                import_string('%s.views.%s' % (app_directory, _))

        except ImportError as ie1:
            pass

        cls._expose_models()
        _ = [ _app(cls._app) for _app in cls._init_apps ]
        cls._add_asset_bundle(cls._app.static_folder)
        if cls._template_paths:
            loader = [
             cls._app.jinja_loader] + list(cls._template_paths)
            cls._app.jinja_loader = jinja2.ChoiceLoader(loader)
        if cls._static_paths:
            cls.assets.load_path = [
             cls._app.static_folder] + list(cls._static_paths)
            [ cls.assets.from_yaml(a) for a in cls._asset_bundles ]
        for subcls in cls.__subclasses__():
            base_route = subcls.base_route
            if not base_route:
                base_route = utils.dasherize(utils.underscore(subcls.__name__))
                if subcls.__name__.lower() == 'index':
                    base_route = '/'
            subcls._register(cls._app, base_route=base_route)

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

        As a dict
        INSTALLED_APPS = [
            "it.can.be.a.string.to.the.module",
            ("in.a.tuple.with.props.dict", {options}),
            [
                ("multi.app.list.in.a.list.of.tuple", {options}),
                ("multi.app.list.in.a.list.of.tuple2", {options})
            ]
        ]

        :return:
        """
        cls._installed_apps = cls._app.config.get('INSTALLED_APPS', [])
        if cls._installed_apps:

            def import_app(module, props={}):
                _ = import_string(module)
                setattr(_, '__options__', utils.dict_dot(props))

            for k in cls._installed_apps:
                if isinstance(k, string_types):
                    import_app(k, {})
                elif isinstance(k, tuple):
                    import_app(k[0], k[1])
                elif isinstance(k, list):
                    for t in k:
                        import_app(t[0], t[1])

    @classmethod
    def render(cls, data={}, _template=None, _layout=None, **kwargs):
        """
        Render the view template based on the class and the method being invoked
        :param data: The context data to pass to the template
        :param _template: The file template to use. By default it will map the module/classname/action.html
        :param _layout: The body layout, must contain {% include __template__ %}
        """
        page_meta()
        vars = dict(__NAME__=__title__, __VERSION__=__version__, __YEAR__=utc_now().year)
        for k, v in vars.items():
            setattr(g, k, v)

        if not _template:
            stack = inspect.stack()[1]
            action_name = stack[3]
            _template = build_endpoint_route_name(cls, action_name)
            _template = utils.list_replace(['.', ':'], '/', _template)
            _template = '%s.%s' % (_template, cls.template_markup)
        data = data or dict()
        data.update(kwargs)
        data['__template__'] = _template
        return render_template((_layout or cls.base_layout), **data)

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
            logging_config = {'version': 1, 'handlers': {'default': {'class': cls._app.config.get('LOGGING_CLASS', 'logging.StreamHandler')}}, 
               'loggers': {'': {'handlers': [
                                           'default'], 
                                'level': 'WARN'}}}
        logging.config.dictConfig(logging_config)
        cls.logger = logging.getLogger('root')
        cls._app._logger = cls.logger
        cls._app._loger_name = cls.logger.name

    @classmethod
    def _setup_db(cls):
        cls._app.db = None
        uri = cls._app.config.get('DB_URL')
        if uri:
            db._connect(uri, cls._app)
            cls._app.db = db
        return

    @classmethod
    def _expose_models(cls):
        if cls._app.db:
            register_models(**{m.__name__:m for m in cls._app.db.Model.__subclasses__() if not hasattr(models, m.__name__) if not hasattr(models, m.__name__)})

    @classmethod
    def _register(cls, app, base_route=None, subdomain=None, route_prefix=None, trailing_slash=True):
        """Registers a Harambe class for use with a specific instance of a
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
        if cls is Harambe:
            raise TypeError('cls must be a subclass of Harambe, not Harambe itself')
        module = cls.__module__.split('.')[(-1)]
        if not hasattr(views, module):
            setattr(views, module, type('', (), {}))
        mod = getattr(views, module)
        setattr(mod, cls.__name__, cls)
        if base_route:
            cls.orig_base_route = cls.base_route
            cls.base_route = base_route
        if route_prefix:
            cls.orig_route_prefix = cls.route_prefix
            cls.route_prefix = route_prefix
        if not subdomain:
            if hasattr(app, 'subdomain') and app.subdomain is not None:
                subdomain = app.subdomain
            elif hasattr(cls, 'subdomain'):
                subdomain = cls.subdomain
        if trailing_slash is not None:
            cls.orig_trailing_slash = cls.trailing_slash
            cls.trailing_slash = trailing_slash
        for name, value in get_interesting_members(Harambe, cls):
            proxy = cls.make_proxy_method(name)
            route_name = build_endpoint_route_name(cls, name)
            try:
                if hasattr(value, '_rule_cache') and name in value._rule_cache:
                    for idx, cached_rule in enumerate(value._rule_cache[name]):
                        rule, options = cached_rule
                        rule = cls.build_rule(rule)
                        sub, ep, options = cls.parse_options(options)
                        if not subdomain and sub:
                            subdomain = sub
                        if ep:
                            endpoint = ep
                        elif len(value._rule_cache[name]) == 1:
                            endpoint = route_name
                        else:
                            endpoint = '%s_%d' % (route_name, idx)
                        app.add_url_rule(rule, endpoint, proxy, subdomain=subdomain, **options)

                elif name in cls.__special_methods:
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
                    app.add_url_rule(rule, route_name, proxy, methods=methods, subdomain=subdomain)
                else:
                    methods = value._methods_cache if hasattr(value, '_methods_cache') else [
                     'GET']
                    name = utils.dasherize(name)
                    route_str = '/%s/' % name
                    if not cls.trailing_slash:
                        route_str = route_str.rstrip('/')
                    rule = cls.build_rule(route_str, value)
                    app.add_url_rule(rule, route_name, proxy, subdomain=subdomain, methods=methods)
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
        return

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
        proxy instantiates the Harambe subclass and calls the appropriate
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
                response = i.before_request(name, **request.view_args)
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
                    _template = build_endpoint_route_name(cls, view.__name__)
                    _template = utils.list_replace(['.', ':'], '/', _template)
                    _template = '%s.%s' % (_template, cls.template_markup)
                    response.setdefault('_template', _template)
                    response = i.render(**response)
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

        result = '/%s' % ('/').join(rule_parts)
        return re.sub('(/)\\1+', '\\1', result)

    @classmethod
    def get_base_route(cls):
        """Returns the route base to use for the current class."""
        base_route = cls.__name__.lower()
        if cls.base_route is not None:
            base_route = cls.base_route
            base_rule = parse_rule(base_route)
            cls.base_args = [ r[2] for r in base_rule ]
        return base_route.strip('/')

    @staticmethod
    def _bind_route_rule_cache(f, rule, append_method=False, **kwargs):
        if rule is None:
            rule = utils.dasherize(f.__name__) + '/'
        if not hasattr(f, '_rule_cache') or f._rule_cache is None:
            f._rule_cache = {f.__name__: [(rule, kwargs)]}
        elif f.__name__ not in f._rule_cache:
            f._rule_cache[f.__name__] = [
             (
              rule, kwargs)]
        elif append_method:
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
         'harambe.extras.jade.JadeTagExtension',
         'harambe.extras.md.MarkdownExtension',
         'harambe.extras.md.MarkdownTagExtension']
        if cls._app.config.get('COMPRESS_HTML'):
            extensions.append('harambe.extras.htmlcompress.HTMLCompress')
        for ext in extensions:
            cls._app.jinja_env.add_extension(ext)


HarambeApp = Harambe()

def build_endpoint_route_name(cls, method_name, class_name=None):
    """
    Build the route endpoint
    It is recommended to place your views in /views directory, so it can build
    the endpoint from it. If not, it will make the endpoint from the module name
    The main reason for having the views directory, it is explicitely easy
    to see the path of the view

    :param cls: The view class
    :param method_name: The name of the method
    :param class_name: To pass the class name.
    :return: string
    """
    module = cls.__module__.split('views.')[1] if '.views.' in cls.__module__ else cls.__module__.split('.')[(-1)]
    return '%s.%s:%s' % (module, class_name or cls.__name__, method_name)


def get_interesting_members(base_class, cls):
    """Returns a generator of methods that can be routed to"""
    base_members = dir(base_class)
    predicate = inspect.ismethod if _py2 else inspect.isfunction
    all_members = inspect.getmembers(cls, predicate=predicate)
    return (member for member in all_members if member[0] not in base_members and (hasattr(member[1], '__self__') and member[1].__self__ not in inspect.getmro(cls) if _py2 else True) and not member[0].startswith('_') and not member[0].startswith('before_') and not member[0].startswith('after_'))


def apply_function_to_members(cls, fn):
    for name, method in get_interesting_members(Harambe, cls):
        setattr(cls, name, fn(method))


def get_true_argspec(method):
    """Drills through layers of decorators attempting to locate the actual argspec for the method."""
    argspec = inspect.getargspec(method)
    args = argspec[0]
    if args and args[0] == 'self':
        return argspec
    else:
        if hasattr(method, '__func__'):
            method = method.__func__
        if not hasattr(method, '__closure__') or method.__closure__ is None:
            raise DecoratorCompatibilityError
        closure = method.__closure__
        for cell in closure:
            inner_method = cell.cell_contents
            if inner_method is method:
                continue
            if not inspect.isfunction(inner_method) and not inspect.ismethod(inner_method):
                continue
            true_argspec = get_true_argspec(inner_method)
            if true_argspec:
                return true_argspec

        return


class DecoratorCompatibilityError(Exception):
    pass


class RegexConverter(BaseConverter):

    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]