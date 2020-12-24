# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xbus/monitor/core.py
# Compiled at: 2016-06-27 04:20:00
# Size of source mod 2**32: 7124 bytes
import os
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid_redis_sessions import session_factory_from_settings
from sqlalchemy import engine_from_config
from xbus.monitor.i18n import init_i18n
from xbus.monitor.models.monitor import DBSession
from xbus.monitor.resources.root import RootFactory
from xbus.monitor.views import saml2_login
from xbus.monitor.views import http_login
from xbus.monitor.utils.config import tobool
from xbus.monitor.auth import get_user_principals
API_PREFIX = '/api/'
COLLECTION_FACTORY_LOC = 'xbus.monitor.resources.{model}.collections.CollectionFactory_{collection}'
RECORD_FACTORY_LOC = 'xbus.monitor.resources.{model}.records.RecordFactory_{collection}'

def _add_api_routes(config, model, collection):
    """Register routes for a collection to be exposed through the API. The
    relevant views then have to be implemented by referencing these routes.

    :param model: Name of the database model where the collection is described.
    :type model: String.

    :param collection: Name of the collection.
    :type collection: String.
    """
    settings = {'api_prefix': API_PREFIX, 
     'collection': collection, 
     'model': model}
    config.add_route('{collection}_list'.format(**settings), '{api_prefix}{collection}'.format(**settings), request_method='GET', factory=COLLECTION_FACTORY_LOC.format(**settings))
    config.add_route('{collection}_create'.format(**settings), '{api_prefix}{collection}'.format(**settings), request_method='POST', factory=COLLECTION_FACTORY_LOC.format(**settings))
    config.add_route(collection, '{api_prefix}{collection}/{{id}}'.format(**settings), factory=RECORD_FACTORY_LOC.format(**settings))
    config.add_route('{collection}_rel_list'.format(**settings), '{api_prefix}{collection}/{{id}}/{{rel}}'.format(**settings), request_method='GET', factory=RECORD_FACTORY_LOC.format(**settings))
    config.add_route('{collection}_rel_create'.format(**settings), '{api_prefix}{collection}/{{id}}/{{rel}}'.format(**settings), request_method='POST', factory=RECORD_FACTORY_LOC.format(**settings))
    config.add_route('{collection}_rel'.format(**settings), '{api_prefix}{collection}/{{id}}/{{rel}}/{{rid}}'.format(**settings), factory=RECORD_FACTORY_LOC.format(**settings))


def main(global_config, **settings):
    """Initiate a Pyramid WSGI application.
    """
    db_url = settings.get('fig.sqlalchemy.url')
    if db_url:
        pg_socket_var = os.getenv('XBUS_POSTGRESQL_1_PORT')
        if pg_socket_var is not None:
            pg_socket = pg_socket_var.split('://', 1)[(-1)]
        else:
            pg_socket = settings.get('fig.sqlalchemy.default.socket')
        settings['sqlalchemy.url'] = db_url.format(socket=pg_socket)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    saml2_enabled = tobool(settings['saml2.enabled'])
    secure_cookie = tobool(settings['cookie.secure'])
    config = Configurator(session_factory=session_factory_from_settings(settings), settings=settings, root_factory=RootFactory, authentication_policy=AuthTktAuthenticationPolicy(settings['authentication.secret'], callback=get_user_principals, secure=secure_cookie), authorization_policy=ACLAuthorizationPolicy())
    if not saml2_enabled:
        config.add_settings(auth_kind='http')
        http_login.setup(config)
    else:
        config.add_settings(auth_kind='saml2')
        saml2_login.setup(config)
    config.include('pyramid_chameleon')
    config.set_default_permission('view')
    init_i18n(config)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('xml_config_ui', '/xml_config')
    config.add_route('event_type_graph', API_PREFIX + 'event_type/{id}/graph', factory=RECORD_FACTORY_LOC.format(model='monitor', collection='event_type'))
    config.add_route('retry_event', API_PREFIX + 'event/{id}/retry', factory=RECORD_FACTORY_LOC.format(model='monitor', collection='event'))
    config.add_route('login_info', 'login_info')
    _add_api_routes(config, 'data_clearing', 'cl_event_type')
    _add_api_routes(config, 'data_clearing', 'cl_item')
    _add_api_routes(config, 'data_clearing', 'cl_item_column')
    _add_api_routes(config, 'data_clearing', 'cl_item_join')
    _add_api_routes(config, 'data_clearing', 'cl_item_type')
    _add_api_routes(config, 'monitor', 'emission_profile')
    _add_api_routes(config, 'monitor', 'emitter')
    _add_api_routes(config, 'monitor', 'emitter_profile')
    _add_api_routes(config, 'monitor', 'envelope')
    _add_api_routes(config, 'monitor', 'event')
    _add_api_routes(config, 'monitor', 'event_error')
    _add_api_routes(config, 'monitor', 'event_error_tracking')
    _add_api_routes(config, 'monitor', 'event_node')
    _add_api_routes(config, 'monitor', 'event_tracking')
    _add_api_routes(config, 'monitor', 'event_type')
    _add_api_routes(config, 'monitor', 'input_descriptor')
    _add_api_routes(config, 'monitor', 'role')
    _add_api_routes(config, 'monitor', 'service')
    _add_api_routes(config, 'monitor', 'user')
    config.add_route('consumer_list', API_PREFIX + 'consumer')
    config.add_route('replay_envelope', API_PREFIX + 'replay_envelope')
    config.add_route('upload', API_PREFIX + 'upload')
    config.add_route('xml_config', API_PREFIX + 'xml_config')
    config.add_route('catchall_static', '/*subpath')
    config.add_view('xbus.monitor.statichome.static_view', route_name='catchall_static')
    config.scan()
    return config.make_wsgi_app()