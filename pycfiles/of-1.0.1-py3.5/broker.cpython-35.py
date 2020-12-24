# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/of/broker/broker.py
# Compiled at: 2016-12-25 14:28:13
# Size of source mod 2**32: 17143 bytes
"""
The broker is the heart of the Optimal Framework. It is the messaging and API hub of the system.
It can also present a UI for administration and a custom UI if needed.
"""
import os, sys, time
from logging import CRITICAL
from multiprocessing import Process
import cherrypy, json
from bson.objectid import ObjectId
from pymongo.mongo_client import MongoClient
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
__author__ = 'Nicklas Borjesson'
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_dir, '../../'))
import of.common.logging, logging
from of.broker.lib.access import DatabaseAccess
from of.broker.lib.auth_backend import MongoDBAuthBackend
from of.common.cumulative_dict import CumulativeDict
from of.common.logging import write_to_log, SEV_FATAL, EC_SERVICE, SEV_DEBUG, EC_UNCATEGORIZED, SEV_ERROR, SEV_INFO, EC_INVALID, make_sparse_log_message, make_textual_log_message, make_event
from of.common.security.authentication import init_authentication
from of.common.settings import JSONXPath
from of.schemas.schema import SchemaTools
from of.broker import run_broker
from of.common.internal import register_signals, resolve_config_path
from of.common.messaging.factory import store_process_system_document, log_process_state_message
from of.broker.lib.messaging.websocket import BrokerWebSocket
from of.schemas.constants import zero_object_id
from of.schemas.validation import of_uri_handler
from of.broker.cherrypy_api.broker import CherryPyBroker
from of.common.plugins import CherryPyPlugins
from of.broker.lib.messaging.handler import BrokerWebSocketHandler
from of.common.queue.monitor import Monitor
import of.common.messaging.websocket
if os.name == 'nt':
    from of.common.logging import write_to_event_log
aux_runner = None
address = ''
schema_tools = None
database_access = None
process_id = None
web_root = None
web_socket_plugin = None
web_config = None
plugins = None
namespaces = None
application_name = None
_settings = None
log_to_database_severity = None
x_logger = None
if os.name != 'nt':
    x_logger = logging.Logger('default')
    fh = logging.FileHandler('/var/log/of.log')
    x_logger.addHandler(fh)

def write_srvc_dbg(_data):
    global process_id
    write_to_log(_data, _category=EC_SERVICE, _severity=SEV_DEBUG, _process_id=process_id)


def log_locally(_data, _category, _severity, _process_id_param, _user_id, _occurred_when, _address_param, _node_id, _uid, _pid):
    global address
    if _process_id_param is None:
        _process_id_param = process_id
    if _address_param is None:
        _address_param = address
    if os.name == 'nt':
        write_to_event_log(make_textual_log_message(_data, _category, _severity, _process_id_param, _user_id, _occurred_when, _address_param, _node_id, _uid, _pid), 'Application', _category, _severity)
    else:
        _message = make_sparse_log_message(_data, _category, _severity, _process_id_param, _user_id, _occurred_when, _address_param, _node_id, _uid, _pid)
    try:
        x_logger.log(msg=_message, level=CRITICAL)
    except Exception as e:
        print(make_sparse_log_message('FAILED TO WRITE TO FILE, PRINTING ERROR: ' + str(e) + _message, EC_SERVICE, SEV_ERROR, _process_id_param, _user_id, _occurred_when, _address_param, _node_id, _uid, _pid))


def log_to_database(_data, _category, _severity, _process_id_param, _user_id, _occurred_when, _address_param, _node_id, _uid, _pid):
    global database_access
    global log_to_database_severity
    if _process_id_param is None:
        _process_id_param = process_id
    if _address_param is None:
        _address_param = address
    if _severity < log_to_database_severity:
        log_locally(_data, _category, _severity, _process_id_param, _user_id, _occurred_when, _address_param, _node_id, _uid, _pid)
    else:
        try:
            database_access.logging.write_log(make_event(_data, _category, _severity, _process_id_param, _user_id, _occurred_when, _address_param, _node_id, _uid, _pid))
        except Exception as e:
            log_locally('Failed to write to database, error: ' + str(e), EC_UNCATEGORIZED, SEV_ERROR, _process_id_param, _user_id, _occurred_when, _address_param, _node_id, _uid, _pid)

        log_locally(_data, _category, _severity, process_id, _user_id, _occurred_when, _address_param, _node_id, _uid, _pid)


