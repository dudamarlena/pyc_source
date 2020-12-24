# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/mopidy_jukepi/__init__.py
# Compiled at: 2015-04-01 05:48:27
from __future__ import unicode_literals
import os, json, tornado.web
from mopidy import config, ext
__version__ = b'1.0.0'

class Extension(ext.Extension):
    dist_name = b'Mopidy-jukePi'
    ext_name = b'jukepi'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), b'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        schema[b'websocket_url'] = config.String(True)
        schema[b'lastfm_api_key'] = config.String(True)
        schema[b'lastfm_api_secret'] = config.String(True)
        schema[b'custom_scripts'] = config.List(True)
        schema[b'jukepi_callback'] = config.String(True)
        schema[b'search_uris'] = config.List(True)
        return schema

    def setup(self, registry):
        registry.add(b'http:app', {b'name': self.ext_name, 
           b'factory': jukepi_app_factory})


def jukepi_app_factory(config, core):
    return [
     (
      b'/', JukePiRequestHandler, {b'core': core, b'config': config}),
     (
      b'/(.*)', tornado.web.StaticFileHandler, {b'path': os.path.join(os.path.dirname(__file__), b'static')})]


def serialize_config(config):
    serialized = {}
    if config.get(b'websocket_url'):
        serialized[b'mopidyWebSocketUrl'] = config.get(b'websocket_url')
    if config.get(b'lastfm_api_key'):
        serialized[b'lastfm'] = {}
        serialized[b'lastfm'][b'key'] = config.get(b'lastfm_api_key')
        serialized[b'lastfm'][b'secret'] = config.get(b'lastfm_api_secret')
    serialized[b'searchUris'] = config.get(b'search_uris')
    return json.dumps(serialized)


class JukePiRequestHandler(tornado.web.RequestHandler):

    def initialize(self, core, config):
        self.core = core
        self.config = config
        self.js_settings = serialize_config(config.get(b'jukepi'))

    def get(self):
        self.render(b'templates/index.html', **{b'js_settings': self.js_settings, 
           b'custom_scripts': self.config.get(b'jukepi').get(b'custom_scripts'), 
           b'jukepi_callback': self.config.get(b'jukepi').get(b'jukepi_callback')})