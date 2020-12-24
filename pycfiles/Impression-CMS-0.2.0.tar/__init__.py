# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/scottblevins/git/impression/impression/__init__.py
# Compiled at: 2016-07-22 10:54:23
__author__ = 'Scott Blevins'
__email__ = 'scott@britecore.com'
__version__ = '1.0'
from flask import Flask, g
from webassets.loaders import PythonLoader as PythonAssetsLoader
from impression.controllers.main import main_controller
from impression.controllers.admin import admin_controller
from impression.controllers.file import file_controller
from impression import assets
from impression.models import db
from impression.controls import get_setting
from impression.decorators import import_user
from impression.extensions import cache, assets_env, debug_toolbar, themes2, login_manager

def before_app_request():
    g.user = None
    g.theme = get_setting('blog-theme', 'impression')
    g.bootstrap_theme = get_setting('bootstrap-theme', 'yeti')
    g.syntax_highlighting_theme = get_setting('syntax-highlighting-theme', 'monokai.css')
    g.blog_title = get_setting('blog-title', 'Blog Title')
    g.blog_copyright = get_setting('blog-copyright', 'Blog Copyright')
    g.upload_directory = get_setting('upload-directory', 'uploads/')
    g.allowed_extensions = get_setting('allowed-extensions', ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'tiff'])
    g.max_file_size = get_setting('max-file-size', 16777216)
    g.user = import_user()
    return


def create_app(object_name):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    Arguments:
        object_name: the python path of the config object,
                     e.g. impression.settings.ProdConfig

        env: The name of the current environment, e.g. prod or dev
    """
    app = Flask(__name__)
    app.config.from_object(object_name)
    cache.init_app(app)
    if debug_toolbar:
        debug_toolbar.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    assets_env.init_app(app)
    assets_loader = PythonAssetsLoader(assets)
    for name, bundle in assets_loader.load_bundles().items():
        assets_env.register(name, bundle)

    main_controller.before_request(before_app_request)
    app.register_blueprint(main_controller)
    admin_controller.before_request(before_app_request)
    app.register_blueprint(admin_controller)
    file_controller.before_request(before_app_request)
    app.register_blueprint(file_controller)
    themes2.init_themes(app, app_identifier='impression')
    return app