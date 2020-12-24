# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydo/drivers/psycopgconn.py
# Compiled at: 2007-02-15 13:23:36
"""
PyDO driver for PostgreSQL, using the psycopg driver.

Currently this has been tested with psycopg 1.1.18 and 1.99.1.12,
and attempts to support both.

"""
from pydo.dbi import DBIBase, ConnectionPool
from pydo.exceptions import PyDOError
from pydo.log import debug
from pydo.operators import BindingConverter
from pydo.dbtypes import DATE, TIMESTAMP, BINARY, INTERVAL, date_formats, timestamp_formats
from pydo.field import Field
import time, datetime
try:
    import psycopg2 as psycopg
except ImportError:
    import psycopg

if psycopg.__version__[:3] >= '1.9':
    psycopg_version = 2
else:
    psycopg_version = 1
try:
    import mx.DateTime
    havemx = True
except ImportError:
    havemx = False

if havemx:
    try:
        from psycopg import TimestampFromMx
    except:
        assert psycopg_version == 2

        def TimestampFromMx(x):
            return psycopg.TimestampFromTicks(x.ticks())


elif psycopg_version == 1:
    raise ImportError, 'mx.DateTime required when using psycopg version 1'

def convert_DATE(dt):
    val = dt.value
    if havemx and isinstance(val, mx.DateTime.DateTimeType):
        return psycopg.DateFromMx(val)
    elif isinstance(val, datetime.date):
        return psycopg.Date(dt.year, dt.month, dt.day)
    elif isinstance(val, (int, float, long)):
        d = datetime.date.fromtimestamp(val)
        return psycopg.Date(d.year, d.month, d.day)
    elif isinstance(val, (tuple, list)):
        return psycopg.Date(*val[:3])
    elif isinstance(val, basestring):
        for f in date_formats:
            try:
                t = time.strptime(val, f)[:3]
            except ValueError:
                continue
            else:
                return psycopg.Date(*t)
        else:
            raise ValueError, "cannot parse date format: '%s'" % val
    raise ValueError, val


def convert_TIMESTAMP(ts):
    val = ts.value
    if havemx and isinstance(val, mx.DateTime.DateTimeType):
        return TimestampFromMx(val)
    elif isinstance(val, datetime.datetime):
        return psycopg.TimestampFromTicks(time.mktime(ts.timetuple()))
    elif isinstance(val, (int, float, long)):
        return psycopg.TimestampFromTicks(val)
    elif isinstance(val, (tuple, list)) and len(val) == 9:
        return psycopg.TimestampFromTicks(time.mktime(val))
    elif isinstance(val, basestring):
        for f in timestamp_formats:
            try:
                t = time.strptime(val, f)
            except ValueError:
                continue
            else:
                return psycopg.TimestampFromTicks(time.mktime(t))
        else:
            raise ValueError, "cannot parse timestamp format: '%s'" % val
    raise ValueError, val


_converters = {datetime.datetime: lambda x: psycopg.TimestampFromTicks(time.mktime(x.timetuple())), 
   datetime.date: lambda x: psycopg.Date(x.year, x.month, x.day), 
   DATE: convert_DATE, TIMESTAMP: convert_TIMESTAMP, BINARY: lambda x: psycopg.Binary(x.value), 
   INTERVAL: lambda x: x.value}
if havemx:
    _converters[mx.DateTime.DateTimeType] = TimestampFromMx
    _converters[mx.DateTime.DateTimeDeltaType] = lambda x: x.strftime('%d:%H:%M:%S')

class PsycopgConverter(BindingConverter):
    __module__ = __name__
    converters = _converters


