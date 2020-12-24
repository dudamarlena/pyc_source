# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/South/south/db/oracle.py
# Compiled at: 2018-07-11 18:15:31
from __future__ import print_function
import os.path, sys, re, warnings, cx_Oracle
from django.db import connection, models
from django.db.backends.util import truncate_name
from django.core.management.color import no_style
from django.db.models.fields import NOT_PROVIDED
from django.db.utils import DatabaseError
try:
    from django.db.backends.oracle.base import get_sequence_name as original_get_sequence_name
except ImportError:
    original_get_sequence_name = None

from south.db import generic

class DatabaseOperations(generic.DatabaseOperations):
    """
    Oracle implementation of database operations.    
    """
    backend_name = 'oracle'
    alter_string_set_type = 'ALTER TABLE %(table_name)s MODIFY %(column)s %(type)s %(nullity)s;'
    alter_string_set_default = 'ALTER TABLE %(table_name)s MODIFY %(column)s DEFAULT %(default)s;'
    alter_string_update_nulls_to_default = 'UPDATE %(table_name)s SET %(column)s = %(default)s WHERE %(column)s IS NULL;'
    add_column_string = 'ALTER TABLE %s ADD %s;'
    delete_column_string = 'ALTER TABLE %s DROP COLUMN %s;'
    add_constraint_string = 'ALTER TABLE %(table_name)s ADD CONSTRAINT %(constraint)s %(clause)s'
    allows_combined_alters = False
    has_booleans = False
    constraints_dict = {'P': 'PRIMARY KEY', 
       'U': 'UNIQUE', 
       'C': 'CHECK', 
       'R': 'FOREIGN KEY'}

    def get_sequence_name(self, table_name):
        if original_get_sequence_name is None:
            return self._get_connection().ops._get_sequence_name(table_name)
        else:
            return original_get_sequence_name(table_name)
            return

    def adj_column_sql(self, col):
        col = re.sub('(?P<constr>CHECK \\(.*\\))(?P<any>.*)(?P<default>DEFAULT \\d+)', lambda mo: '%s %s%s' % (mo.group('default'), mo.group('constr'), mo.group('any')), col)
        col = re.sub('(?P<not_null>(NOT )?NULL) (?P<misc>(.* )?)(?P<default>DEFAULT.+)', lambda mo: '%s %s %s' % (mo.group('default'), mo.group('not_null'), mo.group('misc') or ''), col)
        return col

    def check_meta(self, table_name):
        return table_name in [ m._meta.db_table for m in models.get_models() ]

    def normalize_name(self, name):
        """
        Get the properly shortened and uppercased identifier as returned by quote_name(), but without the actual quotes.
        """
        nn = self.quote_name(name)
        if nn[0] == '"' and nn[(-1)] == '"':
            nn = nn[1:-1]
        return nn

    @generic.invalidate_table_constraints
    def create_table(self, table_name, fields):
        qn = self.quote_name(table_name)
        columns = []
        autoinc_sql = ''
        for field_name, field in fields:
            field = self._field_sanity(field)
            field._suppress_default = True
            col = self.column_sql(table_name, field_name, field)
            if not col:
                continue
            col = self.adj_column_sql(col)
            columns.append(col)
            if isinstance(field, models.AutoField):
                autoinc_sql = connection.ops.autoinc_sql(table_name, field_name)

        sql = 'CREATE TABLE %s (%s);' % (qn, (', ').join([ col for col in columns ]))
        self.execute(sql)
        if autoinc_sql:
            self.execute(autoinc_sql[0])
            self.execute(autoinc_sql[1])

    @generic.invalidate_table_constraints
    def delete_table(self, table_name, cascade=True):
        qn = self.quote_name(table_name)
        if cascade:
            self.execute('DROP TABLE %s CASCADE CONSTRAINTS;' % qn)
        else:
            self.execute('DROP TABLE %s;' % qn)
        sequence_sql = '\nDECLARE\n    i INTEGER;\nBEGIN\n    SELECT COUNT(*) INTO i FROM USER_CATALOG\n        WHERE TABLE_NAME = \'%(sq_name)s\' AND TABLE_TYPE = \'SEQUENCE\';\n    IF i = 1 THEN\n        EXECUTE IMMEDIATE \'DROP SEQUENCE "%(sq_name)s"\';\n    END IF;\nEND;\n/' % {'sq_name': self.get_sequence_name(table_name)}
        self.execute(sequence_sql)

    @generic.invalidate_table_constraints
    def alter_column(self, table_name, name, field, explicit_name=True, ignore_constraints=False):
        if self.dry_run:
            if self.debug:
                print('   - no dry run output for alter_column() due to dynamic DDL, sorry')
            return
        qn = self.quote_name(table_name)
        if hasattr(field, 'south_init'):
            field.south_init()
        field = self._field_sanity(field)
        field.set_attributes_from_name(name)
        if not explicit_name:
            name = field.column
        qn_col = self.quote_name(name)
        params = {'table_name': qn, 
           'column': qn_col, 
           'type': self._db_type_for_alter_column(field), 
           'nullity': 'NOT NULL', 
           'default': 'NULL'}
        if field.null:
            params['nullity'] = 'NULL'
        sql_templates = [
         (
          self.alter_string_set_type, params, []),
         (
          self.alter_string_set_default, params, [])]
        if not field.null and field.has_default():

            def change_params(**kw):
                """A little helper for non-destructively changing the params"""
                p = params.copy()
                p.update(kw)
                return p

            sql_templates[:0] = [
             (
              self.alter_string_set_type, change_params(nullity='NULL'), []),
             (
              self.alter_string_update_nulls_to_default, change_params(default='%s'), [field.get_default()])]
        if not ignore_constraints:
            check_constraints = self._constraints_affecting_columns(table_name, [name], 'CHECK')
            for constraint in check_constraints:
                self.execute(self.delete_check_sql % {'table': self.quote_name(table_name), 
                   'constraint': self.quote_name(constraint)})

            try:
                self.delete_foreign_key(qn, qn_col)
            except ValueError:
                pass

        for sql_template, params, args in sql_templates:
            try:
                self.execute(sql_template % params, args, print_all_errors=False)
            except DatabaseError as exc:
                description = str(exc)
                if 'ORA-01442' in description or 'ORA-01451' in description:
                    params['nullity'] = ''
                    sql = sql_template % params
                    self.execute(sql)
                elif 'ORA-22858' in description or 'ORA-22859' in description:
                    self._alter_column_lob_workaround(table_name, name, field)
                else:
                    self._print_sql_error(exc, sql_template % params)
                    raise

        if not ignore_constraints:
            if field.rel:
                self.add_deferred_sql(self.foreign_key_sql(qn[1:-1], qn_col[1:-1], field.rel.to._meta.db_table, field.rel.to._meta.get_field(field.rel.field_name).column))

    def _alter_column_lob_workaround(self, table_name, name, field):
        """
        Oracle refuses to change a column type from/to LOB to/from a regular
        column. In Django, this shows up when the field is changed from/to
        a TextField.
        What we need to do instead is:
        - Rename the original column
        - Add the desired field as new
        - Update the table to transfer values from old to new
        - Drop old column
        """
        renamed = self._generate_temp_name(name)
        self.rename_column(table_name, name, renamed)
        self.add_column(table_name, name, field, keep_default=False)
        self.execute('UPDATE %s set %s=%s' % (
         self.quote_name(table_name),
         self.quote_name(name),
         self.quote_name(renamed)))
        self.delete_column(table_name, renamed)

    def _generate_temp_name(self, for_name):
        suffix = hex(hash(for_name)).upper()[1:]
        return self.normalize_name(for_name + '_' + suffix)

    @generic.copy_column_constraints
    @generic.delete_column_constraints
    def rename_column(self, table_name, old, new):
        if old == new:
            return []
        self.execute('ALTER TABLE %s RENAME COLUMN %s TO %s;' % (
         self.quote_name(table_name),
         self.quote_name(old),
         self.quote_name(new)))

    @generic.invalidate_table_constraints
    def add_column(self, table_name, name, field, keep_default=False):
        field = self._field_sanity(field)
        sql = self.column_sql(table_name, name, field)
        sql = self.adj_column_sql(sql)
        if sql:
            params = (self.quote_name(table_name),
             sql)
            sql = self.add_column_string % params
            self.execute(sql)
            if field.default is not None:
                field.default = NOT_PROVIDED
                self.alter_column(table_name, name, field, explicit_name=False, ignore_constraints=True)
        return

    def delete_column(self, table_name, name):
        return super(DatabaseOperations, self).delete_column(self.quote_name(table_name), name)

    def lookup_constraint(self, db_name, table_name, column_name=None):
        if column_name:
            column_name = self.normalize_name(column_name)
        return super(DatabaseOperations, self).lookup_constraint(db_name, table_name, column_name)

    def _constraints_affecting_columns(self, table_name, columns, type='UNIQUE'):
        if columns:
            columns = [ self.normalize_name(c) for c in columns ]
        return super(DatabaseOperations, self)._constraints_affecting_columns(table_name, columns, type)

    def _field_sanity(self, field):
        """
        This particular override stops us sending DEFAULTs for BooleanField.
        """
        if isinstance(field, models.BooleanField) and field.has_default():
            field.default = int(field.to_python(field.get_default()))
        if isinstance(field, (models.CharField, models.TextField)):
            field.null = field.empty_strings_allowed
        return field

    def _default_value_workaround(self, value):
        from datetime import date, time, datetime
        if isinstance(value, (date, time, datetime)):
            return "'%s'" % value
        else:
            return super(DatabaseOperations, self)._default_value_workaround(value)

    def _fill_constraint_cache(self, db_name, table_name):
        self._constraint_cache.setdefault(db_name, {})
        self._constraint_cache[db_name][table_name] = {}
        rows = self.execute("\n            SELECT user_cons_columns.constraint_name,\n                   user_cons_columns.column_name,\n                   user_constraints.constraint_type\n            FROM user_constraints\n            JOIN user_cons_columns ON\n                 user_constraints.table_name = user_cons_columns.table_name AND \n                 user_constraints.constraint_name = user_cons_columns.constraint_name\n            WHERE user_constraints.table_name = '%s'\n        " % self.normalize_name(table_name))
        for constraint, column, kind in rows:
            self._constraint_cache[db_name][table_name].setdefault(column, set())
            self._constraint_cache[db_name][table_name][column].add((self.constraints_dict[kind], constraint))