# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mcfletch/pylive/table/pytable/mysql/mydriver.py
# Compiled at: 2004-02-19 05:41:31
"""MySQLdb database driver"""
from pytable import dbdriver, mysql
from pytable.mysql import tableactions
import MySQLdb
from MySQLdb.constants import FIELD_TYPE
from basicproperty import common

class MyDriver(dbdriver.DBDriver):
    """MySQLdb database driver
        """
    __module__ = __name__
    name = mysql.name
    baseModule = MySQLdb
    capabilities = dbdriver.DriverCapabilities(serial=0, inherits=0, queryUnicode=0)
    paramstyle = common.StringProperty('paramstyle', 'DBAPI 2.0 parameter-style value', defaultValue=MySQLdb.paramstyle)
    threadsafety = common.IntegerProperty('paramstyle', 'DBAPI 2.0 threadsafety value XXX should be an enumeration!', defaultValue=MySQLdb.threadsafety)
    apilevel = common.StringProperty('apilevel', 'DBAPI 2.0 apilevel value', defaultValue=MySQLdb.apilevel)
    systemDBName = common.StringProperty('systemDBName', "Default name for driver's system database (for listDatabases connections)", defaultValue='mysql')
    userDescription = 'MySQL database driver (via MySQLdb)\n\nProvides access to the open-source, cross-platform\nGNU GPL-licensed, server-based MySQL database.\n\nThe homepages of MySQL and MySQLdb are:\n\thttp://www.mysql.com/\n\thttp://sourceforge.net/projects/mysql-python\n'

    def establishConnection(self, fullSpecifier):
        """Connect using the fully specified specifier

                fullSpecifier -- a specifier with all arguments unified
                        and ready to be connected.  This specifier should
                        include everything required to do the actual
                        connection (including passwords or the like).

                All sub-classes must override this method!
                """
        set = {}
        for (name, arg) in [('database', 'db'), ('user', 'user'), ('password', 'passwd'), ('host', 'host')]:
            set[arg] = getattr(fullSpecifier, name)

        return MySQLdb.connect(**set)

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
      FIELD_TYPE.DECIMAL, 'decimal'), (FIELD_TYPE.CHAR, 'char'), (FIELD_TYPE.LONG, 'int4'), (FIELD_TYPE.FLOAT, 'float'), (FIELD_TYPE.DOUBLE, 'double'), (FIELD_TYPE.TIMESTAMP, 'timestamp'), (FIELD_TYPE.LONGLONG, 'int8'), (FIELD_TYPE.DATE, 'date'), (FIELD_TYPE.TIME, 'time'), (FIELD_TYPE.DATETIME, 'datetime'), (FIELD_TYPE.TINY_BLOB, 'blob'), (FIELD_TYPE.MEDIUM_BLOB, 'blob'), (FIELD_TYPE.LONG_BLOB, 'blob'), (FIELD_TYPE.BLOB, 'blob'), (FIELD_TYPE.VAR_STRING, 'varchar'), (FIELD_TYPE.STRING, 'text')]
    dataTypeNames = [
     (
      FIELD_TYPE.DECIMAL, 'DECIMAL'), (FIELD_TYPE.CHAR, 'CHAR'), (FIELD_TYPE.LONG, 'LONG'), (FIELD_TYPE.FLOAT, 'FLOAT'), (FIELD_TYPE.DOUBLE, 'DOUBLE'), (FIELD_TYPE.TIMESTAMP, 'TIMESTAMP'), (FIELD_TYPE.LONGLONG, 'LONGLONG'), (FIELD_TYPE.INT24, 'INT24'), (FIELD_TYPE.DATE, 'DATE'), (FIELD_TYPE.TIME, 'TIME'), (FIELD_TYPE.DATETIME, 'DATETIME'), (FIELD_TYPE.YEAR, 'YEAR'), (FIELD_TYPE.NEWDATE, 'NEWDATE'), (FIELD_TYPE.TINY_BLOB, 'TINY_BLOB'), (FIELD_TYPE.MEDIUM_BLOB, 'MEDIUM_BLOB'), (FIELD_TYPE.LONG_BLOB, 'LONG_BLOB'), (FIELD_TYPE.BLOB, 'BLOB'), (FIELD_TYPE.VAR_STRING, 'VARCHAR'), (FIELD_TYPE.STRING, 'STRING')]


MyDriver.copyErrorsFromModule(MySQLdb)