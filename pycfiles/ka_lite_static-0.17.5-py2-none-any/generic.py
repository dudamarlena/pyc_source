# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/South/south/db/generic.py
# Compiled at: 2018-07-11 18:15:31
from __future__ import print_function
import re, sys
from django.core.management.color import no_style
from django.db import transaction, models
from django.db.utils import DatabaseError
from django.db.backends.util import truncate_name
from django.db.backends.creation import BaseDatabaseCreation
from django.db.models.fields import NOT_PROVIDED
from django.dispatch import dispatcher
from django.conf import settings
from django.utils.datastructures import SortedDict
try:
    from django.utils.functional import cached_property
except ImportError:

    class cached_property(object):
        """
        Decorator that creates converts a method with a single
        self argument into a property cached on the instance.
        """

        def __init__(self, func):
            self.func = func

        def __get__(self, instance, type):
            res = instance.__dict__[self.func.__name__] = self.func(instance)
            return res


from south.logger import get_logger
from south.utils.py3 import string_types, text_type

def alias(attrname):
    """
    Returns a function which calls 'attrname' - for function aliasing.
    We can't just use foo = bar, as this breaks subclassing.
    """

    def func(self, *args, **kwds):
        return getattr(self, attrname)(*args, **kwds)

    return func


def invalidate_table_constraints(func):

    def _cache_clear(self, table, *args, **opts):
        self._set_cache(table, value=INVALID)
        return func(self, table, *args, **opts)

    return _cache_clear


def delete_column_constraints(func):

    def _column_rm(self, table, column, *args, **opts):
        self._set_cache(table, column, value=[])
        return func(self, table, column, *args, **opts)

    return _column_rm


def copy_column_constraints(func):

    def _column_cp(self, table, column_old, column_new, *args, **opts):
        db_name = self._get_setting('NAME')
        self._set_cache(table, column_new, value=self.lookup_constraint(db_name, table, column_old))
        return func(self, table, column_old, column_new, *args, **opts)

    return _column_cp


class INVALID(Exception):

    def __repr__(self):
        return 'INVALID'


class DryRunError(ValueError):
    pass


