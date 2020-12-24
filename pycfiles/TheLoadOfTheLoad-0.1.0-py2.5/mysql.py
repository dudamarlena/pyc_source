# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/src/lol/mysql.py
# Compiled at: 2008-07-27 08:08:22
import MySQLdb, logging
logger = logging.getLogger()

class MySQL:

    def __init__(self, databaseConfig):
        self.connection = None
        self.databaseConfig = databaseConfig
        logger.debug('MySQL connecter created')
        return

    def doConnect(self):
        self.connection = MySQLdb.connect(db=self.databaseConfig.getDatabase(), host=self.databaseConfig.getHost(), port=self.databaseConfig.getPort(), user=self.databaseConfig.getUser(), passwd=self.databaseConfig.getPassword())

    def doQuery(self, sql):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        return cursor

    def doExecute(self, sql):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        return cursor

    def doCommit(self):
        return self.connection.commit()

    def doRollback(self):
        return self.connection.rollback()

    def doClose(self):
        return self.connection.close()

    def __del__(self):
        if self.connection is not None:
            del self.connection
        if self.databaseConfig is not None:
            del self.databaseConfig
        return