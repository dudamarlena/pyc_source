# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/app.py
# Compiled at: 2016-03-29 15:18:42
# Size of source mod 2**32: 13232 bytes
import os, logging
from contextlib import contextmanager
from mediagoblin.routing import get_url_map
from mediagoblin.tools.routing import endpoint_to_controller
from werkzeug.wrappers import Request
from werkzeug.exceptions import HTTPException
from werkzeug.routing import RequestRedirect
from werkzeug.wsgi import SharedDataMiddleware
from mediagoblin import meddleware, __version__
from mediagoblin.db.util import check_db_up_to_date
from mediagoblin.tools import common, session, translate, template
from mediagoblin.tools.response import render_http_exception
from mediagoblin.tools.theme import register_themes
from mediagoblin.tools import request as mg_request
from mediagoblin.media_types.tools import media_type_warning
from mediagoblin.mg_globals import setup_globals
from mediagoblin.init.celery import setup_celery_from_config
from mediagoblin.init.plugins import setup_plugins
from mediagoblin.init import get_jinja_loader, get_staticdirector, setup_global_and_app_config, setup_locales, setup_workbench, setup_database, setup_storage
from mediagoblin.tools.pluginapi import PluginManager, hook_transform
from mediagoblin.tools.crypto import setup_crypto
from mediagoblin.auth.tools import check_auth_enabled, no_auth_logout
from mediagoblin.tools.transition import DISABLE_GLOBALS
_log = logging.getLogger(__name__)

class Context(object):
    __doc__ = '\n    MediaGoblin context object.\n\n    If a web request is being used, a Flask Request object is used\n    instead, otherwise (celery tasks, etc), attach things to this\n    object.\n\n    Usually appears as "ctx" in utilities as first argument.\n    '


class MediaGoblinApp(object):
    __doc__ = '\n    WSGI application of MediaGoblin\n\n    ... this is the heart of the program!\n    '

    def __init__(self, config_path, setup_celery=True):
        """
        Initialize the application based on a configuration file.

        Arguments:
         - config_path: path to the configuration file we're opening.
         - setup_celery: whether or not to setup celery during init.
           (Note: setting 'celery_setup_elsewhere' also disables
           setting up celery.)
        """
        _log.info('GNU MediaGoblin %s main server starting', __version__)
        _log.debug('Using config file %s', config_path)
        self.global_config, self.app_config = setup_global_and_app_config(config_path)
        media_type_warning()
        setup_crypto(self.app_config)
        self.session_manager = session.SessionManager()
        setup_locales()
        _log.info('Setting up plugins.')
        setup_plugins()
        if DISABLE_GLOBALS:
            self.db_manager = setup_database(self)
        else:
            self.db = setup_database(self)
        self.theme_registry, self.current_theme = register_themes(self.app_config)
        self.template_loader = get_jinja_loader(self.app_config.get('local_templates'), self.current_theme, PluginManager().get_template_paths())
        self.auth = check_auth_enabled()
        if not self.auth:
            self.app_config['allow_comments'] = False
        self.public_store, self.queue_store = setup_storage()
        self.url_map = get_url_map()
        self.staticdirector = get_staticdirector(self.app_config)
        if setup_celery:
            if not self.app_config.get('celery_setup_elsewhere'):
                if os.environ.get('CELERY_ALWAYS_EAGER', 'false').lower() == 'true':
                    setup_celery_from_config(self.app_config, self.global_config, force_celery_always_eager=True)
                else:
                    setup_celery_from_config(self.app_config, self.global_config)
        if not DISABLE_GLOBALS:
            setup_globals(app=self)
        self.workbench_manager = setup_workbench()
        self.meddleware = [common.import_component(m)(self) for m in meddleware.ENABLED_MEDDLEWARE]

    @contextmanager
    def gen_context(self, ctx=None, **kwargs):
        """
        Attach contextual information to request, or generate a context object

        This avoids global variables; various utilities and contextual
        information (current translation, etc) are attached to this
        object.
        """
        if DISABLE_GLOBALS:
            with self.db_manager.session_scope() as (db):
                yield self._gen_context(db, ctx)
        else:
            yield self._gen_context(self.db, ctx)

    def _gen_context(self, db, ctx, **kwargs):
        if ctx is None:
            ctx = Context()
        ctx.app = self
        ctx.db = db
        ctx.staticdirect = self.staticdirector
        if isinstance(ctx, Request):
            ctx = self._request_only_gen_context(ctx)
        return ctx

    def _request_only_gen_context(self, request):
        """
        Requests get some extra stuff attached to them that's not relevant
        otherwise.
        """
        request.session = self.session_manager.load_session_from_cookie(request)
        request.locale = translate.get_locale_from_request(request)
        request.template_env = template.get_jinja_env(self, self.template_loader, request.locale)
        mg_request.setup_user_in_request(request)
        request.map_adapter = self.url_map.bind_to_environ(request.environ)

        def build_proxy(endpoint, **kw):
            try:
                qualified = kw.pop('qualified')
            except KeyError:
                qualified = False

            return request.map_adapter.build(endpoint, values=dict(**kw), force_external=qualified)

        request.urlgen = build_proxy
        return request

    def call_backend(self, environ, start_response):
        request = Request(environ)
        request.GET = request.args
        request.full_path = environ['SCRIPT_NAME'] + request.path
        if environ.get('HTTPS', '').lower() == 'off':
            environ.pop('HTTPS')
        with self.gen_context(request) as (request):
            return self._finish_call_backend(request, environ, start_response)

    def _finish_call_backend(self, request, environ, start_response):
        no_auth_logout(request)
        request.controller_name = None
        try:
            found_rule, url_values = request.map_adapter.match(return_rule=True)
            request.matchdict = url_values
        except RequestRedirect as response:
            return response(environ, start_response)
        except HTTPException as exc:
            return render_http_exception(request, exc, exc.get_description(environ))(environ, start_response)

        controller = endpoint_to_controller(found_rule)
        request.controller_name = found_rule.endpoint
        try:
            for m in self.meddleware:
                response = m.process_request(request, controller)
                if response is not None:
                    return response(environ, start_response)

        except HTTPException as e:
            return render_http_exception(request, e, e.get_description(environ))(environ, start_response)

        request = hook_transform('modify_request', request)
        request.start_response = start_response
        try:
            response = controller(request)
        except HTTPException as e:
            response = render_http_exception(request, e, e.get_description(environ))

        try:
            for m in self.meddleware[::-1]:
                m.process_response(request, response)

        except HTTPException as e:
            response = render_http_exception(request, e, e.get_description(environ))

        self.session_manager.save_session_to_cookie(request.session, request, response)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        try:
            return self.call_backend(environ, start_response)
        finally:
            if not DISABLE_GLOBALS:
                self.db.reset_after_request()


def paste_app_factory(global_config, **app_config):
    configs = app_config['config'].split()
    mediagoblin_config = None
    for config in configs:
        if os.path.exists(config) and os.access(config, os.R_OK):
            mediagoblin_config = config
            break

    if not mediagoblin_config:
        raise IOError('Usable mediagoblin config not found.')
    del app_config['config']
    mgoblin_app = MediaGoblinApp(mediagoblin_config)
    mgoblin_app.call_backend = SharedDataMiddleware(mgoblin_app.call_backend, exports=app_config)
    mgoblin_app = hook_transform('wrap_wsgi', mgoblin_app)
    return mgoblin_app