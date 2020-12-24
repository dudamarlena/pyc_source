# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/credstuffer/dbhandler.py
# Compiled at: 2020-04-05 08:14:43
# Size of source mod 2**32: 2196 bytes
import logging
from credstuffer.db import DBConnector, DBFetcher, DBInserter
from credstuffer.exceptions import DBConnectorError

class DBHandler:
    __doc__ = ' Base class DBHandler to provide database actions to subclasses\n\n    USAGE:\n            dbhandler = DBHandler()\n\n    '

    def __init__(self, **dbparams):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('create class DBHandler')
        if ('host' and 'port' and 'username' and 'password' and 'dbname') in dbparams.keys():
            self.db_host = dbparams['host']
            self.db_port = dbparams['port']
            self.db_username = dbparams['username']
            self.db_password = dbparams['password']
            self.db_name = dbparams['dbname']
            if DBConnector.connect_psycopg(host=(self.db_host), port=(self.db_port), username=(self.db_username), password=(self.db_password),
              dbname=(self.db_name),
              minConn=1,
              maxConn=39):
                self.dbfetcher = DBFetcher()
                self.dbinserter = DBInserter()
                self.dbstructure = '0123456789abcdefghijklmnopqrstuvwxyz'
                self.schema_list_default = list(self.dbstructure)
                self.schema_list_default.append('symbols')
                self.table_list_default = self.schema_list_default
                self.schema_list = None
                self.table_list = None
            else:
                self.logger.error('DBHandler could not connect to the databases')
                raise DBConnectorError('DBHandler could not connect to the databases')
        else:
            self.logger.error('DBHandler could not connect to the databases')
            raise DBConnectorError('DBHandler could not connect to the databases')

    def fetch_data(self, schema, table):
        """ fetch data from database table 'schema'.'table'

        :param schema: schema name
        :param table: table name

        :return: data from database table
        """
        sql = 'select * from "{}"."{}"'.format(schema, table)
        return self.dbfetcher.all(sql=sql)