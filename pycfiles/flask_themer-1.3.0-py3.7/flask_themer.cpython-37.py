# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flask_themer.py
# Compiled at: 2020-01-15 13:53:28
# Size of source mod 2**32: 7361 bytes
from pathlib import Path
from dataclasses import dataclass, field
from typing import Iterable, Callable, Union
from flask import render_template as flask_render_template
from flask import current_app, Blueprint, url_for, send_from_directory, abort
from jinja2 import TemplateNotFound
from jinja2.loaders import BaseLoader, FileSystemLoader
EXTENSION_KEY = 'themer'
CONFIG_PREFIX = 'THEMER_'
MAGIC_PATH_PREFIX = '☃'

class ThemeError(Exception):
    pass


class NoThemeResolver(ThemeError):
    pass


class ThemerNotInitialized(ThemeError, RuntimeError):
    pass


@dataclass
class Theme:
    theme_loader: 'ThemeLoader'
    jinja_loader: BaseLoader
    name: str
    data = field(default_factory=dict)
    data: dict


class ThemeLoader:

    @property
    def themes(self) -> Iterable[Theme]:
        """
        Return a dict mapping theme names to `Theme` instances.
        """
        raise NotImplementedError

    def get_static(self, theme: str, path: str) -> bytes:
        """
        Return a static asset for the given theme and path.
        """
        raise NotImplementedError


class FileSystemThemeLoader(ThemeLoader):
    __doc__ = 'A simple theme loader that assumes all sub-directories immediately under\n    `path` are themes.\n    '

    def __init__(self, path: Union[(Path, str)], filter: Callable[([Path], bool)]=None):
        self.path = Path(path)
        self._filter = filter

    @property
    def themes(self):
        themes = {}
        if self.path.exists():
            for child in self.path.iterdir():
                if not child.is_dir():
                    continue
                if self._filter:
                    if not self._filter(child):
                        continue
                yield Theme(jinja_loader=(FileSystemLoader(str(child))),
                  theme_loader=self,
                  name=(child.name))

        return themes

    def get_static(self, theme, path):
        return send_from_directory(self.path / theme / 'static', path)


class Themer:

    def __init__(self, app=None, *, loaders=None):
        self.loaders = []
        self.themes = {}
        self._theme_resolver = None
        if app is not None:
            self.init_app(app, loaders=loaders)

    def init_app(self, app, *, loaders=None):
        """Configure `app` to work with Flask-Themer and pre-populate the
        list of themes we know about."""
        app.extensions[EXTENSION_KEY] = self
        default_dir = app.config.setdefault(f"{CONFIG_PREFIX}DEFAULT_DIRECTORY", 'themes')
        app.add_template_global(lookup_theme_path, name='theme')
        app.add_template_global(lookup_static_theme_path, name='theme_static')
        app.register_blueprint(theme_blueprint)
        self.loaders = loaders or [
         FileSystemThemeLoader(Path(app.root_path) / default_dir)]
        for loader in self.loaders:
            for theme in loader.themes:
                self.themes[theme.name] = theme

    def current_theme_loader(self, loader):
        """Set the resolver to use when looking up the currently active
        theme.

        Ex:

            .. code-block:: python

                @themer.current_theme_loader
                def get_current_theme():
                    return current_user.settings.theme
        """
        self._theme_resolver = loader
        return loader

    @property
    def current_theme(self):
        """The currently active theme."""
        if not self._theme_resolver:
            raise NoThemeResolver('No current theme resolver is registered, set one using current_theme_loader.')
        return self._theme_resolver()


def render_template(path, *args, **kwargs):
    """Identical to flask's render_template, but loads from the active theme if
    one is available.
    """
    try:
        return flask_render_template(lookup_theme_path(path), *args, **kwargs)
    except TemplateNotFound:
        return flask_render_template(path, *args, **kwargs)


def lookup_theme_path(path):
    """Given the path to a template, lookup the "real" path after resolving the
    active theme.
    """
    themer = _current_themer()
    return f"{MAGIC_PATH_PREFIX}/{themer.current_theme}/{path}"


def lookup_static_theme_path(path, **kwargs):
    themer = _current_themer()
    return url_for(
 f"{MAGIC_PATH_PREFIX}.static", theme=themer.current_theme, 
     filename=path, **kwargs)


def _current_themer() -> Themer:
    """Returns the currently active Themer instance."""
    try:
        return current_app.extensions[EXTENSION_KEY]
    except KeyError:
        raise ThemerNotInitialized('Trying to use an uninitalized Themer, make sure you call init_app')


class _ThemeTemplateLoader(BaseLoader):
    __doc__ = "\n    Flask provides two mechanisms for replacing the jinja loader,\n    create_global_jinja_loader and jinja_loader.  However, these can't be\n    overloaded by extensions. A Blueprint with a custom jinja_loader\n    is used to get the same effect. This works because the default Flask\n    template loader (DispatchTemplateLoader) looks at the app and *all*\n    blueprint template folders when resolving a template path. This technique\n    is borrowed from flask-themes.\n    "

    def get_source(self, environment, template):
        if not template.startswith(MAGIC_PATH_PREFIX):
            raise TemplateNotFound(template)
        path = template[len(MAGIC_PATH_PREFIX) + 1:]
        try:
            theme, path = path.split('/', 1)
        except ValueError:
            raise TemplateNotFound(template)

        themer = _current_themer()
        if theme in themer.themes:
            return themer.themes[theme].jinja_loader.get_source(environment, path)
        raise TemplateNotFound(template)


theme_blueprint = Blueprint((f"{MAGIC_PATH_PREFIX}"), __name__)
setattr(theme_blueprint, 'jinja_loader', _ThemeTemplateLoader())

@theme_blueprint.route('/static/<theme>/<path:filename>', endpoint='static')
def serve_static(theme, filename):
    themer = _current_themer()
    try:
        t = themer.themes[theme]
    except KeyError:
        abort(404)

    return t.theme_loader.get_static(theme, filename)