class PsycopgDBI(DBIBase):
    __module__ = __name__

    def __init__(self, connectArgs, pool=None, verbose=False, initFunc=None):
        if pool and not hasattr(pool, 'connect'):
            pool = ConnectionPool()
        super(PsycopgDBI, self).__init__(connectArgs, psycopg.connect, psycopg, pool, verbose, initFunc)
        if psycopg_version < 2:
            self._autocommit = None
        return

    if psycopg_version == 2:

        def autocommit():

            def fget(self):
                return self.conn.isolation_level == 0

            def fset(self, val):
                self.conn.set_isolation_level(not val)

            return (fget, fset, None, None)

        autocommit = property(*autocommit())
    else:
        autocommit = False

    def getConverter(self):
        return PsycopgConverter(self.paramstyle)

    def execute(self, sql, values=(), qualified=False):
        """Executes the statement with the values and does conversion
        of the return result as necessary.
        result is list of dictionaries, or number of rows affected"""
        if self.verbose:
            debug('SQL: %s', sql)
            debug('bind variables: %s', values)
        c = self.conn.cursor()
        if values:
            c.execute(sql, values)
        else:
            c.execute(sql)
        if c.statusmessage == 'SELECT':
            resultset = c.fetchall()
        else:
            resultset = None
        if not resultset:
            if c.statusmessage.startswith('INSERT') or c.statusmessage.startswith('UPDATE'):
                return int(c.statusmessage.split()[(-1)])
            return -1
        res = self._convertResultSet(c.description, resultset, qualified)
        c.close()
        return res

    def getSequence(self, name, field, table):
        if name == True:
            name = '%s_%s_seq' % (table, field)
            if self.verbose:
                debug('inferring sequence name: %s', name)
        cur = self.conn.cursor()
        sql = "select nextval('%s')" % name
        if self.verbose:
            debug('SQL: %s', (sql,))
        cur.execute(sql)
        res = cur.fetchone()
        if not res:
            raise PyDOError, 'could not get value for sequence %s!' % name
        return res[0]

    def listTables(self, schema=None):
        """lists the tables in the database schema"""
        if schema is None:
            schema = 'public'
        sql = '\n        SELECT t.tablename AS name\n        FROM pg_catalog.pg_tables t\n        WHERE t.schemaname=%s\n        UNION\n        SELECT v.viewname AS name\n        FROM pg_catalog.pg_views v\n        WHERE v.schemaname=%s\n        '
        cur = self.conn.cursor()
        if self.verbose:
            debug('SQL: %s', (sql,))
        cur.execute(sql, (schema, schema))
        res = cur.fetchall()
        cur.close()
        if not res:
            return []
        return sorted((x[0] for x in res))

    def describeTable(self, table, schema=None):
        sql = '\n        SELECT t.tablename AS tname\n        FROM pg_catalog.pg_tables t\n        WHERE t.tablename=%s\n        AND t.schemaname=%s\n        UNION\n        SELECT v.viewname AS tname\n        FROM pg_catalog.pg_views v\n        WHERE v.viewname=%s\n        and v.schemaname=%s\n        '
        if schema is None:
            schema = 'public'
        cur = self.conn.cursor()
        bind = (table, schema, table, schema)
        if self.verbose:
            debug('SQL: %s', (sql,))
        cur.execute(sql, bind)
        for row in cur.fetchall():
            break
        else:
            raise ValueError, 'no such table or view: %s.%s' % (schema, table)

        sql = '\n        SELECT a.attname, a.attnum\n        FROM pg_catalog.pg_attribute a,\n          pg_catalog.pg_namespace n,\n          pg_catalog.pg_class c\n        WHERE a.attrelid = %s::regclass\n          AND c.oid=a.attrelid\n          AND c.relnamespace=n.oid\n          AND n.nspname=%s\n          AND a.attnum > 0\n          AND NOT a.attisdropped\n        ORDER BY a.attnum\n        '
        fields = {}
        cur = self.conn.cursor()
        if self.verbose:
            debug('SQL: %s', (sql,))
        qtable = '%s.%s' % (schema, table)
        cur.execute(sql, (qtable, schema))
        for row in cur.fetchall():
            if self.verbose:
                debug('Found column %s' % list(row))
            fields[row[1]] = Field(row[0])

        sql = '\n        SELECT indkey\n        FROM pg_catalog.pg_index i,\n        pg_catalog.pg_class c,\n        pg_catalog.pg_namespace n,\n        pg_catalog.pg_attribute a\n        WHERE i.indrelid = %s::regclass\n          AND c.oid=i.indrelid\n          AND c.relnamespace=n.oid\n          AND n.nspname=%s\n          AND i.indisunique\n          AND a.attrelid=c.oid\n          AND a.attnum=indkey[0]\n          AND a.attnotnull\n        '
        unique = set()
        if self.verbose:
            debug('SQL: %s', (sql,))
        cur.execute(sql, (qtable, schema))
        for row in cur.fetchall():
            L = [ int(i) for i in row[0].split(' ') ]
            if [ x for x in L if x < 0 ]:
                if self.verbose:
                    debug('skipping constraint with system columns: %s' % row[0])
                continue
            if self.verbose:
                debug('Found unique index on %s' % L)
            if len(L) == 1:
                fields[L[0]].unique = True
            else:
                unique.add(frozenset([ fields[i].name for i in L ]))

        sql = "\n        SELECT c.relname\n        FROM pg_catalog.pg_class c, pg_catalog.pg_namespace n\n        WHERE relname like '%s_%%%%_seq'\n          AND c.relnamespace=n.oid\n          AND n.nspname=%%s\n          AND relkind = 'S'\n        " % table
        if self.verbose:
            debug('SQL: %s', (sql,))
        cur.execute(sql, (schema,))
        for row in cur.fetchall():
            maybecolname = row[0][len(table) + 1:-4]
            for field in fields.values():
                if field.name == maybecolname:
                    if self.verbose:
                        debug('Found sequence %s on %s' % (row[0], field.name))
                    field.sequence = row[0]
                    break

        cur.close()
        d = {}
        for f in fields.values():
            d[f.name] = f

        return (
         d, unique)