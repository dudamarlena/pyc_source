# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/parser_engine/config.py
# Compiled at: 2019-03-22 05:22:12
# Size of source mod 2**32: 1985 bytes
import pkg_resources, logging
from peewee import MySQLDatabase
from .utils import *
CONFIG_DATA = None
mysqldb = MySQLDatabase(None)

def load_config_data():
    settings = load_scrapy_settings()
    db_config = settings.getdict('MYSQL')
    if db_config:
        mysqldb.init((db_config.get('DATABASE')), host=(db_config.get('HOST', '127.0.0.1')), user=(db_config.get('USER', 'root')),
          passwd=(db_config.get('PASSWORD')),
          port=(db_config.get('PORT', 3306)))
    else:
        if settings.get('MYSQL_USER'):
            mysqldb.init((settings.get('MYSQL_DATABASE')), host=(settings.get('MYSQL_HOST', '127.0.0.1')), user=(settings.get('MYSQL_USER', 'root')),
              passwd=(settings.get('MYSQL_PASSWORD')),
              port=(settings.get('MYSQL_PORT', 3306)))
        db_table = settings.get('PARSER_ENGINE_CONFIG_TABLE')
        if db_table:
            pass
        else:
            config_path = settings.get('PARSER_ENGINE_CONFIG_FILE', 'parser_engine.json')
            if not os.path.isabs(config_path):
                config_path1 = closest_parser_engine_json(config_path)
                if not config_path1:
                    resource_package = __name__
                    resource_path = '/'.join(('templates', config_path))
                    return json.load(pkg_resources.resource_stream(resource_package, resource_path))
                config_path = config_path1
            with open(config_path, mode='rb') as (f):
                return json.loads(f.read())


def init_logger():
    global CONFIG_DATA
    logfile = CONFIG_DATA.get('PARSER_ENGINE_LOG_FILE')
    if logfile:
        logging.basicConfig(filename=logfile, filemode='w', format='[parser-engine] %(ascii)s-%(levelname)s %(message)s',
          level=(logging.DEBUG))


def init_config():
    global CONFIG_DATA
    CONFIG_DATA = load_config_data()
    init_logger()


def get_config_data():
    if not CONFIG_DATA:
        init_config()
    return CONFIG_DATA