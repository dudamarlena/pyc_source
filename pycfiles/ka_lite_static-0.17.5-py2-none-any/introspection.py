# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/db/backends/sqlite3/introspection.py
# Compiled at: 2018-07-11 18:15:30
import re
from django.db.backends import BaseDatabaseIntrospection
field_size_re = re.compile('^\\s*(?:var)?char\\s*\\(\\s*(\\d+)\\s*\\)\\s*$')

def get_field_size(name):
    """ Extract the size number from a "varchar(11)" type name """
    m = field_size_re.search(name)
    if m:
        return int(m.group(1))
    else:
        return


class FlexibleFieldLookupDict(object):
    base_data_types_reverse = {'bool': 'BooleanField', 
       'boolean': 'BooleanField', 
       'smallint': 'SmallIntegerField', 
       'smallint unsigned': 'PositiveSmallIntegerField', 
       'smallinteger': 'SmallIntegerField', 
       'int': 'IntegerField', 
       'integer': 'IntegerField', 
       'bigint': 'BigIntegerField', 
       'integer unsigned': 'PositiveIntegerField', 
       'decimal': 'DecimalField', 
       'real': 'FloatField', 
       'text': 'TextField', 
       'char': 'CharField', 
       'date': 'DateField', 
       'datetime': 'DateTimeField', 
       'time': 'TimeField'}

    def __getitem__(self, key):
        key = key.lower()
        try:
            return self.base_data_types_reverse[key]
        except KeyError:
            size = get_field_size(key)
            if size is not None:
                return ('CharField', {'max_length': size})
            raise KeyError

        return


class DatabaseIntrospection(BaseDatabaseIntrospection):
    data_types_reverse = FlexibleFieldLookupDict()

    def get_table_list(self, cursor):
        """Returns a list of table names in the current database."""
        cursor.execute("\n            SELECT name FROM sqlite_master\n            WHERE type='table' AND NOT name='sqlite_sequence'\n            ORDER BY name")
        return [ row[0] for row in cursor.fetchall() ]

    def get_table_description(self, cursor, table_name):
        """Returns a description of the table, with the DB-API cursor.description interface."""
        return [ (info['name'], info['type'], None, info['size'], None, None, info['null_ok']) for info in self._table_info(cursor, table_name)
               ]

    def get_relations(self, cursor, table_name):
        """
        Returns a dictionary of {field_index: (field_index_other_table, other_table)}
        representing all relationships to the given table. Indexes are 0-based.
        """
        relations = {}
        cursor.execute('SELECT sql FROM sqlite_master WHERE tbl_name = %s AND type = %s', [table_name, 'table'])
        results = cursor.fetchone()[0].strip()
        results = results[results.index('(') + 1:results.rindex(')')]
        for field_index, field_desc in enumerate(results.split(',')):
            field_desc = field_desc.strip()
            if field_desc.startswith('UNIQUE'):
                continue
            m = re.search('references (.*) \\(["|](.*)["|]\\)', field_desc, re.I)
            if not m:
                continue
            table, column = [ s.strip('"') for s in m.groups() ]
            cursor.execute('SELECT sql FROM sqlite_master WHERE tbl_name = %s', [table])
            result = cursor.fetchall()[0]
            other_table_results = result[0].strip()
            li, ri = other_table_results.index('('), other_table_results.rindex(')')
            other_table_results = other_table_results[li + 1:ri]
            for other_index, other_desc in enumerate(other_table_results.split(',')):
                other_desc = other_desc.strip()
                if other_desc.startswith('UNIQUE'):
                    continue
                name = other_desc.split(' ', 1)[0].strip('"')
                if name == column:
                    relations[field_index] = (
                     other_index, table)
                    break

        return relations

    def get_key_columns(self, cursor, table_name):
        """
        Returns a list of (column_name, referenced_table_name, referenced_column_name) for all
        key columns in given table.
        """
        key_columns = []
        cursor.execute('SELECT sql FROM sqlite_master WHERE tbl_name = %s AND type = %s', [table_name, 'table'])
        results = cursor.fetchone()[0].strip()
        results = results[results.index('(') + 1:results.rindex(')')]
        for field_index, field_desc in enumerate(results.split(',')):
            field_desc = field_desc.strip()
            if field_desc.startswith('UNIQUE'):
                continue
            m = re.search('"(.*)".*references (.*) \\(["|](.*)["|]\\)', field_desc, re.I)
            if not m:
                continue
            key_columns.append(tuple([ s.strip('"') for s in m.groups() ]))

        return key_columns

    def get_indexes(self, cursor, table_name):
        indexes = {}
        for info in self._table_info(cursor, table_name):
            if info['pk'] != 0:
                indexes[info['name']] = {'primary_key': True, 'unique': False}

        cursor.execute('PRAGMA index_list(%s)' % self.connection.ops.quote_name(table_name))
        for index, unique in [ (field[1], field[2]) for field in cursor.fetchall() ]:
            cursor.execute('PRAGMA index_info(%s)' % self.connection.ops.quote_name(index))
            info = cursor.fetchall()
            if len(info) != 1:
                continue
            name = info[0][2]
            indexes[name] = {'primary_key': False, 'unique': unique}

        return indexes

    def get_primary_key_column(self, cursor, table_name):
        """
        Get the column name of the primary key for the given table.
        """
        cursor.execute('SELECT sql FROM sqlite_master WHERE tbl_name = %s AND type = %s', [table_name, 'table'])
        results = cursor.fetchone()[0].strip()
        results = results[results.index('(') + 1:results.rindex(')')]
        for field_desc in results.split(','):
            field_desc = field_desc.strip()
            m = re.search('"(.*)".*PRIMARY KEY$', field_desc)
            if m:
                return m.groups()[0]

        return

    def _table_info(self, cursor, name):
        cursor.execute('PRAGMA table_info(%s)' % self.connection.ops.quote_name(name))
        return [ {'name': field[1], 'type': field[2], 'size': get_field_size(field[2]), 'null_ok': not field[3], 'pk': field[5]} for field in cursor.fetchall()
               ]