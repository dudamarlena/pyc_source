# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/db/backends/postgresql_psycopg2/operations.py
# Compiled at: 2018-07-11 18:15:30
from __future__ import unicode_literals
from django.db.backends import BaseDatabaseOperations

class DatabaseOperations(BaseDatabaseOperations):

    def __init__(self, connection):
        super(DatabaseOperations, self).__init__(connection)

    def date_extract_sql(self, lookup_type, field_name):
        if lookup_type == b'week_day':
            return b"EXTRACT('dow' FROM %s) + 1" % field_name
        else:
            return b"EXTRACT('%s' FROM %s)" % (lookup_type, field_name)

    def date_interval_sql(self, sql, connector, timedelta):
        """
        implements the interval functionality for expressions
        format for Postgres:
            (datefield + interval '3 days 200 seconds 5 microseconds')
        """
        modifiers = []
        if timedelta.days:
            modifiers.append(b'%s days' % timedelta.days)
        if timedelta.seconds:
            modifiers.append(b'%s seconds' % timedelta.seconds)
        if timedelta.microseconds:
            modifiers.append(b'%s microseconds' % timedelta.microseconds)
        mods = (b' ').join(modifiers)
        conn = b' %s ' % connector
        return b'(%s)' % conn.join([sql, b"interval '%s'" % mods])

    def date_trunc_sql(self, lookup_type, field_name):
        return b"DATE_TRUNC('%s', %s)" % (lookup_type, field_name)

    def deferrable_sql(self):
        return b' DEFERRABLE INITIALLY DEFERRED'

    def lookup_cast(self, lookup_type):
        lookup = b'%s'
        if lookup_type in ('iexact', 'contains', 'icontains', 'startswith', 'istartswith',
                           'endswith', 'iendswith'):
            lookup = b'%s::text'
        if lookup_type in ('iexact', 'icontains', 'istartswith', 'iendswith'):
            lookup = b'UPPER(%s)' % lookup
        return lookup

    def field_cast_sql(self, db_type):
        if db_type == b'inet':
            return b'HOST(%s)'
        return b'%s'

    def last_insert_id(self, cursor, table_name, pk_name):
        cursor.execute(b"SELECT CURRVAL(pg_get_serial_sequence('%s','%s'))" % (
         self.quote_name(table_name), pk_name))
        return cursor.fetchone()[0]

    def no_limit_value(self):
        return

    def quote_name(self, name):
        if name.startswith(b'"') and name.endswith(b'"'):
            return name
        return b'"%s"' % name

    def set_time_zone_sql(self):
        return b'SET TIME ZONE %s'

    def sql_flush(self, style, tables, sequences):
        if tables:
            sql = [
             b'%s %s;' % (
              style.SQL_KEYWORD(b'TRUNCATE'),
              style.SQL_FIELD((b', ').join([ self.quote_name(table) for table in tables ])))]
            sql.extend(self.sequence_reset_by_name_sql(style, sequences))
            return sql
        else:
            return []

    def sequence_reset_by_name_sql(self, style, sequences):
        sql = []
        for sequence_info in sequences:
            table_name = sequence_info[b'table']
            column_name = sequence_info[b'column']
            if not (column_name and len(column_name) > 0):
                column_name = b'id'
            sql.append(b"%s setval(pg_get_serial_sequence('%s','%s'), 1, false);" % (
             style.SQL_KEYWORD(b'SELECT'),
             style.SQL_TABLE(self.quote_name(table_name)),
             style.SQL_FIELD(column_name)))

        return sql

    def tablespace_sql(self, tablespace, inline=False):
        if inline:
            return b'USING INDEX TABLESPACE %s' % self.quote_name(tablespace)
        else:
            return b'TABLESPACE %s' % self.quote_name(tablespace)

    def sequence_reset_sql(self, style, model_list):
        from django.db import models
        output = []
        qn = self.quote_name
        for model in model_list:
            for f in model._meta.local_fields:
                if isinstance(f, models.AutoField):
                    output.append(b"%s setval(pg_get_serial_sequence('%s','%s'), coalesce(max(%s), 1), max(%s) %s null) %s %s;" % (
                     style.SQL_KEYWORD(b'SELECT'),
                     style.SQL_TABLE(qn(model._meta.db_table)),
                     style.SQL_FIELD(f.column),
                     style.SQL_FIELD(qn(f.column)),
                     style.SQL_FIELD(qn(f.column)),
                     style.SQL_KEYWORD(b'IS NOT'),
                     style.SQL_KEYWORD(b'FROM'),
                     style.SQL_TABLE(qn(model._meta.db_table))))
                    break

            for f in model._meta.many_to_many:
                if not f.rel.through:
                    output.append(b"%s setval(pg_get_serial_sequence('%s','%s'), coalesce(max(%s), 1), max(%s) %s null) %s %s;" % (
                     style.SQL_KEYWORD(b'SELECT'),
                     style.SQL_TABLE(qn(f.m2m_db_table())),
                     style.SQL_FIELD(b'id'),
                     style.SQL_FIELD(qn(b'id')),
                     style.SQL_FIELD(qn(b'id')),
                     style.SQL_KEYWORD(b'IS NOT'),
                     style.SQL_KEYWORD(b'FROM'),
                     style.SQL_TABLE(qn(f.m2m_db_table()))))

        return output

    def savepoint_create_sql(self, sid):
        return b'SAVEPOINT %s' % sid

    def savepoint_commit_sql(self, sid):
        return b'RELEASE SAVEPOINT %s' % sid

    def savepoint_rollback_sql(self, sid):
        return b'ROLLBACK TO SAVEPOINT %s' % sid

    def prep_for_iexact_query(self, x):
        return x

    def check_aggregate_support(self, aggregate):
        """Check that the backend fully supports the provided aggregate.

        The implementation of population statistics (STDDEV_POP and VAR_POP)
        under Postgres 8.2 - 8.2.4 is known to be faulty. Raise
        NotImplementedError if this is the database in use.
        """
        if aggregate.sql_function in ('STDDEV_POP', 'VAR_POP'):
            pg_version = self.connection.pg_version
            if pg_version >= 80200 and pg_version <= 80204:
                raise NotImplementedError(b'PostgreSQL 8.2 to 8.2.4 is known to have a faulty implementation of %s. Please upgrade your version of PostgreSQL.' % aggregate.sql_function)

    def max_name_length(self):
        """
        Returns the maximum length of an identifier.

        Note that the maximum length of an identifier is 63 by default, but can
        be changed by recompiling PostgreSQL after editing the NAMEDATALEN
        macro in src/include/pg_config_manual.h .

        This implementation simply returns 63, but can easily be overridden by a
        custom database backend that inherits most of its behavior from this one.
        """
        return 63

    def distinct_sql(self, fields):
        if fields:
            return b'DISTINCT ON (%s)' % (b', ').join(fields)
        else:
            return b'DISTINCT'

    def last_executed_query(self, cursor, sql, params):
        if cursor.query is not None:
            return cursor.query.decode(b'utf-8')
        else:
            return

    def return_insert_id(self):
        return (
         b'RETURNING %s', ())

    def bulk_insert_sql(self, fields, num_values):
        items_sql = b'(%s)' % (b', ').join([b'%s'] * len(fields))
        return b'VALUES ' + (b', ').join([items_sql] * num_values)