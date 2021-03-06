# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Mardix/Dropbox/Projects/Python/web-portfolio/webmaster/core.py
# Compiled at: 2016-01-16 23:11:48
"""
Webmaster

"""
import re, os, sys, inspect, datetime, functools, logging, logging.config, utils, exceptions
from six import string_types
from werkzeug.contrib.fixers import ProxyFix
from werkzeug.routing import BaseConverter, parse_rule
from werkzeug.exceptions import Aborter
from flask import Flask, g, render_template, flash, session, url_for, request, redirect, make_response, Response
from flask_assets import Environment
import jinja2, __about__
_py2 = sys.version_info[0] == 2
NAME = __about__.name
__version__ = __about__.version
__author__ = __about__.author
__license__ = __about__.license
__copyright__ = __about__.copyright
__all__ = [
 'Webmaster',
 'View',
 'get_env',
 'get_env_config',
 'abort',
 'flash_data',
 'get_flashed_data',
 'init_app',
 'register_package',
 'flash',
 'session',
 'url_for',
 'request',
 'redirect']
_env_key = 'WEB_ENV'

def get_env():
    """
    Return the Capitalize environment name
    It can be used to retrieve class base config
    Default: Development
    :returns: str
    """
    env = 'Development'
    if _env_key in os.environ:
        env = os.environ[_env_key].lower().capitalize()
    return env


def get_env_config(config):
    """
    Return config class
    :param config : Object - The configuration module containing the environment object
    """
    return getattr(config, get_env())


def init_app(kls):
    """
    To bind middlewares, plugins that needs the 'app' object to init
    Bound middlewares will be assigned on cls.init()
    """
    if not hasattr(kls, '__call__'):
        raise TypeError("init_app: '%s' is not callable" % kls)
    View._init_apps.add(kls)
    return kls


