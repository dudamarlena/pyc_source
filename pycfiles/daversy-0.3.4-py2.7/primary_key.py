# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\daversy\db\oracle\primary_key.py
# Compiled at: 2016-01-14 15:12:15
from daversy.utils import *
from daversy.db.object import PrimaryKey, PrimaryKeyColumn

class PrimaryKeyColumnBuilder(object):
    """ Represents a builder for a column in a primary key. """
    DbClass = PrimaryKeyColumn
    XmlTag = 'constraint-column'
    PropertyList = odict((
     'COLUMN_NAME', Property('name')), (
     'CONSTRAINT_NAME', Property('key-name', exclude=True)), (
     'TABLE_NAME', Property('table-name', exclude=True)), (
     'POSITION', Property('position', exclude=True)))
    Query = "\n        SELECT cols.column_name, c.constraint_name, c.table_name, cols.position\n        FROM   sys.user_constraints c, sys.user_cons_columns cols\n        WHERE  c.constraint_name = cols.constraint_name\n        AND    c.constraint_type = 'P'\n        ORDER BY c.constraint_name, cols.position\n    "

    @staticmethod
    def addToState(state, column):
        table = state.tables.get(column['table-name'])
        if table:
            key = table.primary_keys.get(column['key-name'])
            if key:
                key.columns[column.name] = column


class PrimaryKeyBuilder(object):
    """ Represents a builder for a primary key. """
    DbClass = PrimaryKey
    XmlTag = 'primary-key'
    Query = '\n        SELECT c.constraint_name AS name, c.table_name,\n               DECODE(c.deferrable, \'DEFERRABLE\', lower(c.deferred)) AS defer_type,\n               DECODE(i.compression, \'ENABLED\', i.prefix_length) AS "COMPRESS"\n        FROM   sys.user_constraints c\n        LEFT JOIN sys.user_indexes i ON c.index_name = i.index_name\n        WHERE  c.constraint_type = \'P\'\n        ORDER BY c.constraint_name\n    '
    PropertyList = odict((
     'NAME', Property('name')), (
     'DEFER_TYPE', Property('defer-type')), (
     'COMPRESS', Property('compress')), (
     'TABLE_NAME', Property('table-name', exclude=True)))

    @staticmethod
    def addToState(state, key):
        table = state.tables.get(key['table-name'])
        if table:
            table.primary_keys[key.name] = key

    @staticmethod
    def sql(key):
        definition = 'CONSTRAINT %(name)s PRIMARY KEY ( %(columns)s )'
        if key['defer-type']:
            definition += ' DEFERRABLE INITIALLY %(defer-type)s'
        columns = (', ').join([ column.name for column in key.columns.values() ])
        return render(definition, key, columns=columns)