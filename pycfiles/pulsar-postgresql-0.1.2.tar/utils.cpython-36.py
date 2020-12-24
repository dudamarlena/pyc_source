# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/travis/build/quantmind/pulsar-odm/odm/utils.py
# Compiled at: 2017-11-24 06:00:10
# Size of source mod 2**32: 3943 bytes
import os
from inspect import isclass
import sqlalchemy as sa
from sqlalchemy import inspect
from sqlalchemy.exc import OperationalError, ProgrammingError

def get_columns(mixed):
    """
    Return a collection of all Column objects for given SQLAlchemy
    object.
    The type of the collection depends on the type of the object to return the
    columns from.
    ::
        get_columns(User)
        get_columns(User())
        get_columns(User.__table__)
        get_columns(User.__mapper__)
        get_columns(sa.orm.aliased(User))
        get_columns(sa.orm.alised(User.__table__))

    :param mixed:
        SA Table object, SA Mapper, SA declarative class, SA declarative class
        instance or an alias of any of these objects
    """
    if isinstance(mixed, sa.Table):
        return mixed.c
    else:
        if isinstance(mixed, sa.orm.util.AliasedClass):
            return sa.inspect(mixed).mapper.columns
        else:
            if isinstance(mixed, sa.sql.selectable.Alias):
                return mixed.c
            if isinstance(mixed, sa.orm.Mapper):
                return mixed.columns
            mixed = isclass(mixed) or mixed.__class__
        return sa.inspect(mixed).columns


def database_operation(engine, oper, *args):
    operation = _database_operation(engine, oper)
    return operation(engine, *args)


def _database_operation(engine, oper):
    dialect = engine.dialect
    method_name = 'database_%s' % oper
    if hasattr(dialect, method_name):
        return getattr(dialect, method_name)
    else:
        scripts = engine_scripts[method_name]
        if hasattr(scripts, dialect.name):
            return getattr(scripts, dialect.name)
        return scripts.default


class CreateDatabase:

    def sqlite(self, engine, database):
        pass

    def default(self, engine, database):
        conn = engine.connect()
        conn.execute('commit')
        conn.execute('create database %s' % database)
        conn.close()


class DropDatabase:

    def sqlite(self, engine, database):
        try:
            os.remove(database)
        except FileNotFoundError:
            pass

    def default(self, engine, database):
        conn = engine.connect()
        conn.execute('commit')
        conn.execute('drop database %s' % database)
        conn.close()


class AllDatabase:

    def sqlite(self, engine):
        database = engine.url.database
        if os.path.isfile(database):
            return [database]
        else:
            return []

    def default(self, engine):
        insp = inspect(engine)
        return insp.get_schema_names()


class ExistDatabase:
    """ExistDatabase"""

    def sqlite(self, engine):
        database = engine.url.database
        if database:
            return database == ':memory:' or os.path.exists(database)
        else:
            return True

    def postgresql(self, engine):
        database = engine.url.database
        text = "SELECT 1 FROM pg_database WHERE datname='%s'" % database
        return bool(engine.execute(text).scalar())

    def mysql(self, engine):
        database = engine.url.database
        text = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '%s'" % database
        return bool(engine.execute(text).scalar())

    def default(self, engine):
        try:
            engine.execute('SELECT 1')
            return True
        except (ProgrammingError, OperationalError):
            return False


engine_scripts = {'database_exists':ExistDatabase(), 
 'database_create':CreateDatabase(), 
 'database_drop':DropDatabase(), 
 'database_all':AllDatabase()}