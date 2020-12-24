# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydo/drivers/mssqlconn.py
# Compiled at: 2007-02-15 13:23:35
"""
PyDO driver for mssql, using the ADO adapter.
"""
from pydo.dbi import DBIBase, ConnectionPool
from pydo.field import Field, Sequence
from pydo.exceptions import PyDOError
from pydo.dbtypes import DATE, TIMESTAMP, BINARY, INTERVAL, date_formats, timestamp_formats
from pydo.log import debug
from pydo.operators import BindingConverter
import time, datetime, mx.DateTime, adodbapi

def connection_string(server, database):
    return 'Provider=SQLOLEDB;Data Source=%s;Initial Catalog=%s;Integrated Security=SSPI;' % (server, database)


def convert_DATE(dt):
    val = dt.value
    if isinstance(val, mx.DateTime.DateTimeType):
        return val
    elif isinstance(val, datetime.date):
        return mx.DateTime.DateFrom(dt.year, dt.month, dt.day)
    elif isinstance(val, (int, float, long)):
        d = datetime.date.fromtimestamp(val)
        return mx.DateTime.DateFrom(d.year, d.month, d.day)
    elif isinstance(val, (tuple, list)):
        return mx.DateTime.DateFrom(*val[:3])
    elif isinstance(val, basestring):
        for f in date_formats:
            try:
                t = time.strptime(val, f)[:3]
            except ValueError:
                continue
            else:
                return mx.DateTime.DateFrom(*t)
        else:
            raise ValueError, "cannot parse date format: '%s'" % val
    raise ValueError, val


def convert_TIMESTAMP(ts):
    val = ts.value
    if isinstance(val, mx.DateTime.DateTimeType):
        return val
    elif isinstance(val, datetime.datetime):
        return mx.DateTime.DateTimeFromTicks(time.mktime(ts.timetuple()))
    elif isinstance(val, (int, float, long)):
        return mx.DateTime.DateTimeFromTicks(val)
    elif isinstance(val, (tuple, list)) and len(val) == 9:
        return mx.DateTime.DateTimeFromTicks(time.mktime(val))
    elif isinstance(val, basestring):
        for f in timestamp_formats:
            try:
                return mx.DateTime.strptime(val, f)
            except ValueError:
                continue

        else:
            raise ValueError, "cannot parse timestamp format: '%s'" % val
    raise ValueError, val


_converters = {datetime.datetime: lambda x: mx.DateTime.DateTimeFromTicks(time.mktime(x.timetuple())), 
   datetime.date: lambda x: mx.DateTime.DateFromTicks(time.mktime(x.timetuple())), 
   DATE: convert_DATE, TIMESTAMP: convert_TIMESTAMP, INTERVAL: lambda x: x.value}

class MssqlConverter(BindingConverter):
    __module__ = __name__
    converters = _converters


