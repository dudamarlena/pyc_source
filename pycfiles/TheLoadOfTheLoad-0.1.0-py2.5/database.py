# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/src/lol/database.py
# Compiled at: 2008-07-27 08:14:09
from sqlite import SQLite
from mysql import MySQL
import logging
logger = logging.getLogger()

class Database(object):

    def __init__(self, databaseConfig):
        self.database = None
        self.databaseConfig = databaseConfig
        if self.databaseConfig.getDbms() == 'sqlite3':
            self.database = SQLite(self.databaseConfig)
        elif self.databaseConfig.getDbms() == 'mysql':
            self.database = MySQL(self.databaseConfig)
        return

    def connect(self):
        logger.debug('connect')
        return self.database.doConnect()

    def query(self, sql):
        logger.debug('query:' + sql)
        return self.database.doQuery(sql)

    def execute(self, sql):
        logger.debug('execute:' + sql)
        return self.database.doExecute(sql)

    def commit(self):
        logger.debug('commit')
        return self.database.doCommit()

    def rollback(self):
        logger.debug('rollback')
        return self.database.doRollback()

    def close(self):
        logger.debug('close')
        return self.database.doClose()

    def __del__(self):
        if self.database is not None:
            del self.database
        if self.databaseConfig is not None:
            del self.databaseConfig
        return