def error_message_default(status, message, traceback, version):
    _json_message = {'status': status, 
     'version': version, 
     'message': [message], 
     'traceback': [_x.strip() for _x in traceback.split('\n')]}
    cherrypy.serving.response.headers['Content-Type'] = 'application/json'
    return json.dumps(_json_message, indent=4, sort_keys=True)


def start_broker(_cfg_filename=None):
    """
    Starts the broker; Loads settings, connects to database, registers process and starts the web server.
    """
    global address
    global database_access
    global log_to_database_severity
    global namespaces
    global plugins
    global process_id
    global schema_tools
    global settings
    global web_config
    global web_root
    global web_socket_plugin
    process_id = str(ObjectId())
    of.common.logging.callback = log_locally
    write_srvc_dbg('=====Starting broker=============================')
    try:
        if _cfg_filename is None:
            _cfg_filename = resolve_config_path()
        settings = JSONXPath(_cfg_filename)
    except Exception as e:
        if os.name == 'nt':
            write_to_log(_data='Error loading settings from ' + _cfg_filename, _category=EC_SERVICE, _severity=SEV_FATAL)
        raise Exception('Error loading settings:' + str(e))

    if os.name != 'nt':
        x_logger = logging.FileHandler('/var/log/of.log')
    of.common.logging.severity = of.common.logging.severity_identifiers.index(settings.get('broker/logging/severityLevel', _default='warning'))
    log_to_database_severity = of.common.logging.severity_identifiers.index(settings.get('broker/logging/databaseLevel', _default='warning'))
    write_srvc_dbg('Loaded settings from ' + _cfg_filename)
    address = settings.get('broker/address', _default=None)
    if not address or address == '':
        write_to_log(_data='Broker cannot start, missing [broker] address setting in configuration file.', _category=EC_SERVICE, _severity=SEV_FATAL)
        raise Exception('Broker cannot start, missing address.')
    schema_tools = SchemaTools(_json_schema_folders=[os.path.join(script_dir, '../schemas/namespaces/')], _uri_handlers={'ref': of_uri_handler})
    namespaces = CumulativeDict(_default={'schemas': []})
    write_srvc_dbg('Load plugin data')
    _plugins_folder = settings.get_path('broker/pluginsFolder', _default='plugins')
    plugins = CherryPyPlugins(_plugins_folder=_plugins_folder, _schema_tools=schema_tools, _namespaces=namespaces, _process_id=process_id, _no_package_name_override=settings.get('broker/packageNameOverride'))
    plugins.call_hook('init_broker_scope', _broker_scope=globals(), _settings=settings)
    write_srvc_dbg('===Register signal handlers===')
    register_signals(stop_broker)
    plugins.call_hook('before_db_connect', _broker_scope=globals())
    _host = settings.get('broker/database/host', _default='127.0.0.1')
    _user = settings.get('broker/database/username', _default=None)
    _password = settings.get('broker/database/password', _default=None)
    if _user:
        write_srvc_dbg('===Connecting to remote MongoDB backend ' + _host + '===')
        _client = MongoClient('mongodb://' + _user + ':' + _password + '@' + _host)
    else:
        write_srvc_dbg('===Connecting to local MongoDB backend===')
        _client = MongoClient()
    _database_name = settings.get('broker/database/databaseName', _default='optimalframework')
    write_srvc_dbg('Using database name :' + _database_name)
    _database = _client[_database_name]
    database_access = DatabaseAccess(_database=_database, _schema_tools=schema_tools)
    of.common.logging.callback = log_to_database
    database_access.save(store_process_system_document(_process_id=process_id, _name='Broker instance(' + address + ')'), _user=None, _allow_save_id=True)
    plugins.call_hook('after_db_connect', _broker_scope=globals())
    if hasattr(cherrypy.engine, 'subscribe'):
        pass
    else:
        write_to_log(_data='This application requires CherryPy >= 3.1 or higher.', _category=EC_SERVICE, _severity=SEV_FATAL)
        raise Exception('Broker init: This application requires CherryPy >= 3.1 or higher.')

    def ssl_path():
        return os.path.dirname(_cfg_filename)

    cherrypy.config.update({'tools.encode.on': True, 
     'tools.encode.encoding': 'utf-8', 
     'tools.decode.on': True, 
     'tools.trailing_slash.on': True, 
     'tools.staticdir.root': os.path.abspath(os.path.dirname(__file__)), 
     'server.ssl_module': 'builtin', 
     'engine.autoreload.on': False, 
     'server.socket_host': '0.0.0.0', 
     'server.ssl_certificate': os.path.join(ssl_path(), 'optimalframework_test_cert.pem'), 
     'server.ssl_private_key': os.path.join(ssl_path(), 'optimalframework_test_privkey.pem'), 
     'error_page.default': error_message_default})
    write_srvc_dbg('Starting CherryPy, ssl at ' + os.path.join(ssl_path(), 'optimalframework_test_privkey.pem'))
    web_config = {'/': {'tools.staticdir.on': True, 
           'tools.staticdir.dir': 'ui', 
           'tools.trailing_slash.on': True, 
           'tools.staticdir.index': 'index.html'}, 
     
     '/socket': {'tools.websocket.on': True, 
                 'tools.websocket.handler_cls': BrokerWebSocket}}
    cherrypy._global_conf_alias.update(web_config)
    web_socket_plugin = WebSocketPlugin(cherrypy.engine)
    web_socket_plugin.subscribe()
    cherrypy.tools.websocket = WebSocketTool()
    cherrypy.engine.signals.bus.signal_handler.handlers = {'SIGUSR1': cherrypy.engine.signals.bus.graceful}
    init_authentication(MongoDBAuthBackend(database_access))
    web_root = CherryPyBroker(_process_id=process_id, _address=address, _database_access=database_access)
    of.common.messaging.websocket.monitor = Monitor(_handler=BrokerWebSocketHandler(process_id, _peers=web_root.peers, _database_access=database_access, _schema_tools=database_access.schema_tools, _address=address))
    web_root.plugins = plugins
    plugins.call_hook('init_web', _broker_scope=globals())
    _web_config_debug = 'Broker configured. Starting web server. Web config:\n'
    for _curr_key, _curr_config in web_config.items():
        if 'tools.staticdir.dir' in _curr_config:
            _web_config_debug += 'Path: ' + _curr_key + ' directory: ' + _curr_config['tools.staticdir.dir']
        else:
            _web_config_debug += 'Path: ' + _curr_key + ' - no static dir'

    plugins.call_hook('post_web_init', _broker_scope=globals())
    write_to_log(_web_config_debug, _category=EC_SERVICE, _severity=SEV_INFO)
    plugins.call_hook('pre_webserver_start', web_config=web_config, globals=globals())
    cherrypy.log.screen = False
    cherrypy.quickstart(web_root, '/', web_config)


