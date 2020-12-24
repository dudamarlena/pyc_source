# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\py_mysql\lib\mysql\connector\django\introspection.py
# Compiled at: 2017-12-07 02:34:36
# Size of source mod 2**32: 15560 bytes
import re
from collections import namedtuple
import django
if django.VERSION >= (1, 8):
    from django.db.backends.base.introspection import BaseDatabaseIntrospection, FieldInfo, TableInfo
else:
    from django.db.backends import BaseDatabaseIntrospection
if django.VERSION >= (1, 6):
    if django.VERSION < (1, 8):
        from django.db.backends import FieldInfo
    from django.utils.encoding import force_text
    if django.VERSION >= (1, 7):
        from django.utils.datastructures import OrderedSet
from mysql.connector.constants import FieldType
foreign_key_re = re.compile('\\sCONSTRAINT `[^`]*` FOREIGN KEY \\(`([^`]*)`\\) REFERENCES `([^`]*)` \\(`([^`]*)`\\)')
if django.VERSION >= (1, 8):
    FieldInfo = namedtuple('FieldInfo', FieldInfo._fields + ('extra', ))

class DatabaseIntrospection(BaseDatabaseIntrospection):
    data_types_reverse = {FieldType.BLOB: 'TextField', 
     FieldType.DECIMAL: 'DecimalField', 
     FieldType.NEWDECIMAL: 'DecimalField', 
     FieldType.DATE: 'DateField', 
     FieldType.DATETIME: 'DateTimeField', 
     FieldType.DOUBLE: 'FloatField', 
     FieldType.FLOAT: 'FloatField', 
     FieldType.INT24: 'IntegerField', 
     FieldType.LONG: 'IntegerField', 
     FieldType.LONGLONG: 'BigIntegerField', 
     FieldType.SHORT: 'IntegerField' if django.VERSION < (1, 8) else 'SmallIntegerField', 
     
     FieldType.STRING: 'CharField', 
     FieldType.TIME: 'TimeField', 
     FieldType.TIMESTAMP: 'DateTimeField', 
     FieldType.TINY: 'IntegerField', 
     FieldType.TINY_BLOB: 'TextField', 
     FieldType.MEDIUM_BLOB: 'TextField', 
     FieldType.LONG_BLOB: 'TextField', 
     FieldType.VAR_STRING: 'CharField'}

    def get_field_type(self, data_type, description):
        field_type = super(DatabaseIntrospection, self).get_field_type(data_type, description)
        if field_type == 'IntegerField':
            if 'auto_increment' in description.extra:
                return 'AutoField'
        return field_type

    def get_table_list(self, cursor):
        """Returns a list of table names in the current database."""
        cursor.execute('SHOW FULL TABLES')
        if django.VERSION >= (1, 8):
            return [TableInfo(row[0], {'BASE TABLE':'t',  'VIEW':'v'}.get(row[1])) for row in cursor.fetchall()]
        else:
            return [row[0] for row in cursor.fetchall()]

    if django.VERSION >= (1, 11):

        def get_table_description(self, cursor, table_name):
            """
            Returns a description of the table, with the DB-API
            cursor.description interface."
            """
            InfoLine = namedtuple('InfoLine', 'col_name data_type max_len num_prec num_scale extra column_default')
            cursor.execute('\n                SELECT column_name, data_type, character_maximum_length,\n                numeric_precision, numeric_scale, extra, column_default\n                FROM information_schema.columns\n                WHERE table_name = %s AND table_schema = DATABASE()', [
             table_name])
            field_info = dict((line[0], InfoLine(*line)) for line in cursor.fetchall())
            cursor.execute('SELECT * FROM %s LIMIT 1' % self.connection.ops.quote_name(table_name))
            to_int = lambda i: int(i) if i is not None else i
            fields = []
            for line in cursor.description:
                col_name = force_text(line[0])
                fields.append(FieldInfo(*(
                 col_name,) + line[1:3] + (
                 to_int(field_info[col_name].max_len) or line[3],
                 to_int(field_info[col_name].num_prec) or line[4],
                 to_int(field_info[col_name].num_scale) or line[5],
                 line[6],
                 field_info[col_name].column_default,
                 field_info[col_name].extra)))

            return fields

    else:
        if django.VERSION >= (1, 8):

            def get_table_description(self, cursor, table_name):
                """
            Returns a description of the table, with the DB-API
            cursor.description interface."
            """
                InfoLine = namedtuple('InfoLine', 'col_name data_type max_len num_prec num_scale extra')
                cursor.execute('\n                SELECT column_name, data_type, character_maximum_length,\n                numeric_precision, numeric_scale, extra\n                FROM information_schema.columns\n                WHERE table_name = %s AND table_schema = DATABASE()', [
                 table_name])
                field_info = dict((line[0], InfoLine(*line)) for line in cursor.fetchall())
                cursor.execute('SELECT * FROM %s LIMIT 1' % self.connection.ops.quote_name(table_name))
                to_int = lambda i: int(i) if i is not None else i
                fields = []
                for line in cursor.description:
                    col_name = force_text(line[0])
                    fields.append(FieldInfo(*(
                     col_name,) + line[1:3] + (to_int(field_info[col_name].max_len) or line[3], to_int(field_info[col_name].num_prec) or line[4], to_int(field_info[col_name].num_scale) or line[5]) + (line[6],) + (field_info[col_name].extra,)))

                return fields

        else:

            def get_table_description(self, cursor, table_name):
                """
            Returns a description of the table, with the DB-API
            cursor.description interface.
            """
                cursor.execute('SELECT column_name, character_maximum_length FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = %s AND table_schema = DATABASE() AND character_maximum_length IS NOT NULL', [
                 table_name])
                length_map = dict(cursor.fetchall())
                cursor.execute("SELECT column_name, numeric_precision, numeric_scale FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = %s AND table_schema = DATABASE() AND data_type='decimal'", [
                 table_name])
                numeric_map = dict((line[0], tuple([int(n) for n in line[1:]])) for line in cursor.fetchall())
                cursor.execute('SELECT * FROM {0} LIMIT 1'.format(self.connection.ops.quote_name(table_name)))
                if django.VERSION >= (1, 6):
                    return [FieldInfo(*(force_text(line[0]),) + line[1:3] + (length_map.get(line[0], line[3]),) + numeric_map.get(line[0], line[4:6]) + (line[6],)) for line in cursor.description]
                else:
                    return [line[:3] + (length_map.get(line[0], line[3]),) + line[4:] for line in cursor.description]

    def _name_to_index(self, cursor, table_name):
        """
        Returns a dictionary of {field_name: field_index} for the given table.
        Indexes are 0-based.
        """
        return dict((d[0], i) for i, d in enumerate(self.get_table_description(cursor, table_name)))

    def get_relations(self, cursor, table_name):
        """
        Returns a dictionary of {field_index: (field_index_other_table,
        other_table)}
        representing all relationships to the given table. Indexes are 0-based.
        """
        constraints = self.get_key_columns(cursor, table_name)
        relations = {}
        if django.VERSION >= (1, 8):
            for my_fieldname, other_table, other_field in constraints:
                relations[my_fieldname] = (
                 other_field, other_table)

            return relations
        else:
            my_field_dict = self._name_to_index(cursor, table_name)
            for my_fieldname, other_table, other_field in constraints:
                other_field_index = self._name_to_index(cursor, other_table)[other_field]
                my_field_index = my_field_dict[my_fieldname]
                relations[my_field_index] = (other_field_index, other_table)

            return relations

    def get_key_columns(self, cursor, table_name):
        """
        Returns a list of (column_name, referenced_table_name,
        referenced_column_name) for all key columns in given table.
        """
        key_columns = []
        cursor.execute('SELECT column_name, referenced_table_name, referenced_column_name FROM information_schema.key_column_usage WHERE table_name = %s AND table_schema = DATABASE() AND referenced_table_name IS NOT NULL AND referenced_column_name IS NOT NULL', [
         table_name])
        key_columns.extend(cursor.fetchall())
        return key_columns

    def get_indexes(self, cursor, table_name):
        cursor.execute('SHOW INDEX FROM {0}'.format(self.connection.ops.quote_name(table_name)))
        rows = list(cursor.fetchall())
        multicol_indexes = set()
        for row in rows:
            if row[3] > 1:
                multicol_indexes.add(row[2])

        indexes = {}
        for row in rows:
            if row[2] in multicol_indexes:
                pass
            else:
                if row[4] not in indexes:
                    indexes[row[4]] = {'primary_key':False, 
                     'unique':False}
                if row[2] == 'PRIMARY':
                    indexes[row[4]]['primary_key'] = True
                if not row[1]:
                    indexes[row[4]]['unique'] = True

        return indexes

    def get_primary_key_column(self, cursor, table_name):
        """
        Returns the name of the primary key column for the given table
        """
        for column in self.get_indexes(cursor, table_name).items():
            if column[1]['primary_key']:
                return column[0]

    def get_storage_engine(self, cursor, table_name):
        """
        Retrieves the storage engine for a given table. Returns the default
        storage engine if the table doesn't exist.
        """
        cursor.execute('SELECT engine FROM information_schema.tables WHERE table_name = %s', [
         table_name])
        result = cursor.fetchone()
        if not result:
            return self.connection.features.mysql_storage_engine
        else:
            return result[0]

    def get_constraints(self, cursor, table_name):
        """
        Retrieves any constraints or keys (unique, pk, fk, check, index) across
        one or more columns.
        """
        constraints = {}
        name_query = 'SELECT kc.`constraint_name`, kc.`column_name`, kc.`referenced_table_name`, kc.`referenced_column_name` FROM information_schema.key_column_usage AS kc WHERE kc.table_schema = %s AND kc.table_name = %s'
        cursor.execute(name_query, [self.connection.settings_dict['NAME'],
         table_name])
        for constraint, column, ref_table, ref_column in cursor.fetchall():
            if constraint not in constraints:
                constraints[constraint] = {'columns':OrderedSet(),  'primary_key':False, 
                 'unique':False, 
                 'index':False, 
                 'check':False, 
                 'foreign_key':(ref_table, ref_column) if ref_column else None}
            constraints[constraint]['columns'].add(column)

        type_query = '\n            SELECT c.constraint_name, c.constraint_type\n            FROM information_schema.table_constraints AS c\n            WHERE\n                c.table_schema = %s AND\n                c.table_name = %s\n        '
        cursor.execute(type_query, [self.connection.settings_dict['NAME'],
         table_name])
        for constraint, kind in cursor.fetchall():
            if kind.lower() == 'primary key':
                constraints[constraint]['primary_key'] = True
                constraints[constraint]['unique'] = True
            else:
                if kind.lower() == 'unique':
                    constraints[constraint]['unique'] = True

        cursor.execute('SHOW INDEX FROM %s' % self.connection.ops.quote_name(table_name))
        for table, non_unique, index, colseq, column in [x[:5] for x in cursor.fetchall()]:
            if index not in constraints:
                constraints[index] = {'columns':OrderedSet(),  'primary_key':False, 
                 'unique':False, 
                 'index':True, 
                 'check':False, 
                 'foreign_key':None}
            constraints[index]['index'] = True
            constraints[index]['columns'].add(column)

        for constraint in constraints.values():
            constraint['columns'] = list(constraint['columns'])

        return constraints