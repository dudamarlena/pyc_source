# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/flask-sapo-ink/flask_ink/ink.py
# Compiled at: 2017-08-30 15:45:55
# Size of source mod 2**32: 1382 bytes
import flask
from flask_ink import assets
__version__ = '3.1.10'

class Ink(object):

    def __init__(self, app):
        self.app = app
        self.init_app()

    def init_app(self):
        self.app.config.setdefault('INK_MINIFIED_ASSETS', False)
        self.app.config.setdefault('INK_VERSION', __version__)
        self.app.config.setdefault('INK_DEFAULT_ASSET_LOCATION', 'sapo')
        minified_assets = self.app.config['INK_MINIFIED_ASSETS']
        asset_version = self.app.config['INK_VERSION']
        asset_location = self.app.config['INK_DEFAULT_ASSET_LOCATION']
        self.assets = assets.AssetManager(minified=minified_assets, asset_version=asset_version)
        self.make_default_asset_locations()
        self.assets.default_location = asset_location
        blueprint = flask.Blueprint('ink', __name__, template_folder='templates', static_folder='static', static_url_path=self.app.static_url_path + '/ink')
        self.app.register_blueprint(blueprint)
        self.app.jinja_env.globals.update(ink_load_asset=self.assets.load)

    def make_default_asset_locations(self):
        sapo = assets.SapoCDN()
        local = assets.LocalAssets()
        self.assets.register_location('sapo', sapo)
        self.assets.register_location('local', local)