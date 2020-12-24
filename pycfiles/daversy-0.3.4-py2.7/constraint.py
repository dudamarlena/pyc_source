# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\daversy\db\oracle\constraint.py
# Compiled at: 2016-01-14 15:12:15
from daversy.utils import *
from daversy.db.object import CheckConstraint
import re
COL_NOT_NULL = re.compile('^\\s*("?)([\\w$#]+)\\1\\s+IS\\s+NOT\\s+NULL\\s*$', re.I)

class CheckConstraintBuilder(object):
    """ Represents a builder for a check constraint. """
    DbClass = CheckConstraint
    XmlTag = 'check-constraint'
    Query = "\n        WITH cons_cols AS (\n            SELECT owner, constraint_name,\n                   DECODE(COUNT(column_name), 1, MIN(column_name)) AS column_name\n            FROM   sys.user_cons_columns\n            GROUP BY owner, constraint_name\n        )\n        SELECT c.constraint_name, c.search_condition AS condition, c.table_name,\n               DECODE(c.deferrable, 'DEFERRABLE', lower(c.deferred)) AS defer_type,\n               l.column_name, DECODE(c.generated, 'GENERATED NAME', 'true') AS unnamed\n        FROM   sys.user_constraints c, cons_cols l\n        WHERE  c.constraint_type = 'C'\n        AND    c.owner = l.owner AND c.constraint_name = l.constraint_name\n        ORDER BY c.table_name, c.constraint_name\n    "
    PropertyList = odict((
     'CONSTRAINT_NAME', Property('name')), (
     'DEFER_TYPE', Property('defer-type')), (
     'CONDITION', Property('condition', cdata=True)), (
     'TABLE_NAME', Property('table-name', exclude=True)), (
     'COLUMN_NAME', Property('column', exclude=True)), (
     'UNNAMED', Property('unnamed', exclude=True)))

    @staticmethod
    def addToState(state, constraint):
        table = state.tables.get(constraint['table-name'])
        if table:
            if constraint.column and constraint.unnamed:
                column = table.columns.get(constraint.column)
                match = COL_NOT_NULL.match(constraint.condition)
                if match and column.name == match.group(2):
                    if constraint.get('defer-type'):
                        column['nullable'] = 'false'
                        column['notnull-defer-type'] = constraint['defer-type']
                        return
                    if column.nullable == 'false':
                        return
                else:
                    column['check'] = constraint.get('condition')
                    column['check-defer-type'] = constraint.get('defer-type')
                    return
            if constraint.unnamed:
                constraint.name = generated_name(constraint.condition)
            table.constraints[constraint.name] = constraint

    @staticmethod
    def sql(constraint):
        fmt = 'CHECK ( %(condition)s )'
        if not constraint.name.startswith('generated:'):
            fmt = 'CONSTRAINT %(name)s ' + fmt
        if constraint['defer-type']:
            fmt = fmt + ' DEFERRABLE INITIALLY %(defer-type)s'
        return fmt % constraint