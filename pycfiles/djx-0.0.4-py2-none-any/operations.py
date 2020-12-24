# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/db/backends/sqlite3/operations.py
# Compiled at: 2019-02-14 00:35:17
from __future__ import unicode_literals
import datetime, uuid
from django.conf import settings
from django.core.exceptions import FieldError
from django.db import utils
from django.db.backends import utils as backend_utils
from django.db.backends.base.operations import BaseDatabaseOperations
from django.db.models import aggregates, fields
from django.utils import six, timezone
from django.utils.dateparse import parse_date, parse_datetime, parse_time
from django.utils.duration import duration_string

class DatabaseOperations(BaseDatabaseOperations):

    def bulk_batch_size(self, fields, objs):
        """
        SQLite has a compile-time default (SQLITE_LIMIT_VARIABLE_NUMBER) of
        999 variables per query.

        If there's only a single field to insert, the limit is 500
        (SQLITE_MAX_COMPOUND_SELECT).
        """
        limit = 999 if len(fields) > 1 else 500
        if len(fields) > 0:
            return limit // len(fields)
        return len(objs)

    def check_expression_support(self, expression):
        bad_fields = (
         fields.DateField, fields.DateTimeField, fields.TimeField)
        bad_aggregates = (aggregates.Sum, aggregates.Avg, aggregates.Variance, aggregates.StdDev)
        if isinstance(expression, bad_aggregates):
            for expr in expression.get_source_expressions():
                try:
                    output_field = expr.output_field
                    if isinstance(output_field, bad_fields):
                        raise NotImplementedError(b'You cannot use Sum, Avg, StdDev, and Variance aggregations on date/time fields in sqlite3 since date/time is saved as text.')
                except FieldError:
                    pass

    def date_extract_sql(self, lookup_type, field_name):
        return b"django_date_extract('%s', %s)" % (lookup_type.lower(), field_name)

    def date_interval_sql(self, timedelta):
        return (
         b"'%s'" % duration_string(timedelta), [])

    def format_for_duration_arithmetic(self, sql):
        """Do nothing here, we will handle it in the custom function."""
        return sql

    def date_trunc_sql(self, lookup_type, field_name):
        return b"django_date_trunc('%s', %s)" % (lookup_type.lower(), field_name)

    def time_trunc_sql(self, lookup_type, field_name):
        return b"django_time_trunc('%s', %s)" % (lookup_type.lower(), field_name)

    def datetime_cast_date_sql(self, field_name, tzname):
        return (
         b'django_datetime_cast_date(%s, %%s)' % field_name, [tzname])

    def datetime_cast_time_sql(self, field_name, tzname):
        return (
         b'django_datetime_cast_time(%s, %%s)' % field_name, [tzname])

    def datetime_extract_sql(self, lookup_type, field_name, tzname):
        return (
         b"django_datetime_extract('%s', %s, %%s)" % (
          lookup_type.lower(), field_name), [tzname])

    def datetime_trunc_sql(self, lookup_type, field_name, tzname):
        return (
         b"django_datetime_trunc('%s', %s, %%s)" % (
          lookup_type.lower(), field_name), [tzname])

    def time_extract_sql(self, lookup_type, field_name):
        return b"django_time_extract('%s', %s)" % (lookup_type.lower(), field_name)

    def pk_default_value(self):
        return b'NULL'

    def _quote_params_for_last_executed_query(self, params):
        """
        Only for last_executed_query! Don't use this to execute SQL queries!
        """
        BATCH_SIZE = 999
        if len(params) > BATCH_SIZE:
            results = ()
            for index in range(0, len(params), BATCH_SIZE):
                chunk = params[index:index + BATCH_SIZE]
                results += self._quote_params_for_last_executed_query(chunk)

            return results
        sql = b'SELECT ' + (b', ').join([b'QUOTE(?)'] * len(params))
        cursor = self.connection.connection.cursor()
        try:
            return cursor.execute(sql, params).fetchone()
        finally:
            cursor.close()

    def last_executed_query(self, cursor, sql, params):
        if params:
            if isinstance(params, (list, tuple)):
                params = self._quote_params_for_last_executed_query(params)
            else:
                keys = params.keys()
                values = tuple(params.values())
                values = self._quote_params_for_last_executed_query(values)
                params = dict(zip(keys, values))
            return sql % params
        else:
            return sql

    def quote_name(self, name):
        if name.startswith(b'"') and name.endswith(b'"'):
            return name
        return b'"%s"' % name

    def no_limit_value(self):
        return -1

    def sql_flush(self, style, tables, sequences, allow_cascade=False):
        sql = [ b'%s %s %s;' % (style.SQL_KEYWORD(b'DELETE'), style.SQL_KEYWORD(b'FROM'), style.SQL_FIELD(self.quote_name(table))) for table in tables
              ]
        return sql

    def adapt_datetimefield_value(self, value):
        if value is None:
            return
        else:
            if hasattr(value, b'resolve_expression'):
                return value
            if timezone.is_aware(value):
                if settings.USE_TZ:
                    value = timezone.make_naive(value, self.connection.timezone)
                else:
                    raise ValueError(b'SQLite backend does not support timezone-aware datetimes when USE_TZ is False.')
            return six.text_type(value)

    def adapt_timefield_value(self, value):
        if value is None:
            return
        else:
            if hasattr(value, b'resolve_expression'):
                return value
            if timezone.is_aware(value):
                raise ValueError(b'SQLite backend does not support timezone-aware times.')
            return six.text_type(value)

    def get_db_converters(self, expression):
        converters = super(DatabaseOperations, self).get_db_converters(expression)
        internal_type = expression.output_field.get_internal_type()
        if internal_type == b'DateTimeField':
            converters.append(self.convert_datetimefield_value)
        elif internal_type == b'DateField':
            converters.append(self.convert_datefield_value)
        elif internal_type == b'TimeField':
            converters.append(self.convert_timefield_value)
        elif internal_type == b'DecimalField':
            converters.append(self.convert_decimalfield_value)
        elif internal_type == b'UUIDField':
            converters.append(self.convert_uuidfield_value)
        elif internal_type in ('NullBooleanField', 'BooleanField'):
            converters.append(self.convert_booleanfield_value)
        return converters

    def convert_datetimefield_value(self, value, expression, connection, context):
        if value is not None:
            if not isinstance(value, datetime.datetime):
                value = parse_datetime(value)
            if settings.USE_TZ and not timezone.is_aware(value):
                value = timezone.make_aware(value, self.connection.timezone)
        return value

    def convert_datefield_value(self, value, expression, connection, context):
        if value is not None:
            if not isinstance(value, datetime.date):
                value = parse_date(value)
        return value

    def convert_timefield_value(self, value, expression, connection, context):
        if value is not None:
            if not isinstance(value, datetime.time):
                value = parse_time(value)
        return value

    def convert_decimalfield_value(self, value, expression, connection, context):
        if value is not None:
            value = expression.output_field.format_number(value)
            value = backend_utils.typecast_decimal(value)
        return value

    def convert_uuidfield_value(self, value, expression, connection, context):
        if value is not None:
            value = uuid.UUID(value)
        return value

    def convert_booleanfield_value(self, value, expression, connection, context):
        if value in (1, 0):
            return bool(value)
        return value

    def bulk_insert_sql(self, fields, placeholder_rows):
        return (b' UNION ALL ').join(b'SELECT %s' % (b', ').join(row) for row in placeholder_rows)

    def combine_expression(self, connector, sub_expressions):
        if connector == b'^':
            return b'django_power(%s)' % (b',').join(sub_expressions)
        return super(DatabaseOperations, self).combine_expression(connector, sub_expressions)

    def combine_duration_expression(self, connector, sub_expressions):
        if connector not in ('+', '-'):
            raise utils.DatabaseError(b'Invalid connector for timedelta: %s.' % connector)
        fn_params = [
         b"'%s'" % connector] + sub_expressions
        if len(fn_params) > 3:
            raise ValueError(b'Too many params for timedelta operations.')
        return b'django_format_dtdelta(%s)' % (b', ').join(fn_params)

    def integer_field_range(self, internal_type):
        return (None, None)

    def subtract_temporals(self, internal_type, lhs, rhs):
        lhs_sql, lhs_params = lhs
        rhs_sql, rhs_params = rhs
        if internal_type == b'TimeField':
            return (b'django_time_diff(%s, %s)' % (lhs_sql, rhs_sql), lhs_params + rhs_params)
        return (
         b'django_timestamp_diff(%s, %s)' % (lhs_sql, rhs_sql), lhs_params + rhs_params)