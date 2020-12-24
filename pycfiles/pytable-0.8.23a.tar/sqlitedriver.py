# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mcfletch/pylive/table/pytable/pysqlite/sqlitedriver.py
# Compiled at: 2004-11-16 07:05:31
"""SQLite database driver"""
from pytable import dbdriver, pysqlite
from pytable.pysqlite import tableactions
from basicproperty import common
import sqlite

class SQLiteDriver(dbdriver.DBDriver):
    """SQLite Database driver using PySQLite
        """
    __module__ = __name__
    name = pysqlite.name
    baseModule = sqlite
    capabilities = dbdriver.DriverCapabilities(serial=0, inherits=0, queryUnicode=0, queryPyformat=0)
    paramstyle = common.StringProperty('paramstyle', 'DBAPI 2.0 parameter-style value', defaultValue=sqlite.paramstyle)
    threadsafety = common.IntegerProperty('paramstyle', 'DBAPI 2.0 threadsafety value XXX should be an enumeration!', defaultValue=sqlite.threadsafety)
    apilevel = common.StringProperty('apilevel', 'DBAPI 2.0 apilevel value', defaultValue=sqlite.apilevel)
    userDescription = 'SQLite database driver (via PySQLite)\n\nProvides access to the open-source, cross-platform\nCNRI-Python-licensed embedded database engine SQLite\n\nThe homepages of SQLite and PySQLite are:\n\thttp://www.sqlite.org/\n\thttp://pysqlite.sourceforge.net/\n'

    def establishConnection(self, fullSpecifier):
        """Connect using the fully specified specifier

                fullSpecifier -- a specifier with all arguments unified
                        and ready to be connected.  This specifier should
                        include everything required to do the actual
                        connection (including passwords or the like).

                All sub-classes must override this method!
                """
        return sqlite.connect(fullSpecifier.database)

    def __getattr__(self, key):
        """Search for an action-script of the given name in actionScripts"""
        if key != 'queries':
            script = self.queries.get(key)
            if script:
                return script
        raise AttributeError('%r object has no attribute %r' % (self, key))

    queries = {'listDatabases': tableactions.ListDatabases(), 'listTables': tableactions.ListTables(), 'listIndices': tableactions.ListIndices(), 'tableStructure': tableactions.TableStructure()}
    localTypeRegistry = [
     (
      sqlite.NUMBER, 'float'), (sqlite.STRING, 'str'), (sqlite.DATETIME, 'datetime'), (sqlite.BINARY, 'blob')]
    dataTypeNames = [
     (
      sqlite.NUMBER, 'INTEGER'), (sqlite.STRING, 'VARCHAR'), (sqlite.DATETIME, 'DATETIME'), (sqlite.BINARY, 'BLOB')]


SQLiteDriver.copyErrorsFromModule(sqlite)