# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/torngas/global_settings.py
# Compiled at: 2016-02-16 00:41:00
import os
DEBUG = True
XHEADERS = True
TORNADO_CONF = {'static_path': 'static', 
   'xsrf_cookies': True, 
   'login_url': '/login', 
   'cookie_secret': 'bXZ/gDAbQA+zaTxdqJwxKa8OZTbuZE/ok3doaow9N4Q=', 
   'template_path': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')}
MIDDLEWARE_CLASSES = ('torngas.middleware.accesslog.AccessLogMiddleware', 'torngas.httpmodule.httpmodule.HttpModuleMiddleware')
INSTALLED_APPS = ()
COMMON_MODULES = ()
ROUTE_MODULES = {}
CACHES = {'default': {'BACKEND': 'torngas.cache.backends.localcache.LocMemCache', 
               'LOCATION': 'process_cache', 
               'OPTIONS': {'MAX_ENTRIES': 10000, 
                           'CULL_FREQUENCY': 3}}, 
   'default_memcache': {'BACKEND': 'torngas.cache.backends.memcached.MemcachedCache', 
                        'LOCATION': [
                                   '127.0.0.1:11211'], 
                        'TIMEOUT': 300}, 
   'dummy': {'BACKEND': 'torngas.cache.backends.dummy.DummyCache'}, 
   'default_redis': {'BACKEND': 'torngas.cache.backends.rediscache.RedisCache', 
                     'LOCATION': '127.0.0.1:6379', 
                     'OPTIONS': {'DB': 0, 
                                 'PARSER_CLASS': 'redis.connection.DefaultParser', 
                                 'POOL_KWARGS': {'socket_timeout': 2, 
                                                 'socket_connect_timeout': 2}, 
                                 'PING_INTERVAL': 120}}}
TRANSLATIONS = False
TRANSLATIONS_CONF = {'translations_dir': os.path.join(os.path.dirname(__file__), 'translations'), 
   'locale_default': 'zh_CN', 
   'use_accept_language': True}
WHITELIST = False
LOGGING_DIR = 'logs/'
LOGGING = (
 {'name': 'tornado', 
    'level': 'INFO', 
    'log_to_stderr': False, 
    'when': 'midnight', 
    'interval': 1, 
    'filename': 'tornado.log'},
 {'name': 'torngas.tracelog', 
    'level': 'ERROR', 
    'log_to_stderr': False, 
    'when': 'midnight', 
    'interval': 1, 
    'formatter': '%(message)s', 
    'filename': 'torngas_trace_log.log'},
 {'name': 'torngas.accesslog', 
    'level': 'INFO', 
    'log_to_stderr': True, 
    'when': 'midnight', 
    'interval': 1, 
    'formatter': '%(message)s', 
    'filename': 'torngas_access_log.log'},
 {'name': 'torngas.infolog', 
    'level': 'INFO', 
    'log_to_stderr': False, 
    'when': 'midnight', 
    'interval': 1, 
    'filename': 'torngas_info_log.log'})
IPV4_ONLY = True
SESSION = {'session_cache_alias': 'default', 
   'session_name': '__TORNADOID', 
   'cookie_domain': '', 
   'cookie_path': '/', 
   'expires': 0, 
   'ignore_change_ip': False, 
   'httponly': True, 
   'secure': False, 
   'secret_key': 'fLjUfxqXtfNoIldA0A0J', 
   'session_version': 'EtdHjDO1'}
TEMPLATE_CONFIG = {'template_engine': None, 
   'filesystem_checks': True, 
   'cache_directory': '../_tmpl_cache', 
   'collection_size': 50, 
   'cache_size': 0, 
   'format_exceptions': False, 
   'autoescape': False}
DATABASE_CONNECTION = {'default': {'connections': [
                             {'ROLE': 'master', 
                                'DRIVER': 'mysql+mysqldb', 
                                'UID': 'root', 
                                'PASSWD': '', 
                                'HOST': '', 
                                'PORT': 3306, 
                                'DATABASE': '', 
                                'QUERY': {'charset': 'utf8'}},
                             {'ROLE': 'slave', 
                                'DRIVER': 'mysql+mysqldb', 
                                'UID': 'root', 
                                'PASSWD': '', 
                                'HOST': '', 
                                'PORT': 3306, 
                                'DATABASE': '', 
                                'QUERY': {'charset': 'utf8'}}]}}
PING_DB = 300
PING_CONN_COUNT = 5
SQLALCHEMY_CONFIGURATION = {'sqlalchemy.connect_args': {'connect_timeout': 3}, 
   'sqlalchemy.echo': False, 
   'sqlalchemy.max_overflow': 10, 
   'sqlalchemy.echo_pool': False, 
   'sqlalchemy.pool_timeout': 5, 
   'sqlalchemy.encoding': 'utf-8', 
   'sqlalchemy.pool_size': 5, 
   'sqlalchemy.pool_recycle': 3600, 
   'sqlalchemy.poolclass': 'QueuePool'}