# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Mardix/Dropbox/Projects/Python/Flasik/flasik/core.py
# Compiled at: 2019-09-08 01:08:07
"""
core.py

This is the Flasik core. it contains the classes and functions

"""
import re, os, sys, six, arrow, jinja2, inspect, logging, werkzeug, functools
from . import utils
import pkg_resources, logging.config
from .__about__ import *
from .flasik_db import FlasikDB
from flask_assets import Environment
from werkzeug.contrib.fixers import ProxyFix
from werkzeug.routing import BaseConverter, parse_rule
from flask import Flask, g, render_template, flash, session, make_response, Response, request, abort, url_for as f_url_for, redirect as f_redirect
__KEY__ = 'flasik'
__all__ = [
 'Flasik',
 'db',
 'models',
 'views',
 'get_config',
 'get_project_env',
 'set_page_context',
 'extends',
 'flash',
 'session',
 'abort',
 'g',
 'redirect',
 'url_for',
 'ext']

def is_method(x):
    if six.PY2:
        return inspect.ismethod
    return inspect.isfunction


views = type('', (), {})
models = type('', (), {})
db = FlasikDB()
ext = type('', (), {})

def get_project_env():
    """
    if the app and the envi are passed in the command line as 'FLASIK_PROJECT=$project_name:$config_env'
    If the string doesn't have the colon, it will use the value as config_env
    :return: tuple (project_name, config_env)
    """
    project_name, config_env = ('default', 'Dev')
    if 'FLASIK_PROJECT' in os.environ:
        project = os.environ['FLASIK_PROJECT'].lower()
        if project:
            if ':' in project:
                project_name, config_env = os.environ['FLASIK_PROJECT'].split(':', 2)
            else:
                config_env = project
    return (
     project_name, config_env.lower().capitalize())


def extends(kls):
    """
    To bind middlewares, plugins that needs the 'app' context to initialize
    Bound middlewares will be assigned on cls.init()
    Usage:

    # As a function
    def myfn(app):
        pass

    extends(myfn)

    # As a decorator
    @extends
    def myfn(app):
        pass

    """
    if not hasattr(kls, '__call__'):
        raise FlasikError("extends: '%s' is not callable" % kls)
    Flasik._init_apps.add(kls)
    return kls


def get_config(key, default=None):
    """
    Shortcut to access the application's config in your class
    :param key: The key to access
    :param default: The default value when None
    :returns mixed:
    """
    if Flasik._app:
        return Flasik._app.config.get(key, default)
    return default


def set_page_context(**kwargs):
    """
    To set page context
    Page  allows you to add page meta data in the request `g` context
    :params **kwargs:

    meta keys we're expecting:
        title (str)
        description (str)
        url (str) (Will pick it up by itself if not set)
        image (str)
        site_name (str) (but can pick it up from config file)
        keywords (list)
        locale (str)

    """
    default = dict(title=None, description=None, keywords=None, url=None, image=None, site_name=None, locale=None)
    key = 'PAGE_CONTEXT'
    context = getattr(g, key, default)
    context.update(**kwargs)
    setattr(g, key, context)
    return


class FlasikError(Exception):
    """
    This exception is not reserved, but it used for all Flasik exception.
    It helps catch Core problems.
    """
    pass


def url_for(endpoint, **kw):
    """
    Flasik url_for is an alias to the flask url_for, with the ability of
    passing the function signature to build the url, without knowing the endpoint
    :param endpoint:
    :param kw:
    :return:
    """
    _endpoint = None
    if isinstance(endpoint, six.string_types):
        return f_url_for(endpoint, **kw)
    else:
        if isinstance(endpoint, Flasik):
            fn = sys._getframe().f_back.f_code.co_name
            endpoint = getattr(endpoint, fn)
        if is_method(endpoint):
            _endpoint = _get_action_endpoint(endpoint)
            if not _endpoint:
                _endpoint = _build_endpoint_route_name(endpoint)
        if _endpoint:
            return f_url_for(_endpoint, **kw)
        raise FlasikError('Flasik `url_for` received an invalid endpoint')
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
    if isinstance(endpoint, six.string_types):
        _endpoint = endpoint
        if '/' in endpoint:
            return f_redirect(endpoint)
        for r in Flasik._app.url_map.iter_rules():
            _endpoint = endpoint
            if 'GET' in r.methods and endpoint in r.endpoint:
                _endpoint = r.endpoint
                break

    else:
        if isinstance(endpoint, Flasik):
            fn = sys._getframe().f_back.f_code.co_name
            endpoint = getattr(endpoint, fn)
        if is_method(endpoint):
            _endpoint = _get_action_endpoint(endpoint)
            if not _endpoint:
                _endpoint = _build_endpoint_route_name(endpoint)
    if _endpoint:
        return f_redirect(url_for(_endpoint, **kw))
    else:
        raise FlasikError('Invalid endpoint')
        return


