# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/South/south/db/firebird.py
# Compiled at: 2018-07-11 18:15:31
from __future__ import print_function
import datetime
from django.db import connection, models
from django.core.management.color import no_style
from django.db.utils import DatabaseError
from south.db import generic
from south.utils.py3 import string_types

class DatabaseOperations(generic.DatabaseOperations):
    backend_name = 'firebird'
    alter_string_set_type = 'ALTER %(column)s TYPE %(type)s'
    alter_string_set_default = 'ALTER %(column)s SET DEFAULT %(default)s;'
    alter_string_drop_null = ''
    add_column_string = 'ALTER TABLE %s ADD %s;'
    delete_column_string = 'ALTER TABLE %s DROP %s;'
    rename_table_sql = ''
    allows_combined_alters = False
    has_booleans = False

    def _fill_constraint_cache(self, db_name, table_name):
        self._constraint_cache.setdefault(db_name, {})
        self._constraint_cache[db_name][table_name] = {}
        rows = self.execute("\n            SELECT\n                rc.RDB$CONSTRAINT_NAME,\n                rc.RDB$CONSTRAINT_TYPE,\n                cc.RDB$TRIGGER_NAME\n            FROM rdb$relation_constraints rc\n            JOIN rdb$check_constraints cc\n            ON rc.rdb$constraint_name = cc.rdb$constraint_name\n            WHERE rc.rdb$constraint_type = 'NOT NULL'\n            AND rc.rdb$relation_name = '%s'\n            " % table_name)
        for constraint, kind, column in rows:
            self._constraint_cache[db_name][table_name].setdefault(column, set())
            self._constraint_cache[db_name][table_name][column].add((kind, constraint))

    def _alter_column_set_null(self, table_name, column_name, is_null):
        sql = "\n            UPDATE RDB$RELATION_FIELDS SET RDB$NULL_FLAG = %(null_flag)s\n            WHERE RDB$FIELD_NAME = '%(column)s'\n            AND RDB$RELATION_NAME = '%(table_name)s'\n        "
        null_flag = 'NULL' if is_null else '1'
        return sql % {'null_flag': null_flag, 
           'column': column_name.upper(), 
           'table_name': table_name.upper()}

    def _column_has_default(self, params):
        sql = "\n            SELECT a.RDB$DEFAULT_VALUE\n            FROM RDB$RELATION_FIELDS a\n            WHERE a.RDB$FIELD_NAME = '%(column)s'\n            AND a.RDB$RELATION_NAME = '%(table_name)s'\n        "
        value = self.execute(sql % params)
        if value:
            return True
        return False

    def _alter_set_defaults(self, field, name, params, sqls):
        """Subcommand of alter_column that sets default values (overrideable)"""
        if self._column_has_default(params):
            sqls.append(('ALTER COLUMN %s DROP DEFAULT' % (self.quote_name(name),), []))

    @generic.invalidate_table_constraints
    def create_table(self, table_name, fields):
        columns = []
        autoinc_sql = ''
        for field_name, field in fields:
            field._suppress_default = True
            col = self.column_sql(table_name, field_name, field)
            if not col:
                continue
            columns.append(col)
            if isinstance(field, models.AutoField):
                field_name = field.db_column or field.column
                autoinc_sql = connection.ops.autoinc_sql(table_name, field_name)

        self.execute(self.create_table_sql % {'table': self.quote_name(table_name), 
           'columns': (', ').join([ col for col in columns if col ])})
        if autoinc_sql:
            self.execute(autoinc_sql[0])
            self.execute(autoinc_sql[1])

    def rename_table(self, old_table_name, table_name):
        """
        Renames table is not supported by firebird.
        This involve recreate all related objects (store procedure, views, triggers, etc)
        """
        pass

    @generic.invalidate_table_constraints
    def delete_table(self, table_name, cascade=False):
        """
        Deletes the table 'table_name'.
        Firebird will also delete any triggers associated with the table.
        """
        super(DatabaseOperations, self).delete_table(table_name, cascade=False)
        sql = connection.ops.drop_sequence_sql(table_name)
        if sql:
            try:
                self.execute(sql)
            except:
                pass

    def column_sql(self, table_name, field_name, field, tablespace='', with_name=True, field_prepared=False):
        """
        Creates the SQL snippet for a column. Used by add_column and add_table.
        """
        if not field_prepared:
            field.set_attributes_from_name(field_name)
        if hasattr(field, 'south_init'):
            field.south_init()
        field = self._field_sanity(field)
        try:
            sql = field.db_type(connection=self._get_connection())
        except TypeError:
            sql = field.db_type()

        if sql:
            if with_name:
                field_output = [
                 self.quote_name(field.column), sql]
            else:
                field_output = [
                 sql]
            if field.primary_key:
                field_output.append('NOT NULL PRIMARY KEY')
            elif field.unique:
                field_output.append('UNIQUE')
            sql = (' ').join(field_output)
            sqlparams = ()
            if not getattr(field, '_suppress_default', False):
                if field.has_default():
                    default = field.get_default()
                    if default is not None:
                        if callable(default):
                            default = default()
                        if isinstance(default, string_types):
                            default = "'%s'" % default.replace("'", "''")
                        elif isinstance(default, (datetime.date, datetime.time, datetime.datetime)):
                            default = "'%s'" % default
                        elif isinstance(default, bool):
                            default = int(default)
                        if isinstance(default, string_types):
                            default = default.replace('%', '%%')
                        sql += ' DEFAULT %s'
                        sqlparams = default
                elif not field.null and field.blank or field.get_default() == '':
                    if field.empty_strings_allowed and self._get_connection().features.interprets_empty_strings_as_nulls:
                        sql += " DEFAULT ''"
            if not field.primary_key and not field.null:
                sql += ' NOT NULL'
            if field.rel and self.supports_foreign_keys:
                self.add_deferred_sql(self.foreign_key_sql(table_name, field.column, field.rel.to._meta.db_table, field.rel.to._meta.get_field(field.rel.field_name).column))
        if hasattr(field, 'post_create_sql'):
            for stmt in field.post_create_sql(no_style(), table_name):
                self.add_deferred_sql(stmt)

        if not field.rel:
            if hasattr(self._get_connection().creation, 'sql_indexes_for_field'):
                model = self.mock_model('FakeModelForGISCreation', table_name)
                for stmt in self._get_connection().creation.sql_indexes_for_field(model, field, no_style()):
                    self.add_deferred_sql(stmt)

        if sql:
            return sql % sqlparams
        else:
            return
            return

    def _drop_constraints(self, table_name, name, field):
        if self.has_check_constraints:
            check_constraints = self._constraints_affecting_columns(table_name, [name], 'CHECK')
            for constraint in check_constraints:
                self.execute(self.delete_check_sql % {'table': self.quote_name(table_name), 
                   'constraint': self.quote_name(constraint)})

        unique_constraint = list(self._constraints_affecting_columns(table_name, [name], 'UNIQUE'))
        if field.unique and not unique_constraint:
            self.create_unique(table_name, [name])
        else:
            if not field.unique and unique_constraint:
                self.delete_unique(table_name, [name])
            try:
                self.delete_foreign_key(table_name, name)
            except ValueError:
                pass

    @generic.invalidate_table_constraints
    def alter_column(self, table_name, name, field, explicit_name=True, ignore_constraints=False):
        """
        Alters the given column name so it will match the given field.
        Note that conversion between the two by the database must be possible.
        Will not automatically add _id by default; to have this behavour, pass
        explicit_name=False.

        @param table_name: The name of the table to add the column to
        @param name: The name of the column to alter
        @param field: The new field definition to use
        """
        if self.dry_run:
            if self.debug:
                print('   - no dry run output for alter_column() due to dynamic DDL, sorry')
            return
        if hasattr(field, 'south_init'):
            field.south_init()
        field.set_attributes_from_name(name)
        if not explicit_name:
            name = field.column
        else:
            field.column = name
        if not ignore_constraints:
            self._drop_constraints(table_name, name, field)
        params = {'column': self.quote_name(name), 
           'type': self._db_type_for_alter_column(field), 
           'table_name': table_name}
        sqls = []
        sqls_extra = []
        if params['type'] is not None:
            sqls.append((self.alter_string_set_type % params, []))
        self._alter_add_column_mods(field, name, params, sqls)
        sqls_extra.append(self._alter_column_set_null(table_name, name, field.null))
        self._alter_set_defaults(field, name, params, sqls)
        if self.allows_combined_alters:
            sqls, values = list(zip(*sqls))
            self.execute('ALTER TABLE %s %s;' % (self.quote_name(table_name), (', ').join(sqls)), generic.flatten(values))
        else:
            for sql, values in sqls:
                try:
                    self.execute('ALTER TABLE %s %s;' % (self.quote_name(table_name), sql), values)
                except DatabaseError as e:
                    print(e)

            for sql in sqls_extra:
                self.execute(sql)

        if not ignore_constraints:
            if field.rel and self.supports_foreign_keys:
                self.execute(self.foreign_key_sql(table_name, field.column, field.rel.to._meta.db_table, field.rel.to._meta.get_field(field.rel.field_name).column))
        return

    @generic.copy_column_constraints
    @generic.delete_column_constraints
    def rename_column(self, table_name, old, new):
        if old == new:
            return []
        self.execute('ALTER TABLE %s ALTER %s TO %s;' % (
         self.quote_name(table_name),
         self.quote_name(old),
         self.quote_name(new)))