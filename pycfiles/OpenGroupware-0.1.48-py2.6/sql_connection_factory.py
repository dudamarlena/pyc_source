# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/foundation/factories/sql_connection_factory.py
# Compiled at: 2012-10-12 07:02:39
import logging
from coils.foundation.defaultsmanager import ServerDefaultsManager

class SQLConnectionFactory(object):
    _classes = None

    @staticmethod
    def Init():
        log = logging.getLogger('OIE')
        SQLConnectionFactory._classes = {}
        try:
            import informixdb
        except:
            log.info('Unable to load Informix support')
        else:
            log.info('Informix support loaded')
            from informix_connection import InformixConnection
            SQLConnectionFactory._classes['informix'] = InformixConnection

        try:
            import psycopg2
        except:
            log.info('Unable to load PostgreSQL support')
        else:
            log.info('PostgreSQL support loaded')
            from postgres_connection import PostgresConnection
            SQLConnectionFactory._classes['postgres'] = PostgresConnection

    @staticmethod
    def Connect(source):
        if SQLConnectionFactory._classes is None:
            SQLConnectionFactory.Init()
        log = logging.getLogger('OIE')
        sd = ServerDefaultsManager()
        config = sd.default_as_dict('OIESQLSources')
        if source in config:
            config = config.get(source)
            try:
                driver = SQLConnectionFactory._classes.get(config.get('driver'))
                connection = driver(config)
            except Exception, e:
                log.exception(e)
                log.error(('Unable to provide connection to source name {0}').format(source))
                return
            else:
                return connection
        else:
            log.error(('No source defined with name {0}').format(source))
            return
        return