# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\migration\sqlobject_migration.py
# Compiled at: 2006-11-01 19:21:05
import sys, sqlobject
from package import get_migrations_module
from base_classes import Migration, PackageVersion
from MySQLdb import OperationalError, ProgrammingError

class SOPackageVersion(sqlobject.SQLObject, PackageVersion):
    """Object used to keep track of the database version"""
    __module__ = __name__

    class sqlmeta:
        __module__ = __name__
        table = 'tg_migrate'

    package = sqlobject.StringCol(length=255, alternateID=True, alternateMethodName='get_by_package')
    version = sqlobject.IntCol()

    def get_version(self):
        return self.version

    def set_version(self, version):
        self.version = version
        self._connection.commit()


def get_pv_class(package):
    hub = get_migrations_module(package).migration_hub
    SOPackageVersion._connection = hub
    try:
        SOPackageVersion.select(0).count()
    except ProgrammingError, e:
        if e[0] == 1146:
            SOPackageVersion.createTable()
        else:
            raise

    hub.begin()
    try:
        package_version = SOPackageVersion.get_by_package(package)
    except sqlobject.SQLObjectNotFound:
        package_version = SOPackageVersion(package=package, version=0)

    hub.commit()
    return package_version


class SOMigration(Migration):
    __module__ = __name__

    def query(self, query):
        conn = self.get_connection()
        return conn.query(query)

    def create_table(self, cls):
        conn_ = cls._connection
        cls._connection = self.get_connection()
        cls.createTable()
        cls._connection = conn_

    def drop_table(self, cls):
        conn_ = cls._connection
        cls._connection = self.get_connection()
        cls.dropTable()
        cls._connection = conn_

    def add_column(self, cls, column_name, column):
        column.name = column_name
        col = column.withClass(cls.sqlmeta.soClass)
        original_connection = cls._connection
        cls.setConnection(self.get_connection())
        cls._connection.addColumn(cls.sqlmeta.table, col)
        cls.setConnection(original_connection)

    def del_column(self, cls, column_name, dbName=None):
        col = cls.sqlmeta.columns.get(column_name, None)
        used_dummy = False
        if col is None:
            cls.sqlmeta.addColumn(sqlobject.IntCol(column_name, dbName=dbName))
            col = cls.sqlmeta.columns.get(column_name)
            used_dummy = True
        original_connection = cls._connection
        cls.setConnection(self.get_connection())
        cls._connection.delColumn(cls.sqlmeta.table, col)
        cls.setConnection(original_connection)
        if used_dummy:
            cls.sqlmeta.delColumn(column_name)
        return

    def get_connection(self):
        mod = sys.modules[self.__module__]
        if hasattr(mod, 'hub'):
            connection = mod.hub.getConnection()
        else:
            raise "Couldn't find a connection hub in the migrations module"
        return connection