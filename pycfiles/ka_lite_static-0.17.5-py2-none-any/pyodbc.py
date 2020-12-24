# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/South/south/db/sql_server/pyodbc.py
# Compiled at: 2018-07-11 18:15:31
from datetime import date, datetime, time
from warnings import warn
from django.db import models
from django.db.models import fields
from south.db import generic
from south.db.generic import delete_column_constraints, invalidate_table_constraints, copy_column_constraints
from south.exceptions import ConstraintDropped
from south.utils.py3 import string_types
try:
    from django.utils.encoding import smart_text
except ImportError:
    from django.utils.encoding import smart_unicode as smart_text

from django.core.management.color import no_style

class DatabaseOperations(generic.DatabaseOperations):
    """
    django-pyodbc (sql_server.pyodbc) implementation of database operations.
    """
    backend_name = 'pyodbc'
    add_column_string = 'ALTER TABLE %s ADD %s;'
    alter_string_set_type = 'ALTER COLUMN %(column)s %(type)s'
    alter_string_set_null = 'ALTER COLUMN %(column)s %(type)s NULL'
    alter_string_drop_null = 'ALTER COLUMN %(column)s %(type)s NOT NULL'
    allows_combined_alters = False
    drop_index_string = 'DROP INDEX %(index_name)s ON %(table_name)s'
    drop_constraint_string = 'ALTER TABLE %(table_name)s DROP CONSTRAINT %(constraint_name)s'
    delete_column_string = 'ALTER TABLE %s DROP COLUMN %s'
    create_foreign_key_sql = 'ALTER TABLE %(table)s ADD CONSTRAINT %(constraint)s ' + 'FOREIGN KEY (%(column)s) REFERENCES %(target)s'
    create_unique_sql = 'ALTER TABLE %(table)s ADD CONSTRAINT %(constraint)s UNIQUE (%(columns)s)'
    default_schema_name = 'dbo'
    has_booleans = False

    @delete_column_constraints
    def delete_column(self, table_name, name):
        q_table_name, q_name = self.quote_name(table_name), self.quote_name(name)
        for const in self._find_constraints_for_column(table_name, name):
            params = {'table_name': q_table_name, 'constraint_name': const}
            sql = self.drop_constraint_string % params
            self.execute(sql, [])

        for ind in self._find_indexes_for_column(table_name, name):
            params = {'table_name': q_table_name, 'index_name': ind}
            sql = self.drop_index_string % params
            self.execute(sql, [])

        drop_default = self.drop_column_default_sql(table_name, name)
        if drop_default:
            sql = 'ALTER TABLE [%s] %s' % (table_name, drop_default)
            self.execute(sql, [])
        self.execute(self.delete_column_string % (q_table_name, q_name), [])

    def _find_indexes_for_column(self, table_name, name):
        """Find the indexes that apply to a column, needed when deleting"""
        sql = "\n        SELECT si.name, si.id, sik.colid, sc.name\n        FROM dbo.sysindexes si WITH (NOLOCK)\n        INNER JOIN dbo.sysindexkeys sik WITH (NOLOCK)\n            ON  sik.id = si.id\n            AND sik.indid = si.indid\n        INNER JOIN dbo.syscolumns sc WITH (NOLOCK)\n            ON  si.id = sc.id\n            AND sik.colid = sc.colid\n        WHERE si.indid !=0\n            AND si.id = OBJECT_ID('%s')\n            AND sc.name = '%s'\n        "
        idx = self.execute(sql % (table_name, name), [])
        return [ i[0] for i in idx ]

    def _find_constraints_for_column(self, table_name, name, just_names=True):
        """
        Find the constraints that apply to a column, needed when deleting. Defaults not included.
        This is more general than the parent _constraints_affecting_columns, as on MSSQL this
        includes PK and FK constraints.
        """
        sql = "\n         SELECT CC.[CONSTRAINT_NAME]\n              ,TC.[CONSTRAINT_TYPE]\n              ,CHK.[CHECK_CLAUSE]\n              ,RFD.TABLE_SCHEMA\n              ,RFD.TABLE_NAME\n              ,RFD.COLUMN_NAME\n              -- used for normalized names\n              ,CC.TABLE_NAME\n              ,CC.COLUMN_NAME\n          FROM [INFORMATION_SCHEMA].[TABLE_CONSTRAINTS] TC\n          JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE CC\n               ON TC.CONSTRAINT_CATALOG = CC.CONSTRAINT_CATALOG \n              AND TC.CONSTRAINT_SCHEMA = CC.CONSTRAINT_SCHEMA\n              AND TC.CONSTRAINT_NAME = CC.CONSTRAINT_NAME\n          LEFT JOIN INFORMATION_SCHEMA.CHECK_CONSTRAINTS CHK\n               ON CHK.CONSTRAINT_CATALOG = CC.CONSTRAINT_CATALOG\n              AND CHK.CONSTRAINT_SCHEMA = CC.CONSTRAINT_SCHEMA\n              AND CHK.CONSTRAINT_NAME = CC.CONSTRAINT_NAME\n              AND 'CHECK' = TC.CONSTRAINT_TYPE\n          LEFT JOIN INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS REF\n               ON REF.CONSTRAINT_CATALOG = CC.CONSTRAINT_CATALOG\n              AND REF.CONSTRAINT_SCHEMA = CC.CONSTRAINT_SCHEMA\n              AND REF.CONSTRAINT_NAME = CC.CONSTRAINT_NAME\n              AND 'FOREIGN KEY' = TC.CONSTRAINT_TYPE\n          LEFT JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE RFD\n               ON RFD.CONSTRAINT_CATALOG = REF.UNIQUE_CONSTRAINT_CATALOG\n              AND RFD.CONSTRAINT_SCHEMA = REF.UNIQUE_CONSTRAINT_SCHEMA\n              AND RFD.CONSTRAINT_NAME = REF.UNIQUE_CONSTRAINT_NAME\n          WHERE CC.CONSTRAINT_CATALOG = CC.TABLE_CATALOG\n            AND CC.CONSTRAINT_SCHEMA = CC.TABLE_SCHEMA\n            AND CC.TABLE_CATALOG = %s\n            AND CC.TABLE_SCHEMA = %s\n            AND CC.TABLE_NAME = %s\n            AND CC.COLUMN_NAME = %s \n        "
        db_name = self._get_setting('name')
        schema_name = self._get_schema_name()
        table = self.execute(sql, [db_name, schema_name, table_name, name])
        if just_names:
            return [ r[0] for r in table ]
        all = {}
        for r in table:
            cons_name, type = r[:2]
            if type == 'PRIMARY KEY' or type == 'UNIQUE':
                cons = all.setdefault(cons_name, (type, []))
                sql = '\n                SELECT COLUMN_NAME\n                FROM INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE RFD\n                WHERE RFD.CONSTRAINT_CATALOG = %s\n                  AND RFD.CONSTRAINT_SCHEMA = %s\n                  AND RFD.TABLE_NAME = %s\n                  AND RFD.CONSTRAINT_NAME = %s\n                '
                columns = self.execute(sql, [db_name, schema_name, table_name, cons_name])
                cons[1].extend(col for col, in columns)
            elif type == 'CHECK':
                cons = (
                 type, r[2])
            elif type == 'FOREIGN KEY':
                if cons_name in all:
                    raise NotImplementedError('Multiple-column foreign keys are not supported')
                else:
                    cons = (
                     type, r[3:6])
            else:
                raise NotImplementedError("Don't know how to handle constraints of type " + type)
            all[cons_name] = cons

        return all

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
        self._fix_field_definition(field)
        if not ignore_constraints:
            qn = self.quote_name
            sch = qn(self._get_schema_name())
            tab = qn(table_name)
            table = ('.').join([sch, tab])
            try:
                self.delete_foreign_key(table_name, name)
            except ValueError:
                pass

            constraints = self._find_constraints_for_column(table_name, name, False)
            for constraint in constraints.keys():
                params = dict(table_name=table, constraint_name=qn(constraint))
                sql = self.drop_constraint_string % params
                self.execute(sql, [])

        ret_val = super(DatabaseOperations, self).alter_column(table_name, name, field, explicit_name, ignore_constraints=True)
        if not ignore_constraints:
            for cname, (ctype, args) in constraints.items():
                params = dict(table=table, constraint=qn(cname))
                if ctype == 'UNIQUE':
                    params['columns'] = (', ').join(map(qn, args))
                    sql = self.create_unique_sql % params
                elif ctype == 'PRIMARY KEY':
                    params['columns'] = (', ').join(map(qn, args))
                    sql = self.create_primary_key_string % params
                elif ctype == 'FOREIGN KEY':
                    continue
                elif ctype == 'CHECK':
                    warn(ConstraintDropped('CHECK ' + args, table_name, name))
                    continue
                else:
                    raise NotImplementedError("Don't know how to handle constraints of type " + type)
                self.execute(sql, [])

            if field.rel and self.supports_foreign_keys:
                self.execute(self.foreign_key_sql(table_name, field.column, field.rel.to._meta.db_table, field.rel.to._meta.get_field(field.rel.field_name).column))
                model = self.mock_model('FakeModelForIndexCreation', table_name)
                for stmt in self._get_connection().creation.sql_indexes_for_field(model, field, no_style()):
                    self.execute(stmt)

        return ret_val

    def _alter_set_defaults(self, field, name, params, sqls):
        """Subcommand of alter_column that sets default values (overrideable)"""
        table_name = self.quote_name(params['table_name'])
        drop_default = self.drop_column_default_sql(table_name, name)
        if drop_default:
            sqls.append((drop_default, []))

    def _value_to_unquoted_literal(self, field, value):
        conn = self._get_connection()
        value = field.get_db_prep_save(value, connection=conn)
        if isinstance(value, string_types):
            return smart_text(value)
        else:
            if isinstance(value, (date, time, datetime)):
                return value.isoformat()
            return str(value)

    def _default_value_workaround(self, value):
        if isinstance(value, (date, time, datetime)):
            return value.isoformat()
        else:
            return super(DatabaseOperations, self)._default_value_workaround(value)

    def _quote_string(self, s):
        return "'" + s.replace("'", "''") + "'"

    def drop_column_default_sql(self, table_name, name, q_name=None):
        """MSSQL specific drop default, which is a pain"""
        sql = "\n        SELECT object_name(cdefault)\n        FROM syscolumns\n        WHERE id = object_id('%s')\n        AND name = '%s'\n        "
        cons = self.execute(sql % (table_name, name), [])
        if cons and cons[0] and cons[0][0]:
            return 'DROP CONSTRAINT %s' % cons[0][0]
        else:
            return

    def _fix_field_definition(self, field):
        if isinstance(field, (fields.BooleanField, fields.NullBooleanField)):
            if field.default == True:
                field.default = 1
            if field.default == False:
                field.default = 0

    @invalidate_table_constraints
    def add_column(self, table_name, name, field, keep_default=False):
        """
        Adds the column 'name' to the table 'table_name'.
        Uses the 'field' paramater, a django.db.models.fields.Field instance,
        to generate the necessary sql

        @param table_name: The name of the table to add the column to
        @param name: The name of the column to add
        @param field: The field to use
        """
        self._fix_field_definition(field)
        sql = self.column_sql(table_name, name, field)
        if sql:
            params = (self.quote_name(table_name),
             sql)
            sql = self.add_column_string % params
            self.execute(sql)
            if not keep_default and field.default is not None:
                field.default = fields.NOT_PROVIDED
                self.drop_default(table_name, name, field)
        return

    @invalidate_table_constraints
    def drop_default(self, table_name, name, field):
        fragment = self.drop_column_default_sql(table_name, name)
        if fragment:
            table_name = self.quote_name(table_name)
            sql = (' ').join(['ALTER TABLE', table_name, fragment])
            self.execute(sql)

    @invalidate_table_constraints
    def create_table(self, table_name, field_defs):
        for _, f in field_defs:
            self._fix_field_definition(f)

        super(DatabaseOperations, self).create_table(table_name, field_defs)

    def _find_referencing_fks(self, table_name):
        """MSSQL does not support cascading FKs when dropping tables, we need to implement."""
        sql = '\n        SELECT FKTU.TABLE_SCHEMA as REFING_TABLE_SCHEMA,\n               FKTU.TABLE_NAME as REFING_TABLE_NAME,\n               FK.[CONSTRAINT_NAME] as FK_NAME\n        FROM [INFORMATION_SCHEMA].[REFERENTIAL_CONSTRAINTS] FK\n        JOIN [INFORMATION_SCHEMA].[CONSTRAINT_TABLE_USAGE] UCTU\n          ON FK.UNIQUE_CONSTRAINT_CATALOG = UCTU.CONSTRAINT_CATALOG and\n             FK.UNIQUE_CONSTRAINT_NAME = UCTU.CONSTRAINT_NAME and\n             FK.UNIQUE_CONSTRAINT_SCHEMA = UCTU.CONSTRAINT_SCHEMA\n        JOIN [INFORMATION_SCHEMA].[CONSTRAINT_TABLE_USAGE] FKTU\n          ON FK.CONSTRAINT_CATALOG = FKTU.CONSTRAINT_CATALOG and\n             FK.CONSTRAINT_NAME = FKTU.CONSTRAINT_NAME and\n             FK.CONSTRAINT_SCHEMA = FKTU.CONSTRAINT_SCHEMA\n        WHERE FK.CONSTRAINT_CATALOG = %s\n          AND UCTU.TABLE_SCHEMA = %s -- REFD_TABLE_SCHEMA\n          AND UCTU.TABLE_NAME = %s -- REFD_TABLE_NAME\n        '
        db_name = self._get_setting('name')
        schema_name = self._get_schema_name()
        return self.execute(sql, [db_name, schema_name, table_name])

    @invalidate_table_constraints
    def delete_table(self, table_name, cascade=True):
        """
        Deletes the table 'table_name'.
        """
        if cascade:
            refing = self._find_referencing_fks(table_name)
            for schmea, table, constraint in refing:
                table = ('.').join(map(self.quote_name, [schmea, table]))
                params = dict(table_name=table, constraint_name=self.quote_name(constraint))
                sql = self.drop_constraint_string % params
                self.execute(sql, [])

            cascade = False
        super(DatabaseOperations, self).delete_table(table_name, cascade)

    @copy_column_constraints
    @delete_column_constraints
    def rename_column(self, table_name, old, new):
        """
        Renames the column of 'table_name' from 'old' to 'new'.
        WARNING - This isn't transactional on MSSQL!
        """
        if old == new:
            return
        params = (
         table_name, self.quote_name(old), self.quote_name(new))
        self.execute("EXEC sp_rename '%s.%s', %s, 'COLUMN'" % params)

    @invalidate_table_constraints
    def rename_table(self, old_table_name, table_name):
        """
        Renames the table 'old_table_name' to 'table_name'.
        WARNING - This isn't transactional on MSSQL!
        """
        if old_table_name == table_name:
            return
        params = (self.quote_name(old_table_name), self.quote_name(table_name))
        self.execute('EXEC sp_rename %s, %s' % params)

    def _db_type_for_alter_column(self, field):
        return self._db_positive_type_for_alter_column(DatabaseOperations, field)

    def _alter_add_column_mods(self, field, name, params, sqls):
        return self._alter_add_positive_check(DatabaseOperations, field, name, params, sqls)

    @invalidate_table_constraints
    def delete_foreign_key(self, table_name, column):
        super(DatabaseOperations, self).delete_foreign_key(table_name, column)
        find_index_sql = '\n            SELECT i.name -- s.name, t.name,  c.name\n            FROM sys.tables t\n            INNER JOIN sys.schemas s ON t.schema_id = s.schema_id\n            INNER JOIN sys.indexes i ON i.object_id = t.object_id\n            INNER JOIN sys.index_columns ic ON ic.object_id = t.object_id\n                                            AND ic.index_id = i.index_id\n            INNER JOIN sys.columns c ON c.object_id = t.object_id \n                                     AND ic.column_id = c.column_id\n            WHERE i.is_unique=0 AND i.is_primary_key=0 AND i.is_unique_constraint=0\n              AND s.name = %s\n              AND t.name = %s\n              AND c.name = %s\n            '
        schema = self._get_schema_name()
        indexes = self.execute(find_index_sql, [schema, table_name, column])
        qn = self.quote_name
        for index in (i[0] for i in indexes if i[0]):
            self.execute('DROP INDEX %s on %s.%s' % (qn(index), qn(schema), qn(table_name)))