def register_package(pkg):
    """
    Allow to register packages by loading and exposing: templates, static,
    and exceptions for abort()

    Structure of package
        root
            | $package_name
                | __init__.py
                |
                | exceptions.py
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
        root_pkg_dir = utils.get_pkg_resources_filename(pkg)
    template_path = os.path.join(root_pkg_dir, 'templates')
    static_path = os.path.join(root_pkg_dir, 'static')
    logging.info('Registering Package: ' + pkg)
    if os.path.isdir(template_path):
        template_path = jinja2.FileSystemLoader(template_path)
        View._template_paths.add(template_path)
    if os.path.isdir(static_path):
        View._static_paths.add(static_path)
        View._add_asset_bundle(static_path)
    if os.path.isfile(os.path.join(root_pkg_dir, 'exceptions.py')):
        exceptions = utils.import_string(pkg + '.exceptions')
        init_app(lambda x: abort.map_from_module(exceptions))


def flash_data(data):
    """
    Just like flash, but will save data
    :param data:
    :return:
    """
    session['_flash_data'] = data


def get_flashed_data():
    """
    Retrieved
    :return: mixed
    """
    return session.pop('_flash_data', None)


class CustomAborter(Aborter):
    """
    We'll modify abort, to also use the name of custom HTTPException classes
    """

    def __call__(self, code, *args, **kwargs):
        if isinstance(code, string_types):
            if code in self.mapping:
                raise self.get_exception(code)(*args, **kwargs)
        if not args and not kwargs and not isinstance(code, int):
            raise exceptions.HTTPException(response=code)
        if code not in self.mapping:
            raise LookupError('no exception for %r' % code)
        raise self.get_exception(code)(*args, **kwargs)

    def get_exception(self, code):
        """
        Expose the class based on the code
        :param code:
        :return:
        """
        raise self.mapping[code]

    def map_from_module(self, module):
        """
        Map all classes the in $module with subclasses of exceptions.HTTPException
        to be called as as error in with abort()
        :param obj:
        :return:
        """
        maps = {}
        for name in dir(module):
            obj = getattr(module, name)
            try:
                if issubclass(obj, exceptions.HTTPException):
                    maps[name] = obj
            except TypeError as ter:
                pass

        self.mapping.update(maps)


abort = CustomAborter()

class FlaskView(object):
    """Base view for any class based views implemented with Flask-Classy. Will
    automatically configure routes when registered with a Flask app instance.
    """
    decorators = []
    base_route = None
    route_prefix = None
    trailing_slash = True

    @classmethod
    def register(cls, app, base_route=None, subdomain=None, route_prefix=None, trailing_slash=None):
        """Registers a FlaskView class for use with a specific instance of a
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
        if cls is FlaskView:
            raise TypeError('cls must be a subclass of FlaskView, not FlaskView itself')
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
        members = get_interesting_members(FlaskView, cls)
        special_methods = ['get', 'put', 'patch', 'post', 'delete', 'index']
        for name, value in members:
            proxy = cls.make_proxy_method(name)
            route_name = cls.build_route_name(name)
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

                elif name in special_methods:
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
        proxy instantiates the FlaskView subclass and calls the appropriate
        method.
        :param name: the name of the method to create a proxy for
        """
        i = cls()
        view = getattr(i, name)
        if cls.decorators:
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
            if isinstance(response, dict):
                if hasattr(i, '_renderer'):
                    response = i._renderer(response)
                else:
                    df_v_t = '%s/%s.html' % (cls.__name__, view.__name__)
                    response.setdefault('template_', df_v_t)
                    response = i.render_(**response)
            if not isinstance(response, Response):
                response = make_response(response)
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
        if cls.base_route is not None:
            base_route = cls.base_route
            base_rule = parse_rule(base_route)
            cls.base_args = [ r[2] for r in base_rule ]
        elif cls.__name__.endswith('View'):
            base_route = cls.__name__[:-4].lower()
        else:
            base_route = cls.__name__.lower()
        return base_route.strip('/')

    @classmethod
    def build_route_name(cls, method_name):
        """Creates a unique route name based on the combination of the class
        name with the method name.

        :param method_name: the method name to use when building a route name
        """
        return cls.__name__ + ':%s' % method_name


class View(FlaskView):
    """ Webmaster """
    base_layout = 'layout.html'
    assets = None
    logger = None
    _app = None
    _init_apps = set()
    _template_paths = set()
    _static_paths = set()
    _asset_bundles = set()
    _default_page_meta = dict(title='', description='', url='', image='', site_name='', object_type='article', locale='', keywords=[], use_opengraph=True, use_googleplus=True, use_twitter=True, properties={})
    _global = dict(__NAME__=NAME, __VERSION__=__version__, __YEAR__=datetime.datetime.now().year, __META__=_default_page_meta)

    @classmethod
    def init(cls, flask_or_import_name, project=None, directory=None, config=None, exceptions=None, compress_html=True):
        """
        Allow to register all subclasses of Webmaster at once

        If a class doesn't have a route base, it will create a dasherize version
        of the class name.

        So we call it once initiating
        :param flask_or_import_name: Flask instance or import name -> __name__
        :param project: name of the project. If the directory and config is empty, it will guess them from here
        :param directory: The directory containing your project's Views, Templates and Static
        :param config: string of config object. ie: "app.config.Dev"
        :param exceptions: The exceptions path to load
        :param compress_html: bool - If true it will use the plugin "jinja2htmlcompress"
                to remove white spaces off the html resul
        """
        if isinstance(flask_or_import_name, Flask):
            app = flask_or_import_name
        else:
            app = Flask(flask_or_import_name)
        app.wsgi_app = ProxyFix(app.wsgi_app)
        app.url_map.converters['regex'] = RegexConverter
        if not directory:
            directory = 'application/%s' % project if project else '.'
        if not config:
            config = 'application.config.%s' % get_env()
        app.config.from_object(config)
        if compress_html:
            app.jinja_env.add_extension('webmaster.htmlcompress_ext.HTMLCompress')
        if directory:
            app.template_folder = directory + '/templates'
            app.static_folder = directory + '/static'
        abort.map_from_module(exceptions)
        cls._app = app
        cls._setup_logger()
        cls._add_asset_bundle(app.static_folder)
        cls.assets = Environment(cls._app)
        if cls._template_paths:
            loader = [
             cls._app.jinja_loader] + list(cls._template_paths)
            cls._app.jinja_loader = jinja2.ChoiceLoader(loader)
        if cls._static_paths:
            loader = [
             cls._app.static_folder] + list(cls._static_paths)
            cls.assets.load_path = loader
        [ _app(cls._app) for _app in cls._init_apps ]
        for subcls in cls.__subclasses__():
            base_route = subcls.base_route
            if not base_route:
                base_route = utils.dasherize(utils.underscore(subcls.__name__))
                if subcls.__name__.lower() == 'index':
                    base_route = '/'
            subcls.register(cls._app, base_route=base_route)

        [ cls.assets.from_yaml(a) for a in cls._asset_bundles ]

        @cls._app.after_request
        def _after_request_cleanup(response):
            cls._global['__META__'] = cls._default_page_meta
            return response

        return cls._app

    @classmethod
    def render_(cls, data={}, template_=None, layout_=None, **kwargs):
        """
        To render data to the associate template file of the action view
        :param data: The context data to pass to the template
        :param template_: The file template to use. By default it will map the classname/action.html
        :param layout_: The body layout, must contain {% include __template__ %}
        """
        if not template_:
            stack = inspect.stack()[1]
            module = inspect.getmodule(cls).__name__
            module_name = module.split('.')[(-1)]
            action_name = stack[3]
            view_name = cls.__name__
            if view_name.endswith('View'):
                view_name = view_name[:-4]
            template_ = '%s/%s.html' % (view_name, action_name)
        data = data or dict()
        data['__'] = cls._global
        if kwargs:
            data.update(kwargs)
        data['__template__'] = template_
        return render_template((layout_ or cls.base_layout), **data)

    @classmethod
    def meta_tags(cls, **kwargs):
        """
        Meta allows you to add meta data to site
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

        """
        page_meta = cls._global.get('__META__', {})
        page_meta.update(**kwargs)
        cls.g(__META__=page_meta)

    @classmethod
    def get_config(cls, key, default=None):
        """
        Shortcut to access the application's config in your class
        :param key: The key to access
        :param default: The default value when None
        :returns mixed:
        """
        return cls._app.config.get(key, default)

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
        logging_config = cls._app.config['LOGGING_CONFIG'] if 'LOGGING_CONFIG' in cls._app.config else None
        if not logging_config:
            logging_cls = cls._app.config['LOGGING_CLASS'] if 'LOGGING_CLASS' in cls._app.config else 'logging.StreamHandler'
            logging_config = {'version': 1, 
               'handlers': {'default': {'class': logging_cls}}, 
               'loggers': {'': {'handlers': [
                                           'default'], 
                                'level': 'WARN'}}}
        logging.config.dictConfig(logging_config)
        cls.logger = logging.getLogger('root')
        cls._app._logger = cls.logger
        cls._app._loger_name = cls.logger.name
        return


Webmaster = View

def get_interesting_members(base_class, cls):
    """Returns a list of methods that can be routed to"""
    base_members = dir(base_class)
    predicate = inspect.ismethod if _py2 else inspect.isfunction
    all_members = inspect.getmembers(cls, predicate=predicate)
    return [ member for member in all_members if member[0] not in base_members and (hasattr(member[1], '__self__') and member[1].__self__ not in inspect.getmro(cls) if _py2 else True) and not member[0].startswith('_') and not member[0].startswith('before_') and not member[0].startswith('after_')
           ]


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