def stop_broker(_reason, _restart=None):
    if _restart:
        write_to_log('BROKER WAS TOLD TO RESTART, shutting down orderly', _category=EC_SERVICE, _severity=SEV_INFO, _process_id=process_id)
    else:
        write_to_log('BROKER WAS TERMINATED, shutting down orderly', _category=EC_SERVICE, _severity=SEV_INFO, _process_id=process_id)
    write_srvc_dbg('Reason:' + str(_reason))
    _exit_status = 0
    write_srvc_dbg('Stop the monitor')
    try:
        of.common.messaging.websocket.monitor.stop()
    except Exception as e:
        write_to_log('Exception trying to stop monitor:', _category=EC_INVALID)
        _exit_status += 1

    time.sleep(1)
    try:
        database_access.save(log_process_state_message(_changed_by=zero_object_id, _state='killed', _process_id=process_id, _reason='Broker was terminated, reason: "' + _reason + '", shutting down gracefully'), _user=None)
    except Exception as e:
        write_to_log('Exception trying to write log item to Mongo DB backend:' + str(e), _category=EC_SERVICE, _severity=SEV_ERROR)
        _exit_status += 1

    try:
        write_srvc_dbg('Unsubscribing the web socket plugin...')
        web_socket_plugin.unsubscribe()
        write_srvc_dbg('Stopping the web socket plugin...')
        web_socket_plugin.stop()
        write_srvc_dbg('Shutting down web server...')
        cherrypy.engine.stop()
        write_srvc_dbg('Web server shut down...')
    except Exception as e:
        write_to_log('Exception trying to shut down web server:' + str(e), _category=EC_SERVICE, _severity=SEV_ERROR)
        _exit_status += 4

    if _restart:
        write_srvc_dbg('Broker was told to restart, so it now starts a new broker instance...')
        _broker_process = Process(target=run_broker, name='optimalframework_broker', daemon=False)
        _broker_process.start()
        _broker_process.join()
    write_srvc_dbg('Broker exiting with exit status ' + str(_exit_status))
    if os.name != 'nt':
        os._exit(_exit_status)
    else:
        cherrypy.engine.exit()
        return _exit_status


if __name__ == '__main__':
    start_broker()