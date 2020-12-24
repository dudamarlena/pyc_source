# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/tools/sqlmap/lib/utils/sqlalchemy.py
# Compiled at: 2013-12-09 06:41:17
"""
Copyright (c) 2006-2013 sqlmap developers (http://sqlmap.org/)
See the file 'doc/COPYING' for copying permission
"""
import imp, logging, os, sys, warnings
_sqlalchemy = None
try:
    f, pathname, desc = imp.find_module('sqlalchemy', sys.path[1:])
    _ = imp.load_module('sqlalchemy', f, pathname, desc)
    if hasattr(_, 'dialects'):
        _sqlalchemy = _
        warnings.simplefilter(action='ignore', category=_sqlalchemy.exc.SAWarning)
except ImportError:
    pass

try:
    import MySQLdb
    warnings.filterwarnings('error', category=MySQLdb.Warning)
except ImportError:
    pass

from lib.core.data import conf
from lib.core.data import logger
from lib.core.exception import SqlmapConnectionException
from lib.core.exception import SqlmapFilePathException
from plugins.generic.connector import Connector as GenericConnector

class SQLAlchemy(GenericConnector):

    def __init__(self, dialect=None):
        GenericConnector.__init__(self)
        self.dialect = dialect

    def connect(self):
        if _sqlalchemy:
            self.initConnection()
            try:
                if not self.port and self.db:
                    if not os.path.exists(self.db):
                        raise SqlmapFilePathException, "the provided database file '%s' does not exist" % self.db
                    _ = conf.direct.split('//', 1)
                    conf.direct = '%s////%s' % (_[0], os.path.abspath(self.db))
                if self.dialect:
                    conf.direct = conf.direct.replace(conf.dbms, self.dialect)
                engine = _sqlalchemy.create_engine(conf.direct, connect_args={'check_same_thread': False} if self.dialect == 'sqlite' else {})
                self.connector = engine.connect()
            except SqlmapFilePathException:
                raise
            except Exception as msg:
                raise SqlmapConnectionException("SQLAlchemy connection issue ('%s')" % msg[0])

            self.printConnected()

    def fetchall(self):
        try:
            retVal = []
            for row in self.cursor.fetchall():
                retVal.append(tuple(row))

            return retVal
        except _sqlalchemy.exc.ProgrammingError as msg:
            logger.log(logging.WARN if conf.dbmsHandler else logging.DEBUG, '(remote) %s' % msg.message if hasattr(msg, 'message') else msg)
            return

        return

    def execute(self, query):
        try:
            self.cursor = self.connector.execute(query)
        except (_sqlalchemy.exc.OperationalError, _sqlalchemy.exc.ProgrammingError) as msg:
            logger.log(logging.WARN if conf.dbmsHandler else logging.DEBUG, '(remote) %s' % msg.message if hasattr(msg, 'message') else msg)
        except _sqlalchemy.exc.InternalError as msg:
            raise SqlmapConnectionException(msg[1])

    def select(self, query):
        self.execute(query)
        return self.fetchall()