# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\daversy\db\oracle\column.py
# Compiled at: 2016-01-14 15:12:15
from daversy.utils import *
from daversy.db.object import TableColumn, ViewColumn
YESNO_MAPPING = {'Y': 'true', 'N': 'false'}

def correctTimestamps(type):
    """ Timestamps are returned as 'timestamp(6)', while we want it as 'timestamp'"""
    return type.startswith('timestamp') and 'timestamp' or type


class TableColumnBuilder(object):
    """ Represents a builder for a column in a table."""
    DbClass = TableColumn
    XmlTag = 'column'
    PropertyList = odict((
     'COLUMN_NAME', Property('name')), (
     'DATA_TYPE', Property('type', None, correctTimestamps)), (
     'CUSTOM_TYPE', Property('custom-type')), (
     'DATA_LENGTH', Property('length')), (
     'DATA_PRECISION', Property('precision')), (
     'DATA_SCALE', Property('scale')), (
     'NULLABLE', Property('nullable', 'true', lambda flag: YESNO_MAPPING[flag])), (
     'DATA_DEFAULT', Property('default-value')), (
     'COMMENTS', Property('comment')), (
     'DEFER_TYPE', Property('notnull-defer-type')), (
     'CHK', Property('check')), (
     'CHK_DEFER_TYPE', Property('check-defer-type')), (
     'CHAR_SEMANTICS', Property('char-semantics')), (
     'VIRTUAL_COL', Property('virtual')), (
     'PARENT_NAME', Property('parent-name', exclude=True)), (
     'COLUMN_ID', Property('sequence', exclude=True)))
    Query = "\n        SELECT tc.column_name, tc.table_name AS parent_name, tc.column_id,\n               nvl2(tc.data_type_owner, null, lower(tc.data_type)) AS data_type,\n               nvl2(tc.data_type_owner, tc.data_type, null) AS custom_type,\n               nvl2(tc.char_used, tc.char_length, tc.data_length) AS data_length,\n               tc.data_precision, tc.data_scale, tc.nullable, tc.data_default,\n               c.comments, NULL AS defer_type, NULL AS chk, NULL AS chk_defer_type,\n               DECODE(tc.char_used, 'C', 'true') AS char_semantics,\n               DECODE(tc.virtual_column, 'YES', 'true') AS virtual_col\n        FROM   sys.user_tab_cols tc, sys.user_col_comments c\n        WHERE  tc.table_name  = c.table_name\n        AND    tc.column_name = c.column_name\n        AND    tc.data_type_owner IS NULL\n        ORDER BY tc.table_name, tc.column_id\n    "

    @staticmethod
    def addToState(state, column):
        custom_type = column['custom-type']
        if custom_type and not state.types.get(custom_type):
            raise LookupError('Cannot find the type %s' % custom_type)
        table = state.tables.get(column['parent-name'])
        if table:
            column.comment = trim_spaces(column.comment)
            table.columns[column.name] = column

    @staticmethod
    def sql(column):
        if column['custom-type']:
            return '%(name)-30s %(custom-type)s' % column
        if column['virtual']:
            return '%(name)-30s GENERATED ALWAYS AS (%(default-value)s)' % column
        definition = '%(name)-30s %(type)s'
        if column.type in ('number', 'float'):
            if not column.precision and column.scale:
                raise TypeError("Can't specify scale without precision for a column.")
            elif column.precision and not column.scale:
                definition += '(%(precision)s)'
            elif column.precision and column.scale:
                definition += '(%(precision)s, %(scale)s)'
        elif column.type in ('varchar2', 'char'):
            if int(column.length) < 1:
                raise TypeError("%s can't be of zero length." % (type,))
            if column['char-semantics'] == 'true':
                definition += '(%(length)s CHAR)'
            else:
                definition += '(%(length)s BYTE)'
        elif column.type in ('nvarchar2', 'nchar'):
            if int(column.length) < 1:
                raise TypeError("%s can't be of zero length." % (type,))
            definition += '(%(length)s)'
        result = definition % column
        if column['default-value']:
            result += ' default %s' % column['default-value'].strip()
        if column['nullable'] == 'false':
            result += ' not null'
            if column['notnull-defer-type']:
                result += ' deferrable initially ' + column['notnull-defer-type']
        if column.check:
            result += ' check(%s)' % column.check
            if column['check-defer-type']:
                result += ' deferrable initially ' + column['check-defer-type']
        return result

    @staticmethod
    def commentSQL(parent, col):
        if not col.comment:
            return None
        else:
            return "COMMENT ON COLUMN %s.%s IS '%s';" % (parent.name, col.name,
             sql_escape(col.comment))


class ViewColumnBuilder(object):
    """ Represents a builder for a column in a view."""
    DbClass = ViewColumn
    XmlTag = 'column'
    PropertyList = odict((
     'COLUMN_NAME', Property('name')), (
     'COMMENTS', Property('comment')), (
     'PARENT_NAME', Property('parent-name', exclude=True)), (
     'COLUMN_ID', Property('sequence', exclude=True)))
    Query = '\n        SELECT vc.column_name, vc.table_name AS parent_name, vc.column_id,\n               c.comments\n        FROM   sys.user_tab_columns vc, sys.user_col_comments c\n        WHERE  vc.table_name  = c.table_name\n        AND    vc.column_name = c.column_name\n        ORDER BY vc.table_name, vc.column_id\n    '

    @staticmethod
    def addToState(state, column):
        view = state.views.get(column['parent-name'])
        if view:
            column.comment = trim_spaces(column.comment)
            view.columns[column.name] = column

    @staticmethod
    def commentSQL(parent, col):
        if not col.comment:
            return None
        else:
            return "COMMENT ON COLUMN %s.%s IS '%s';" % (parent.name, col.name,
             sql_escape(col.comment))