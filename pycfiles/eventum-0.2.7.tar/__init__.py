# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dan/working/eventum/eventum/__init__.py
# Compiled at: 2016-04-20 18:30:22
import json, logging, os
from jinja2 import ChoiceLoader, FileSystemLoader
from flask import current_app
from flask.ext.mongoengine import MongoEngine
from flask.ext.assets import Environment, Bundle
from webassets.filter import get_filter
from eventum.config import eventum_config

class Eventum(object):
    EXTENSION_NAME = 'eventum'
    ABSOLUTE_PATH_KEYS = ['EVENTUM_UPLOAD_FOLDER', 'EVENTUM_DELETE_FOLDER']

    def __init__(self, app=None):
        self._assets = None
        self.db = None
        self._gcal_client = None
        if app is not None:
            self.init_app(app)
        return

    def init_app(self, app):
        from eventum.lib.google_calendar import GoogleCalendarAPIClient
        from eventum.lib.google_web_server_auth import set_web_server_client_id
        from eventum.routes.base import configure_routing
        app.extensions = getattr(app, 'extensions', {})
        if self.EXTENSION_NAME not in app.extensions:
            app.extensions[self.EXTENSION_NAME] = self
        self.app = app
        self._normalize_client_settings()
        self._setdefault_eventum_settings()
        self.register_templates()
        self.db = MongoEngine(app)
        self.register_delete_rules()
        self.register_blueprints()
        configure_routing(app)
        self.register_scss()
        self._gcal_client = GoogleCalendarAPIClient(app)
        set_web_server_client_id(app)
        self.register_logger()

    @classmethod
    def gcal_client(cls):
        return current_app.extensions[cls.EXTENSION_NAME]._gcal_client

    def _normalize_client_settings(self):
        if 'EVENTUM_SETTINGS' in self.app.config:
            for key, value in self.app.config['EVENTUM_SETTINGS'].iteritems():
                self.app.config['EVENTUM_' + key] = value

        for key in self.ABSOLUTE_PATH_KEYS:
            self.app.config[key] = os.path.abspath(self.app.config[key])

    def _default_configurations_generator(self):
        for a in dir(eventum_config):
            if not a.startswith('_') and a.isupper():
                yield a

    def _setdefault_eventum_settings(self):
        for attr in self._default_configurations_generator():
            self.app.config.setdefault(attr, getattr(eventum_config, attr))

    def register_blueprints(self):
        from eventum.routes.base import register_error_handlers
        from eventum.routes import admin, auth, events, media, posts, users, whitelist, api, eventum
        admin_blueprints = [
         admin, auth, events, media, posts, users,
         whitelist, api, eventum]
        url_prefix = self.app.config['EVENTUM_URL_PREFIX']
        static_path = self.app.config['EVENTUM_STATIC_FOLDER']
        for bp in admin_blueprints:
            register_error_handlers(bp)
            self.app.register_blueprint(bp, url_prefix=url_prefix, static_path=static_path)

    def register_delete_rules(self):
        """Registers rules for how Mongoengine handles the deletion of objects
        that are being referenced by other objects.

        See the documentation for
        :func:`mongoengine.model.register_delete_rule` for more information.

        All delete rules for User fields must by DENY, because User objects
        should never be deleted.  Lists of reference fields should PULL, to
        remove deleted objects from the list, and all others should NULLIFY
        """
        from eventum.models import Event, EventSeries, User, Post, BlogPost, Image
        from mongoengine import NULLIFY, PULL, DENY
        Event.register_delete_rule(EventSeries, 'events', PULL)
        Image.register_delete_rule(BlogPost, 'images', PULL)
        Image.register_delete_rule(User, 'image', NULLIFY)
        Image.register_delete_rule(BlogPost, 'featured_image', NULLIFY)
        Image.register_delete_rule(Event, 'image', NULLIFY)
        EventSeries.register_delete_rule(Event, 'parent_series', NULLIFY)
        User.register_delete_rule(Event, 'creator', DENY)
        User.register_delete_rule(Image, 'creator', DENY)
        User.register_delete_rule(Post, 'author', DENY)
        User.register_delete_rule(Post, 'posted_by', DENY)

    def register_logger(self):
        """Create an error logger and attach it to ``app``."""
        max_bytes = int(self.app.config['EVENTUM_LOG_FILE_MAX_SIZE']) * 1024 * 1024
        Handler = logging.handlers.RotatingFileHandler
        f_str = '%(levelname)s @ %(asctime)s @ %(filename)s %(funcName)s %(lineno)d: %(message)s'
        access_handler = Handler(self.app.config['EVENTUM_WERKZEUG_LOG_NAME'], maxBytes=max_bytes)
        access_handler.setLevel(logging.INFO)
        logging.getLogger('werkzeug').addHandler(access_handler)
        app_handler = Handler(self.app.config['EVENTUM_APP_LOG_NAME'], maxBytes=max_bytes)
        formatter = logging.Formatter(f_str)
        app_handler.setLevel(logging.INFO)
        app_handler.setFormatter(formatter)
        self.app.logger.addHandler(app_handler)

    def register_templates(self):
        my_loader = ChoiceLoader([
         self.app.jinja_loader,
         FileSystemLoader(self.app.config['EVENTUM_TEMPLATE_FOLDER'])])
        self.app.jinja_loader = my_loader

    def register_scss(self):
        """Registers the Flask-Assets rules for scss compilation.  This reads
        from ``eventum/config/scss.json`` to make these rules.
        """
        self.assets.append_path(self.app.config['EVENTUM_STATIC_FOLDER'], '/static')
        bundle = Bundle('eventum_scss/eventum.scss', output='css/gen/eventum/eventum.%(version)s.css', depends='**/*.scss', filters=('scss',
                                                                                                                                     'cssmin'))
        self.assets.register('scss_eventum', bundle)

    @property
    def assets(self):
        if self._assets is not None:
            return self._assets
        else:
            if not hasattr(self.app.jinja_env, 'assets_environment') or not self.app.jinja_env.assets_environment:
                self._assets = Environment(self.app)
            self._assets = self.app.jinja_env.assets_environment
            return self._assets