class DatabaseOperations(object):
    """
    Generic SQL implementation of the DatabaseOperations.
    Some of this code comes from Django Evolution.
    """
    alter_string_set_type = 'ALTER COLUMN %(column)s TYPE %(type)s'
    alter_string_set_null = 'ALTER COLUMN %(column)s DROP NOT NULL'
    alter_string_drop_null = 'ALTER COLUMN %(column)s SET NOT NULL'
    delete_check_sql = 'ALTER TABLE %(table)s DROP CONSTRAINT %(constraint)s'
    add_column_string = 'ALTER TABLE %s ADD COLUMN %s;'
    delete_unique_sql = 'ALTER TABLE %s DROP CONSTRAINT %s'
    delete_foreign_key_sql = 'ALTER TABLE %(table)s DROP CONSTRAINT %(constraint)s'
    create_table_sql = 'CREATE TABLE %(table)s (%(columns)s)'
    max_index_name_length = 63
    drop_index_string = 'DROP INDEX %(index_name)s'
    delete_column_string = 'ALTER TABLE %s DROP COLUMN %s CASCADE;'
    create_primary_key_string = 'ALTER TABLE %(table)s ADD CONSTRAINT %(constraint)s PRIMARY KEY (%(columns)s)'
    delete_primary_key_sql = 'ALTER TABLE %(table)s DROP CONSTRAINT %(constraint)s'
    add_check_constraint_fragment = 'ADD CONSTRAINT %(constraint)s CHECK (%(check)s)'
    rename_table_sql = 'ALTER TABLE %s RENAME TO %s;'
    backend_name = None
    default_schema_name = 'public'
    allows_combined_alters = True
    supports_foreign_keys = True
    has_check_constraints = True
    has_booleans = True
    raises_default_errors = True

    @cached_property
    def has_ddl_transactions(self):
        """
        Tests the database using feature detection to see if it has
        transactional DDL support.
        """
        self._possibly_initialise()
        connection = self._get_connection()
        if hasattr(connection.features, 'confirm') and not connection.features._confirmed:
            connection.features.confirm()
        exceptions = (DatabaseError,)
        try:
            from MySQLdb import OperationalError
            exceptions += (OperationalError,)
        except ImportError:
            pass

        if getattr(connection.features, 'supports_transactions', True):
            cursor = connection.cursor()
            self.start_transaction()
            cursor.execute('CREATE TABLE DDL_TRANSACTION_TEST (X INT)')
            self.rollback_transaction()
            try:
                try:
                    cursor.execute('CREATE TABLE DDL_TRANSACTION_TEST (X INT)')
                except exceptions:
                    return False

                return True
            finally:
                cursor.execute('DROP TABLE DDL_TRANSACTION_TEST')

        else:
            return False

    def __init__(self, db_alias):
        self.debug = False
        self.deferred_sql = []
        self.dry_run = False
        self.pending_transactions = 0
        self.pending_create_signals = []
        self.db_alias = db_alias
        self._constraint_cache = {}
        self._initialised = False

    def lookup_constraint(self, db_name, table_name, column_name=None):
        """ return a set() of constraints for db_name.table_name.column_name """

        def _lookup():
            table = self._constraint_cache[db_name][table_name]
            if table is INVALID:
                raise INVALID
            else:
                if column_name is None:
                    return list(table.items())
                else:
                    return table[column_name]

            return

        try:
            ret = _lookup()
            return ret
        except INVALID:
            del self._constraint_cache[db_name][table_name]
            self._fill_constraint_cache(db_name, table_name)
        except KeyError:
            if self._is_valid_cache(db_name, table_name):
                return []
            self._fill_constraint_cache(db_name, table_name)

        return self.lookup_constraint(db_name, table_name, column_name)

    def _set_cache(self, table_name, column_name=None, value=INVALID):
        db_name = self._get_setting('NAME')
        try:
            if column_name is not None:
                self._constraint_cache[db_name][table_name][column_name] = value
            else:
                self._constraint_cache[db_name][table_name] = value
        except (LookupError, TypeError):
            pass

        return

    def _is_valid_cache(self, db_name, table_name):
        try:
            return self._constraint_cache[db_name][table_name] is not INVALID
        except KeyError:
            return False

    def _is_multidb(self):
        try:
            from django.db import connections
            connections
        except ImportError:
            return False

        return True

    def _get_connection(self):
        """
        Returns a django connection for a given DB Alias
        """
        if self._is_multidb():
            from django.db import connections
            return connections[self.db_alias]
        else:
            from django.db import connection
            return connection

    def _get_setting(self, setting_name):
        """
        Allows code to get a setting (like, for example, STORAGE_ENGINE)
        """
        setting_name = setting_name.upper()
        connection = self._get_connection()
        if self._is_multidb():
            return connection.settings_dict[setting_name]
        else:
            return getattr(settings, 'DATABASE_%s' % setting_name)

    def _has_setting(self, setting_name):
        """
        Existence-checking version of _get_setting.
        """
        try:
            self._get_setting(setting_name)
        except (KeyError, AttributeError):
            return False

        return True

    def _get_schema_name(self):
        try:
            return self._get_setting('schema')
        except (KeyError, AttributeError):
            return self.default_schema_name

    def _possibly_initialise(self):
        if not self._initialised:
            self.connection_init()
            self._initialised = True

    def connection_init(self):
        """
        Run before any SQL to let database-specific config be sent as a command,
        e.g. which storage engine (MySQL) or transaction serialisability level.
        """
        pass

    def quote_name(self, name):
        """
        Uses the database backend to quote the given table/column name.
        """
        return self._get_connection().ops.quote_name(name)

    def _print_sql_error(self, e, sql, params=[]):
        print('FATAL ERROR - The following SQL query failed: %s' % sql, file=sys.stderr)
        print('The error was: %s' % e, file=sys.stderr)

    def execute(self, sql, params=[], print_all_errors=True):
        """
        Executes the given SQL statement, with optional parameters.
        If the instance's debug attribute is True, prints out what it executes.
        """
        self._possibly_initialise()
        cursor = self._get_connection().cursor()
        if self.debug:
            print('   = %s' % sql, params)
        if self.dry_run:
            return []
        get_logger().debug(text_type('execute "%s" with params "%s"' % (sql, params)))
        try:
            cursor.execute(sql, params)
        except DatabaseError as e:
            if print_all_errors:
                self._print_sql_error(e, sql, params)
            raise

        try:
            return cursor.fetchall()
        except:
            return []

    def execute_many(self, sql, regex="(?mx) ([^';]* (?:'[^']*'[^';]*)*)", comment_regex='(?mx) (?:^\\s*$)|(?:--.*$)'):
        """
        Takes a SQL file and executes it as many separate statements.
        (Some backends, such as Postgres, don't work otherwise.)
        """
        sql = ('\n').join([ x.strip().replace('%', '%%') for x in re.split(comment_regex, sql) if x.strip() ])
        for st in re.split(regex, sql)[1:][::2]:
            self.execute(st)

    def add_deferred_sql(self, sql):
        """
        Add a SQL statement to the deferred list, that won't be executed until
        this instance's execute_deferred_sql method is run.
        """
        self.deferred_sql.append(sql)

    def execute_deferred_sql(self):
        """
        Executes all deferred SQL, resetting the deferred_sql list
        """
        for sql in self.deferred_sql:
            self.execute(sql)

        self.deferred_sql = []

    def clear_deferred_sql(self):
        """
        Resets the deferred_sql list to empty.
        """
        self.deferred_sql = []

    def clear_run_data(self, pending_creates=None):
        """
        Resets variables to how they should be before a run. Used for dry runs.
        If you want, pass in an old panding_creates to reset to.
        """
        self.clear_deferred_sql()
        self.pending_create_signals = pending_creates or []

    def get_pending_creates(self):
        return self.pending_create_signals

    @invalidate_table_constraints
    def create_table(self, table_name, fields):
        """
        Creates the table 'table_name'. 'fields' is a tuple of fields,
        each repsented by a 2-part tuple of field name and a
        django.db.models.fields.Field object
        """
        if len(table_name) > 63:
            print('   ! WARNING: You have a table name longer than 63 characters; this will not fully work on PostgreSQL or MySQL.')
        for field_name, field in fields:
            field._suppress_default = True

        columns = [ self.column_sql(table_name, field_name, field) for field_name, field in fields
                  ]
        self.execute(self.create_table_sql % {'table': self.quote_name(table_name), 
           'columns': (', ').join([ col for col in columns if col ])})

    add_table = alias('create_table')

    @invalidate_table_constraints
    def rename_table(self, old_table_name, table_name):
        """
        Renames the table 'old_table_name' to 'table_name'.
        """
        if old_table_name == table_name:
            return
        params = (self.quote_name(old_table_name), self.quote_name(table_name))
        self.execute(self.rename_table_sql % params)
        self._set_cache(table_name, value=INVALID)

    @invalidate_table_constraints
    def delete_table(self, table_name, cascade=True):
        """
        Deletes the table 'table_name'.
        """
        params = (
         self.quote_name(table_name),)
        if cascade:
            self.execute('DROP TABLE %s CASCADE;' % params)
        else:
            self.execute('DROP TABLE %s;' % params)

    drop_table = alias('delete_table')

    @invalidate_table_constraints
    def clear_table(self, table_name):
        """
        Deletes all rows from 'table_name'.
        """
        params = (
         self.quote_name(table_name),)
        self.execute('DELETE FROM %s;' % params)

    @invalidate_table_constraints
    def add_column(self, table_name, name, field, keep_default=True):
        """
        Adds the column 'name' to the table 'table_name'.
        Uses the 'field' paramater, a django.db.models.fields.Field instance,
        to generate the necessary sql

        @param table_name: The name of the table to add the column to
        @param name: The name of the column to add
        @param field: The field to use
        """
        sql = self.column_sql(table_name, name, field)
        if sql:
            params = (self.quote_name(table_name),
             sql)
            sql = self.add_column_string % params
            self.execute(sql)
            if field.default is not None:
                field.default = NOT_PROVIDED
                self.alter_column(table_name, name, field, explicit_name=False, ignore_constraints=True)
        return

    def _db_type_for_alter_column(self, field):
        """
        Returns a field's type suitable for ALTER COLUMN.
        By default it just returns field.db_type().
        To be overriden by backend specific subclasses
        @param field: The field to generate type for
        """
        try:
            return field.db_type(connection=self._get_connection())
        except TypeError:
            return field.db_type()

    def _alter_add_column_mods(self, field, name, params, sqls):
        """
        Subcommand of alter_column that modifies column definitions beyond
        the type string -- e.g. adding constraints where they cannot be specified
        as part of the type (overrideable)
        """
        pass

    def _alter_set_defaults(self, field, name, params, sqls):
        """Subcommand of alter_column that sets default values (overrideable)"""
        sqls.append(('ALTER COLUMN %s DROP DEFAULT' % (self.quote_name(name),), []))

    def _update_nulls_to_default(self, params, field):
        """Subcommand of alter_column that updates nulls to default value (overrideable)"""
        default = field.get_db_prep_save(field.get_default(), connection=self._get_connection())
        self.execute('UPDATE %(table_name)s SET %(column)s=%%s WHERE %(column)s IS NULL' % params, [default])

    @invalidate_table_constraints
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
            if self.has_check_constraints:
                check_constraints = self._constraints_affecting_columns(table_name, [name], 'CHECK')
                for constraint in check_constraints:
                    self.execute(self.delete_check_sql % {'table': self.quote_name(table_name), 
                       'constraint': self.quote_name(constraint)})

            try:
                self.delete_foreign_key(table_name, name)
            except ValueError:
                pass

        params = {'column': self.quote_name(name), 
           'type': self._db_type_for_alter_column(field), 
           'table_name': self.quote_name(table_name)}
        sqls = []
        if params['type'] is not None:
            sqls.append((self.alter_string_set_type % params, []))
        self._alter_add_column_mods(field, name, params, sqls)
        if field.null or field.has_default():
            sqls.append((self.alter_string_set_null % params, []))
        else:
            sqls.append((self.alter_string_drop_null % params, []))
        self._alter_set_defaults(field, name, params, sqls)
        if self.allows_combined_alters:
            sqls, values = zip(*sqls)
            self.execute('ALTER TABLE %s %s;' % (self.quote_name(table_name), (', ').join(sqls)), flatten(values))
        else:
            for sql, values in sqls:
                self.execute('ALTER TABLE %s %s;' % (self.quote_name(table_name), sql), values)

        if not field.null and field.has_default():
            self._update_nulls_to_default(params, field)
            self.execute('ALTER TABLE %s %s;' % (self.quote_name(table_name), self.alter_string_drop_null % params), [])
        if not ignore_constraints:
            if field.rel and self.supports_foreign_keys:
                self.execute(self.foreign_key_sql(table_name, field.column, field.rel.to._meta.db_table, field.rel.to._meta.get_field(field.rel.field_name).column))
        return

    def _fill_constraint_cache(self, db_name, table_name):
        schema = self._get_schema_name()
        ifsc_tables = ['constraint_column_usage', 'key_column_usage']
        self._constraint_cache.setdefault(db_name, {})
        self._constraint_cache[db_name][table_name] = {}
        for ifsc_table in ifsc_tables:
            rows = self.execute('\n                SELECT kc.constraint_name, kc.column_name, c.constraint_type\n                FROM information_schema.%s AS kc\n                JOIN information_schema.table_constraints AS c ON\n                    kc.table_schema = c.table_schema AND\n                    kc.table_name = c.table_name AND\n                    kc.constraint_name = c.constraint_name\n                WHERE\n                    kc.table_schema = %%s AND\n                    kc.table_name = %%s\n            ' % ifsc_table, [schema, table_name])
            for constraint, column, kind in rows:
                self._constraint_cache[db_name][table_name].setdefault(column, set())
                self._constraint_cache[db_name][table_name][column].add((kind, constraint))

    def _constraints_affecting_columns(self, table_name, columns, type='UNIQUE'):
        """
        Gets the names of the constraints affecting the given columns.
        If columns is None, returns all constraints of the type on the table.
        """
        if self.dry_run:
            raise DryRunError('Cannot get constraints for columns.')
        if columns is not None:
            columns = set(map(lambda s: s.lower(), columns))
        db_name = self._get_setting('NAME')
        cnames = {}
        for col, constraints in self.lookup_constraint(db_name, table_name):
            for kind, cname in constraints:
                if kind == type:
                    cnames.setdefault(cname, set())
                    cnames[cname].add(col.lower())

        for cname, cols in cnames.items():
            if cols == columns or columns is None:
                yield cname

        return

    @invalidate_table_constraints
    def create_unique(self, table_name, columns):
        """
        Creates a UNIQUE constraint on the columns on the given table.
        """
        if not isinstance(columns, (list, tuple)):
            columns = [
             columns]
        name = self.create_index_name(table_name, columns, suffix='_uniq')
        cols = (', ').join(map(self.quote_name, columns))
        self.execute('ALTER TABLE %s ADD CONSTRAINT %s UNIQUE (%s)' % (
         self.quote_name(table_name),
         self.quote_name(name),
         cols))
        return name

    @invalidate_table_constraints
    def delete_unique(self, table_name, columns):
        """
        Deletes a UNIQUE constraint on precisely the columns on the given table.
        """
        if not isinstance(columns, (list, tuple)):
            columns = [
             columns]
        if self.dry_run:
            if self.debug:
                print('   - no dry run output for delete_unique_column() due to dynamic DDL, sorry')
            return
        constraints = list(self._constraints_affecting_columns(table_name, columns))
        if not constraints:
            raise ValueError('Cannot find a UNIQUE constraint on table %s, columns %r' % (table_name, columns))
        for constraint in constraints:
            self.execute(self.delete_unique_sql % (
             self.quote_name(table_name),
             self.quote_name(constraint)))

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
            field_output.append('%sNULL' % (not field.null and 'NOT ' or ''))
            if field.primary_key:
                field_output.append('PRIMARY KEY')
            elif field.unique:
                field_output.append('UNIQUE')
            tablespace = field.db_tablespace or tablespace
            if tablespace and getattr(self._get_connection().features, 'supports_tablespaces', False) and field.unique:
                field_output.append(self._get_connection().ops.tablespace_sql(tablespace, inline=True))
            sql = (' ').join(field_output)
            sqlparams = ()
            if not getattr(field, '_suppress_default', False):
                if field.has_default():
                    default = field.get_default()
                    if default is not None:
                        if callable(default):
                            default = default()
                        default = field.get_db_prep_save(default, connection=self._get_connection())
                        default = self._default_value_workaround(default)
                        if isinstance(default, string_types):
                            default = "'%s'" % default.replace("'", "''")
                        if isinstance(default, string_types):
                            default = default.replace('%', '%%')
                        sql += ' DEFAULT %s'
                        sqlparams = default
                elif not field.null and field.blank or field.get_default() == '':
                    if field.empty_strings_allowed and self._get_connection().features.interprets_empty_strings_as_nulls:
                        sql += " DEFAULT ''"
            if field.rel and self.supports_foreign_keys:
                self.add_deferred_sql(self.foreign_key_sql(table_name, field.column, field.rel.to._meta.db_table, field.rel.to._meta.get_field(field.rel.field_name).column))
        if hasattr(field, 'post_create_sql'):
            for stmt in field.post_create_sql(no_style(), table_name):
                self.add_deferred_sql(stmt)

        if hasattr(self._get_connection().creation, 'sql_indexes_for_field'):
            model = self.mock_model('FakeModelForGISCreation', table_name)
            for stmt in self._get_connection().creation.sql_indexes_for_field(model, field, no_style()):
                self.add_deferred_sql(stmt)

        if sql:
            return sql % sqlparams
        else:
            return
            return

    def _field_sanity(self, field):
        """
        Placeholder for DBMS-specific field alterations (some combos aren't valid,
        e.g. DEFAULT and TEXT on MySQL)
        """
        return field

    def _default_value_workaround(self, value):
        """
        DBMS-specific value alterations (this really works around
        missing functionality in Django backends)
        """
        if isinstance(value, bool) and not self.has_booleans:
            return int(value)
        else:
            return value

    def foreign_key_sql(self, from_table_name, from_column_name, to_table_name, to_column_name):
        """
        Generates a full SQL statement to add a foreign key constraint
        """
        constraint_name = '%s_refs_%s_%s' % (from_column_name, to_column_name, self._digest(from_table_name, to_table_name))
        return 'ALTER TABLE %s ADD CONSTRAINT %s FOREIGN KEY (%s) REFERENCES %s (%s)%s;' % (
         self.quote_name(from_table_name),
         self.quote_name(self.shorten_name(constraint_name)),
         self.quote_name(from_column_name),
         self.quote_name(to_table_name),
         self.quote_name(to_column_name),
         self._get_connection().ops.deferrable_sql())

    @invalidate_table_constraints
    def delete_foreign_key(self, table_name, column):
        """
        Drop a foreign key constraint
        """
        if self.dry_run:
            if self.debug:
                print('   - no dry run output for delete_foreign_key() due to dynamic DDL, sorry')
            return
        constraints = self._find_foreign_constraints(table_name, column)
        if not constraints:
            raise ValueError('Cannot find a FOREIGN KEY constraint on table %s, column %s' % (table_name, column))
        for constraint_name in constraints:
            self.execute(self.delete_foreign_key_sql % {'table': self.quote_name(table_name), 
               'constraint': self.quote_name(constraint_name)})

    drop_foreign_key = alias('delete_foreign_key')

    def _find_foreign_constraints(self, table_name, column_name=None):
        constraints = self._constraints_affecting_columns(table_name, [column_name], 'FOREIGN KEY')
        primary_key_columns = self._find_primary_key_columns(table_name)
        if len(primary_key_columns) > 1:
            return list(constraints)
        else:
            primary_key_columns.add(column_name)
            recursive_constraints = set(self._constraints_affecting_columns(table_name, primary_key_columns, 'FOREIGN KEY'))
            return list(recursive_constraints.union(constraints))

    def _digest(self, *args):
        """
        Use django.db.backends.creation.BaseDatabaseCreation._digest
        to create index name in Django style. An evil hack :(
        """
        if not hasattr(self, '_django_db_creation'):
            self._django_db_creation = BaseDatabaseCreation(self._get_connection())
        return self._django_db_creation._digest(*args)

    def shorten_name(self, name):
        return truncate_name(name, self._get_connection().ops.max_name_length())

    def create_index_name(self, table_name, column_names, suffix=''):
        """
        Generate a unique name for the index
        """
        if len(column_names) == 1 and not suffix:
            try:
                _hash = self._digest([column_names[0]])
            except TypeError:
                _hash = self._digest(column_names[0])

            return self.shorten_name('%s_%s' % (table_name, _hash))
        table_name = table_name.replace('"', '').replace('.', '_')
        index_unique_name = '_%x' % abs(hash((table_name, (',').join(column_names))))
        index_name = ('%s_%s%s%s' % (table_name, column_names[0], index_unique_name, suffix)).replace('"', '').replace('.', '_')
        if len(index_name) > self.max_index_name_length:
            part = '_%s%s%s' % (column_names[0], index_unique_name, suffix)
            index_name = '%s%s' % (table_name[:self.max_index_name_length - len(part)], part)
        return index_name

    def create_index_sql(self, table_name, column_names, unique=False, db_tablespace=''):
        """
        Generates a create index statement on 'table_name' for a list of 'column_names'
        """
        if not column_names:
            print('No column names supplied on which to create an index')
            return ''
        connection = self._get_connection()
        if db_tablespace and connection.features.supports_tablespaces:
            tablespace_sql = ' ' + connection.ops.tablespace_sql(db_tablespace)
        else:
            tablespace_sql = ''
        index_name = self.create_index_name(table_name, column_names)
        return 'CREATE %sINDEX %s ON %s (%s)%s;' % (
         unique and 'UNIQUE ' or '',
         self.quote_name(index_name),
         self.quote_name(table_name),
         (',').join([ self.quote_name(field) for field in column_names ]),
         tablespace_sql)

    @invalidate_table_constraints
    def create_index(self, table_name, column_names, unique=False, db_tablespace=''):
        """ Executes a create index statement """
        sql = self.create_index_sql(table_name, column_names, unique, db_tablespace)
        self.execute(sql)

    @invalidate_table_constraints
    def delete_index(self, table_name, column_names, db_tablespace=''):
        """
        Deletes an index created with create_index.
        This is possible using only columns due to the deterministic
        index naming function which relies on column names.
        """
        if isinstance(column_names, string_types):
            column_names = [
             column_names]
        name = self.create_index_name(table_name, column_names)
        sql = self.drop_index_string % {'index_name': self.quote_name(name), 
           'table_name': self.quote_name(table_name)}
        self.execute(sql)

    drop_index = alias('delete_index')

    @delete_column_constraints
    def delete_column(self, table_name, name):
        """
        Deletes the column 'column_name' from the table 'table_name'.
        """
        params = (
         self.quote_name(table_name), self.quote_name(name))
        self.execute(self.delete_column_string % params, [])

    drop_column = alias('delete_column')

    def rename_column(self, table_name, old, new):
        """
        Renames the column 'old' from the table 'table_name' to 'new'.
        """
        raise NotImplementedError('rename_column has no generic SQL syntax')

    @invalidate_table_constraints
    def delete_primary_key(self, table_name):
        """
        Drops the old primary key.
        """
        if self.dry_run:
            if self.debug:
                print('   - no dry run output for delete_primary_key() due to dynamic DDL, sorry')
            return
        constraints = list(self._constraints_affecting_columns(table_name, None, type='PRIMARY KEY'))
        if not constraints:
            raise ValueError('Cannot find a PRIMARY KEY constraint on table %s' % (table_name,))
        for constraint in constraints:
            self.execute(self.delete_primary_key_sql % {'table': self.quote_name(table_name), 
               'constraint': self.quote_name(constraint)})

        return

    drop_primary_key = alias('delete_primary_key')

    @invalidate_table_constraints
    def create_primary_key(self, table_name, columns):
        """
        Creates a new primary key on the specified columns.
        """
        if not isinstance(columns, (list, tuple)):
            columns = [
             columns]
        self.execute(self.create_primary_key_string % {'table': self.quote_name(table_name), 
           'constraint': self.quote_name(table_name + '_pkey'), 
           'columns': (', ').join(map(self.quote_name, columns))})

    def _find_primary_key_columns(self, table_name):
        """
        Find all columns of the primary key of the specified table
        """
        db_name = self._get_setting('NAME')
        primary_key_columns = set()
        for col, constraints in self.lookup_constraint(db_name, table_name):
            for kind, cname in constraints:
                if kind == 'PRIMARY KEY':
                    primary_key_columns.add(col.lower())

        return primary_key_columns

    def start_transaction(self):
        """
        Makes sure the following commands are inside a transaction.
        Must be followed by a (commit|rollback)_transaction call.
        """
        if self.dry_run:
            self.pending_transactions += 1
        transaction.commit_unless_managed(using=self.db_alias)
        transaction.enter_transaction_management(using=self.db_alias)
        transaction.managed(True, using=self.db_alias)

    def commit_transaction(self):
        """
        Commits the current transaction.
        Must be preceded by a start_transaction call.
        """
        if self.dry_run:
            return
        transaction.commit(using=self.db_alias)
        transaction.leave_transaction_management(using=self.db_alias)

    def rollback_transaction(self):
        """
        Rolls back the current transaction.
        Must be preceded by a start_transaction call.
        """
        if self.dry_run:
            self.pending_transactions -= 1
        transaction.rollback(using=self.db_alias)
        transaction.leave_transaction_management(using=self.db_alias)

    def rollback_transactions_dry_run(self):
        """
        Rolls back all pending_transactions during this dry run.
        """
        if not self.dry_run:
            return
        while self.pending_transactions > 0:
            self.rollback_transaction()

        if transaction.is_dirty(using=self.db_alias):
            transaction.leave_transaction_management(using=self.db_alias)

    def send_create_signal(self, app_label, model_names):
        self.pending_create_signals.append((app_label, model_names))

    def send_pending_create_signals(self, verbosity=0, interactive=False):
        signals = SortedDict()
        for app_label, model_names in self.pending_create_signals:
            try:
                signals[app_label].extend(model_names)
            except KeyError:
                signals[app_label] = list(model_names)

        for app_label, model_names in signals.items():
            self.really_send_create_signal(app_label, list(set(model_names)), verbosity=verbosity, interactive=interactive)

        self.pending_create_signals = []

    def really_send_create_signal(self, app_label, model_names, verbosity=0, interactive=False):
        """
        Sends a post_syncdb signal for the model specified.

        If the model is not found (perhaps it's been deleted?),
        no signal is sent.

        TODO: The behavior of django.contrib.* apps seems flawed in that
        they don't respect created_models.  Rather, they blindly execute
        over all models within the app sending the signal.  This is a
        patch we should push Django to make  For now, this should work.
        """
        if self.debug:
            print(' - Sending post_syncdb signal for %s: %s' % (app_label, model_names))
        app = models.get_app(app_label)
        if not app:
            return
        created_models = []
        for model_name in model_names:
            model = models.get_model(app_label, model_name)
            if model:
                created_models.append(model)

        if created_models:
            if hasattr(dispatcher, 'send'):
                dispatcher.send(signal=models.signals.post_syncdb, sender=app, app=app, created_models=created_models, verbosity=verbosity, interactive=interactive)
            elif self._is_multidb():
                models.signals.post_syncdb.send(sender=app, app=app, created_models=created_models, verbosity=verbosity, interactive=interactive, db=self.db_alias)
            else:
                models.signals.post_syncdb.send(sender=app, app=app, created_models=created_models, verbosity=verbosity, interactive=interactive)

    def mock_model(self, model_name, db_table, db_tablespace='', pk_field_name='id', pk_field_type=models.AutoField, pk_field_args=[], pk_field_kwargs={}):
        """
        Generates a MockModel class that provides enough information
        to be used by a foreign key/many-to-many relationship.

        Migrations should prefer to use these rather than actual models
        as models could get deleted over time, but these can remain in
        migration files forever.

        Depreciated.
        """

        class MockOptions(object):

            def __init__(self):
                self.db_table = db_table
                self.db_tablespace = db_tablespace or settings.DEFAULT_TABLESPACE
                self.object_name = model_name
                self.module_name = model_name.lower()
                if pk_field_type == models.AutoField:
                    pk_field_kwargs['primary_key'] = True
                self.pk = pk_field_type(*pk_field_args, **pk_field_kwargs)
                self.pk.set_attributes_from_name(pk_field_name)
                self.abstract = False

            def get_field_by_name(self, field_name):
                return (
                 self.pk, self.model, True, False)

            def get_field(self, name):
                return self.pk

        class MockModel(object):
            _meta = None

        MockModel._meta = MockOptions()
        MockModel._meta.model = MockModel
        return MockModel

    def _db_positive_type_for_alter_column(self, klass, field):
        """
        A helper for subclasses overriding _db_type_for_alter_column:
        Remove the check constraint from the type string for PositiveInteger
        and PositiveSmallInteger fields.
        @param klass: The type of the child (required to allow this to be used when it is subclassed)
        @param field: The field to generate type for
        """
        super_result = super(klass, self)._db_type_for_alter_column(field)
        if isinstance(field, (models.PositiveSmallIntegerField, models.PositiveIntegerField)):
            return super_result.split(' ', 1)[0]
        return super_result

    def _alter_add_positive_check(self, klass, field, name, params, sqls):
        """
        A helper for subclasses overriding _alter_add_column_mods:
        Add a check constraint verifying positivity to PositiveInteger and
        PositiveSmallInteger fields.
        """
        super(klass, self)._alter_add_column_mods(field, name, params, sqls)
        if isinstance(field, (models.PositiveSmallIntegerField, models.PositiveIntegerField)):
            uniq_hash = abs(hash(tuple(params.values())))
            d = dict(constraint='CK_%s_PSTV_%s' % (name, hex(uniq_hash)[2:]), check='%s >= 0' % self.quote_name(name))
            sqls.append((self.add_check_constraint_fragment % d, []))


def flatten(ls):
    nl = []
    for l in ls:
        nl += l

    return nl