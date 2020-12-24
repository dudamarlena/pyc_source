# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\Projects\flask-microservices\flask_microservices\main.py
# Compiled at: 2017-01-25 04:25:19
# Size of source mod 2**32: 4670 bytes
from flask import Blueprint, Flask, __version__
from flask.globals import _request_ctx_stack
from flask.helpers import send_from_directory
from flask.templating import DispatchingJinjaLoader
from .exceptions import InvalidModulePath
from collections import namedtuple
from importlib import import_module
import os
FLASK_VERSION = float(__version__)

class MicroServicesApp(Flask):
    __doc__ = "Extends the default Flask app to attempt to locate static\n    files from Blueprints before 404'ing.\n    "

    def __init__(self, name):
        super(MicroServicesApp, self).__init__(name)
        self.jinja_options = self.jinja_options.copy()
        self.jinja_options['loader'] = MicroServicesLoader(self)

    def register_urls(self, modules, path='modules'):
        """Resolves a given app, module list, and module path into
        usable blueprints.
        """
        cwd = self.root_path
        path = os.path.normpath(path)
        module_dir = os.path.join(cwd, path)
        if not os.path.exists(module_dir):
            exception_message = 'Invalid module path provided. With the given path, your modules should be located at {}'.format(module_dir)
            raise InvalidModulePath(exception_message)
        app_name = os.path.split(cwd)[(-1)]
        module_location = '.'.join(os.path.split(path))
        if module_location.startswith('.'):
            module_location = module_location[1:]
        if module_location.endswith('.'):
            module_location = module_location[:-1]
        module_hierarchy = '{}.{}'.format(app_name, module_location)
        for module_name in modules:
            formatted_module = '{}.{}'.format(module_hierarchy, module_name)
            _MicroServicesApp__module = import_module(formatted_module)
            self.register_blueprint(_MicroServicesApp__module.blueprint)

    def send_static_file(self, filename):
        for blueprint_name, blueprint in self.blueprints.items():
            filepath = os.path.join(blueprint.static_folder, filename)
            if os.path.exists(filepath):
                return send_from_directory(blueprint.static_folder, filename)

        return super(MicroServicesApp, self).send_static_file(filename)


class Router(Blueprint):
    __doc__ = 'URL Routing syntas xugar.'

    @classmethod
    def create_blueprint(cls, module_name, import_name):
        return cls(module_name, import_name, static_folder='static', template_folder='templates', static_url_path='/static_{}'.format(module_name), url_prefix=None)

    def register_urls(self, urls):
        for _url in urls:
            self.add_url_rule(rule=_url.rule, endpoint=_url.name, view_func=_url.view_func, methods=_url.methods)


class MicroServicesLoader(DispatchingJinjaLoader):
    __doc__ = 'Prevent template namespace collisions between modules.\n\n    Additionally, prefer local templates to global templates.\n    This means that global templates will no longer override local templates.\n    '

    def _iter_loaders(self, template):
        blueprint = _request_ctx_stack.top.request.blueprint
        if blueprint is not None and blueprint in self.app.blueprints:
            loader = self.app.blueprints[blueprint].jinja_loader
            if loader is not None:
                if FLASK_VERSION <= 0.1:
                    yield (
                     loader, template)
        else:
            yield (
             blueprint, loader)
        loader = self.app.jinja_loader
        if loader is not None:
            if FLASK_VERSION <= 0.1:
                yield (
                 loader, template)
        else:
            yield (
             self.app, loader)


def url(rule, view_func, name=None, methods=['GET']):
    """Simple URL wrapper for `Flask-MicroServices.Router`.

    Usage:
    ```
    from . import views

    url('/explore/', view_func=views.explore_home, name='explore_home', methods=['GET'])
    url('/explore/', view_func=views.explore_home, name='explore_home')
    url('/explore/', views.explore_home, 'explore_home')
    url('/explore/', views.explore_home)
    ```

    # Note that 'endpoint' is now 'name'.
    # Note also that the name and view_func parameters are reversed from that
    of a normal flask URL.
    """
    __url = namedtuple('Url', ['rule', 'name', 'view_func', 'methods'])
    return __url(rule, name, view_func, methods)