class Flasik(object):
    decorators = []
    base_route = None
    route_prefix = None
    trailing_slash = True
    assets = None
    _ext = set()
    __special_methods = ['get', 'put', 'patch', 'post', 'delete', 'index']
    _app = None
    _init_apps = set()
    _template_paths = set()
    _static_paths = set()
    _asset_bundles = set()

    @classmethod
    def Initialize(cls, flask_or_import_name, projects, project_name=None):
        """
        Initialize Flasik
        :param flask_or_import_name: Flask instance or import name -> __name__
        :param projects: dict of applications/views to load. ie:
            {
                "default": [
                    "application",
                    "another.app.path"
                ]
            }
        :param project_name: name of the project. If empty, it will try to get
                             it from the get_project_env(). By default it is "default"
                             The app default is set as environment variable
                             ie: app=PROJECT_NAME:CONFIG -> app=default:production
        :return:
        """
        if not project_name:
            project_name = get_project_env()[0]
        config_env = get_project_env()[1]
        app = flask_or_import_name if isinstance(flask_or_import_name, Flask) else Flask(flask_or_import_name)
        app.url_map.converters['regex'] = RegexConverter
        app.config.from_object('__config__.%s' % config_env)
        if app.config.get('USE_PROXY_FIX', True):
            app.wsgi_app = werkzeug.contrib.fixers.ProxyFix(app.wsgi_app)
        cls._app = app
        cls.assets = Environment(cls._app)
        cls._setup_db()
        try:
            if project_name not in projects:
                raise FlasikError('Missing project: %s' % project_name)
            for view in projects[project_name]:
                werkzeug.import_string('%s.__models__' % view)
                cls._expose_models()
                werkzeug.import_string('%s.__views__' % view)
                _register_application_template(view, view)

        except ImportError as ie1:
            logging.critical(ie1)

        [ _app(cls._app) for _app in cls._init_apps ]
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
    def render(cls, data={}, template=None, **kwargs):
        """
        Render the view template based on the class and the method being invoked
        :param data: The context data to pass to the template
        :param template: The file template to use. By default it will map the module/classname/action.html
        """
        set_page_context()
        vars = dict(__NAME__=__title__, __VERSION__=__version__, __YEAR__=arrow.utcnow().year)
        for k, v in vars.items():
            setattr(g, k, v)

        if not template:
            stack = inspect.stack()[1]
            action_name = stack[3]
            template = make_template_path(cls, action_name)
        data = data or {}
        data.update(kwargs)
        return render_template(template, **data)

    @classmethod
    def _add_asset_bundle(cls, path):
        """
        Add a webassets bundle yml file
        """
        f = '%s/assets.yml' % path
        if os.path.isfile(f):
            cls._asset_bundles.add(f)

    @classmethod
    def _setup_db(cls):
        """
        Setup the DB connection if DB_URL is set
        """
        uri = cls._app.config.get('DB_URL')
        if uri:
            db.connect__(uri, cls._app)

    @classmethod
    def _expose_models(cls):
        """
        Register the models and assign them to `models`
        :return:
        """
        if db._IS_OK_:
            _register_models(**{m.__name__:m for m in db.Model.__subclasses__() if not hasattr(models, m.__name__) if not hasattr(models, m.__name__)})

    @classmethod
    def _register(cls, app, base_route=None, subdomain=None, route_prefix=None, trailing_slash=True):
        """Registers a Flasik class for use with a specific instance of a
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
        if cls is Flasik:
            raise TypeError('cls must be a subclass of Flasik, not Flasik itself')
        module = cls.__module__
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
        for name, value in get_interesting_members(Flasik, cls):
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
        proxy instantiates the Flasik subclass and calls the appropriate
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
                    template = make_template_path(cls, view.__name__)
                    response.setdefault('template', template)
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


def _bind_route_rule_cache(f, rule, append_method=False, **kwargs):
    """
    Put the rule cache on the method itself instead of globally
    :param f:
    :param rule:
    :param append_method:

    """
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


def build_endpoint_route_name(cls, method_name, class_name=None):
    """
    Build the route endpoint
    It is recommended to place your views in /views directory, so it can build
    the endpoint from it. If not, it will make the endpoint from the module name
    The main reason for having the views directory, it is explicitly easy
    to see the path of the view

    :param cls: The view class
    :param method_name: The name of the method
    :param class_name: To pass the class name.
    :return: string
    """
    return '%s.%s:%s' % (cls.__module__, class_name or cls.__name__, method_name)


def make_template_path(cls, method_name):
    _template = build_endpoint_route_name(cls, method_name)
    m = _template.split('.')
    if '__views__' in m[1]:
        m.remove('__views__')
    _template = ('.').join(list(m))
    _template = utils.list_replace(['.', ':'], '/', _template)
    return '%s.html' % _template


def get_interesting_members(base_class, cls):
    """Returns a generator of methods that can be routed to"""
    base_members = dir(base_class)
    predicate = inspect.ismethod if six.PY2 else inspect.isfunction
    all_members = inspect.getmembers(cls, predicate=predicate)
    return (member for member in all_members if member[0] not in base_members and (hasattr(member[1], '__self__') and member[1].__self__ not in inspect.getmro(cls) if six.PY2 else True) and not member[0].startswith('_') and not member[0].startswith('before_') and not member[0].startswith('after_'))


def apply_function_to_members(cls, fn):
    """
    Apply a function to all the members of a class.
    Used for decorators that is applied in a class and want all the members
    to use it
    :param cls: class
    :param fn: function
    :return: 
    """
    for name, method in get_interesting_members(Flasik, cls):
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


_views_attr = {}

def set_view_attr(view, key, value, cls_name=None):
    """
    Set the view attributes
    :param view: object (class or instance method)
    :param key: string - the key
    :param value: mixed - the value
    :param cls_name: str - To pass the class name associated to the view
            in the case of decorators that may not give the real class name
    :return: 
    """
    ns = view_namespace(view, cls_name)
    if ns:
        if ns not in _views_attr:
            _views_attr[ns] = {}
        _views_attr[ns][key] = value


def get_view_attr(view, key, default=None, cls_name=None):
    """
    Get the attributes that was saved for the view
    :param view: object (class or instance method)
    :param key: string - the key
    :param default: mixed - the default value
    :param cls_name: str - To pass the class name associated to the view
            in the case of decorators that may not give the real class name
    :return: mixed
    """
    ns = view_namespace(view, cls_name)
    if ns:
        if ns not in _views_attr:
            return default
        return _views_attr[ns].get(key, default)
    return default


def view_namespace(view, cls_name=None):
    """
    Create the namespace from the view
    :param view: object (class or instance method)
    :param cls_name: str - To pass the class name associated to the view
            in the case of decorators that may not give the real class name
    :return: string or None
    """
    ns = view.__module__
    if inspect.isclass(view):
        ns += '.%s' % view.__name__
    else:
        if hasattr(view, 'im_class') or hasattr(view, 'im_self'):
            if view.im_class is not None:
                cls_name = view.im_class.__name__
            elif view.im_self is not None:
                cls_name = view.im_self.__name__
        if cls_name is None:
            return
        ns += '.%s.%s' % (cls_name, view.__name__)
    return ns


def _register_models(**kwargs):
    """
    Alias to register model
    :param kwargs:
    :return:
    """
    [ setattr(models, k, v) for k, v in kwargs.items() ]


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
                    for r in Flasik._app.url_map.iter_rules():
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


def _register_application_template(pkg, prefix):
    """
    Allow to register an app templates by loading and exposing: templates, static,
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
    :param prefix: str - to prefix the template path
    """
    root_pkg_dir = pkg
    if not os.path.isdir(pkg):
        root_pkg_dir = pkg_resources.resource_filename(pkg, '')
    template_path = os.path.join(root_pkg_dir, 'templates')
    static_path = os.path.join(root_pkg_dir, 'static')
    if os.path.isdir(template_path):
        loader = jinja2.FileSystemLoader(template_path)
        ploader = jinja2.PrefixLoader({prefix: loader})
        loader = ploader
        Flasik._template_paths.add(loader)
    if os.path.isdir(static_path):
        Flasik._static_paths.add(static_path)
        Flasik._add_asset_bundle(static_path)