class MssqlDBI(DBIBase):
    __module__ = __name__
    auto_increment = True

    def __init__(self, connectArgs, pool=None, verbose=False, initFunc=None):
        if pool and not hasattr(pool, 'connect'):
            pool = ConnectionPool()
        super(MssqlDBI, self).__init__(connectArgs, adodbapi.connect, adodbapi, pool, verbose, initFunc)
        autocommit = False

    def getConverter(self):
        return MssqlConverter(self.paramstyle)

    def getAutoIncrement(self, name):
        q = self.conn.db.cursor()
        q.execute('SELECT @@IDENTITY')
        return q.fetchone()[0]

    def listTables(self, schema=None):
        """list the tables in the database schema.
      """
        if schema:
            sql = "\n          SELECT\n            TABLE_NAME\n          FROM\n            INFORMATION_SCHEMA.TABLES\n          WHERE\n            TABLE_TYPE='BASE_TABLE' AND\n            SCHEMA='%s'\n          ORDER BY\n            TABLE_NAME\n        " % schema
        else:
            sql = "\n          SELECT\n            TABLE_NAME\n          FROM\n            INFORMATION_SCHEMA.TABLES\n          WHERE\n            TABLE_TYPE='BASE_TABLE'\n          ORDER BY\n            TABLE_NAME\n        "
        c = self.conn.cursor()
        c.execute(sql)
        res = c.fetchall()
        if res:
            return sorted((x[0] for x in res))
        return ()

    def describeTable(self, table, schema=None):
        schema = schema or 'dbo'
        fields = {}
        unique = set()
        nullable = []
        c = self.conn.cursor()
        if self.verbose:

            def execute(sql):
                debug('SQL: %s', (sql,))
                c.execute(sql)

        else:
            execute = c.execute
        sql = "\n        select \n          column_name = col.COLUMN_NAME, \n          is_nullable = CASE LOWER (col.IS_NULLABLE) WHEN 'yes' THEN 1 ELSE 0 END,\n          is_identity = COLUMNPROPERTY (OBJECT_ID (col.TABLE_SCHEMA + '.' + col.TABLE_NAME), col.COLUMN_NAME, 'IsIdentity'),\n          is_primary_key = CASE WHEN ccu.COLUMN_NAME IS NULL THEN 0 ELSE 1 END\n        FROM\n          INFORMATION_SCHEMA.COLUMNS AS col\n        LEFT OUTER JOIN INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS tco ON\n          tco.TABLE_SCHEMA = col.TABLE_SCHEMA AND\n          tco.TABLE_NAME = col.TABLE_NAME AND\n          tco.CONSTRAINT_TYPE = 'PRIMARY KEY'\n        LEFT OUTER JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE AS ccu ON\n          ccu.CONSTRAINT_CATALOG = tco.CONSTRAINT_CATALOG AND\n          ccu.CONSTRAINT_SCHEMA = tco.CONSTRAINT_SCHEMA AND\n          ccu.CONSTRAINT_NAME = tco.CONSTRAINT_NAME AND\n          ccu.COLUMN_NAME = col.COLUMN_NAME\n        WHERE\n          col.TABLE_SCHEMA = '%s' AND\n          col.TABLE_NAME = '%s'\n      " % (schema, table)
        execute(sql)
        for (name, is_nullable, is_identity, is_primary_key) in c.fetchall():
            if is_identity and not is_nullable and is_primary_key:
                fields[name] = Sequence(name)
            else:
                fields[name] = Field(name)
            if is_nullable:
                nullable.append(name)

        constraint_sql = "\n      SELECT\n        tco.CONSTRAINT_CATALOG,\n        tco.CONSTRAINT_SCHEMA,\n        tco.CONSTRAINT_NAME\n      FROM\n        INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS tco\n      WHERE\n        tco.TABLE_SCHEMA = '%s' AND\n        tco.TABLE_NAME = '%s'\n      AND\n        tco.CONSTRAINT_TYPE IN ('UNIQUE', 'PRIMARY KEY')\n      " % (schema, table)
        column_sql = "\n      SELECT\n        ccu.COLUMN_NAME\n      FROM\n        INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE AS ccu\n      WHERE\n        ccu.CONSTRAINT_CATALOG = '%s' AND\n        ccu.CONSTRAINT_SCHEMA = '%s' AND\n        ccu.CONSTRAINT_NAME = '%s'\n      "
        execute(constraint_sql)
        for (constraint_catalog, constraint_schema, constraint_name) in c.fetchall():
            q2 = self.conn.cursor()
            q2.execute(column_sql % (constraint_catalog, constraint_schema, constraint_name))
            unique.add(frozenset([ r[0] for r in q2.fetchall() ]))

        sql = "\n      SELECT * FROM sysindexes WHERE id = OBJECT_ID ('%s.%s') AND indid BETWEEN 1 AND 254\n      " % (schema, table)
        execute(sql)
        rows = c.fetchall()
        print 'rows=', rows
        if rows:
            sql = "sp_helpindex '%s.%s'" % (schema, table)
            execute(sql)
            for (index_name, index_description, index_keys) in c.fetchall():
                descriptions = [ d.strip() for d in index_description.lower().replace(',', ' ').split() ]
                if 'unique' in descriptions:
                    unique.add(frozenset([ k.strip() for k in index_keys.split(',') ]))

        return (
         fields, unique)