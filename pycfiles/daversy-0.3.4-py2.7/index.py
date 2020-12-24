# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\daversy\db\oracle\index.py
# Compiled at: 2016-01-14 15:12:15
from daversy.utils import *
from daversy.db.object import Index, IndexColumn

class IndexColumnBuilder(object):
    """ Represents a builder for a column in an index. """
    DbClass = IndexColumn
    XmlTag = 'index-column'
    Query = '\n        SELECT c.column_name, lower(c.descend) AS sort, i.index_name,\n               i.table_name, c.column_position AS position,\n               e.column_expression AS expression\n        FROM   sys.user_indexes i, sys.user_ind_columns c,\n               sys.user_ind_expressions e\n        WHERE  i.index_name = c.index_name\n        AND    i.table_name = c.table_name\n        AND    c.index_name = e.index_name (+)\n        AND    c.column_position = e.column_position (+)\n        ORDER BY i.index_name, c.column_position\n    '
    PropertyList = odict((
     'COLUMN_NAME', Property('name')), (
     'SORT', Property('sort')), (
     'EXPRESSION', Property('expression', exclude=True)), (
     'INDEX_NAME', Property('index-name', exclude=True)), (
     'TABLE_NAME', Property('table-name', exclude=True)), (
     'POSITION', Property('position', exclude=True)))

    @staticmethod
    def addToState(state, column):
        table = state.tables.get(column['table-name'])
        real = table and table.columns.get(column.name)
        if column.expression and not real:
            column.name = column.expression
        index = state.indexes.get(column['index-name'])
        if index:
            index.columns[column.name] = column


class IndexBuilder(object):
    """ Represents a builder for a index on a table. """
    DbClass = Index
    XmlTag = 'index'
    Query = '\n        SELECT i.index_name, i.table_name,\n               decode(i.uniqueness, \'UNIQUE\', \'true\', \'false\') AS is_unique,\n               decode(i.index_type, \'BITMAP\', \'true\')          AS is_bitmap,\n               DECODE(i.compression, \'ENABLED\', i.prefix_length) AS "COMPRESS"\n        FROM   sys.user_indexes i\n        WHERE  i.index_type IN (\'NORMAL\', \'FUNCTION-BASED NORMAL\', \'BITMAP\')\n        ORDER BY i.index_name\n    '
    PropertyList = odict((
     'INDEX_NAME', Property('name')), (
     'IS_UNIQUE', Property('unique')), (
     'IS_BITMAP', Property('bitmap')), (
     'TABLE_NAME', Property('table-name')), (
     'COMPRESS', Property('compress')))

    @staticmethod
    def addToState(state, index):
        table = state.tables.get(index['table-name'])
        if table:
            if table.primary_keys.has_key(index.name) or table.unique_keys.has_key(index.name):
                return
            state.indexes[index.name] = index

    @staticmethod
    def createSQL(index):
        sql = 'CREATE %(unique)s %(bitmap)s INDEX %(name)s ON %(table-name)s (\n  %(column_sql)s\n)%(suffix)s\n/\n'
        column_def = [ '%(name)-30s %(sort)s' % column for column in index.columns.values()
                     ]
        column_sql = (',\n  ').join(column_def)
        unique = index.unique == 'true' and 'UNIQUE' or ''
        bitmap = index.bitmap == 'true' and 'BITMAP' or ''
        suffix = ''
        if index.compress:
            suffix = ' COMPRESS ' + index.compress
        return render(sql, index, unique=unique, bitmap=bitmap, suffix=suffix, column_sql=column_sql)