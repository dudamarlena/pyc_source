# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/South/south/db/postgresql_psycopg2.py
# Compiled at: 2018-07-11 18:15:31
from __future__ import print_function
import uuid
from django.db.backends.util import truncate_name
from south.db import generic

class DatabaseOperations(generic.DatabaseOperations):
    """
    PsycoPG2 implementation of database operations.
    """
    backend_name = 'postgres'

    def create_index_name(self, table_name, column_names, suffix=''):
        """
        Generate a unique name for the index

        Django's logic for naming field indexes is different in the
        postgresql_psycopg2 backend, so we follow that for single-column
        indexes.
        """
        if len(column_names) == 1:
            return truncate_name('%s_%s%s' % (table_name, column_names[0], suffix), self._get_connection().ops.max_name_length())
        return super(DatabaseOperations, self).create_index_name(table_name, column_names, suffix)

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
    def rename_table(self, old_table_name, table_name):
        """will rename the table and an associated ID sequence and primary key index"""
        generic.DatabaseOperations.rename_table(self, old_table_name, table_name)
        if self.execute('\n            SELECT 1\n            FROM information_schema.sequences\n            WHERE sequence_name = %s\n            ', [
         old_table_name + '_id_seq']):
            generic.DatabaseOperations.rename_table(self, old_table_name + '_id_seq', table_name + '_id_seq')
        pkey_index_names = self.execute('\n            SELECT pg_index.indexrelid::regclass\n            FROM pg_index, pg_attribute\n            WHERE\n              indrelid = %s::regclass AND\n              pg_attribute.attrelid = indrelid AND\n              pg_attribute.attnum = any(pg_index.indkey)\n              AND indisprimary\n            ', [
         table_name])
        if old_table_name + '_pkey' in pkey_index_names:
            generic.DatabaseOperations.rename_table(self, old_table_name + '_pkey', table_name + '_pkey')

    def rename_index(self, old_index_name, index_name):
        """Rename an index individually"""
        generic.DatabaseOperations.rename_table(self, old_index_name, index_name)

    def _default_value_workaround(self, value):
        """Support for UUIDs on psql"""
        if isinstance(value, uuid.UUID):
            return str(value)
        else:
            return super(DatabaseOperations, self)._default_value_workaround(value)

    def _db_type_for_alter_column(self, field):
        return self._db_positive_type_for_alter_column(DatabaseOperations, field)

    def _alter_add_column_mods(self, field, name, params, sqls):
        return self._alter_add_positive_check(DatabaseOperations, field, name, params, sqls)