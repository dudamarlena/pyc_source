# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\sqlbase7_sa\sqlbase7_sa05.py
# Compiled at: 2010-05-27 13:57:37
from sqlalchemy import types, Column, PrimaryKeyConstraint
from sqlalchemy.sql.compiler import OPERATORS
from sqlalchemy.sql import operators as sql_operators
from sqlbase7_sa.sqlbase7 import SQLBase7Compiler, SQLBase7Dialect

class SQLBase7Compiler_SA05(SQLBase7Compiler):
    operators = SQLBase7Compiler.operators.copy()
    operators.update({sql_operators.ilike_op: lambda x, y, escape=None: '@lower(%s) LIKE @lower(%s)' % (x, y) + (escape and " ESCAPE '%s'" % escape or '')})


class SQLBase7Dialect_SA05(SQLBase7Dialect):
    statement_compiler = SQLBase7Compiler_SA05

    @classmethod
    def dbapi(cls):
        import pyodbc
        return pyodbc

    def table_names(self, connection, schema):
        cursor = connection.connection.cursor()
        table_names = [ row.NAME for row in cursor.execute('SELECT NAME FROM %s.SYSTABLES WHERE REMARKS IS NOT NULL' % schema)
                      ]
        cursor.close()
        return table_names

    def reflecttable(self, connection, table, include_columns=None):
        if table.schema is None:
            table.schema = connection.default_schema_name()
        sql = "SELECT NAME,COLTYPE,NULLS FROM %s.SYSCOLUMNS WHERE TBNAME = '%s'" % (table.schema, table.name)
        if include_columns:
            sql += ' AND NAME NOT IN (%s)' % (',').join(include_columns)
        cursor = connection.connection.cursor()
        for row in cursor.execute(sql):
            table.append_column(Column(row.NAME, self._type_map[row.COLTYPE]))

        cursor.close()
        cursor = connection.connection.cursor()
        key_columns = [ row.COLNAME for row in cursor.execute("SELECT COLNAME FROM %s.SYSPKCONSTRAINTS WHERE NAME = '%s' ORDER BY PKCOLSEQNUM" % (table.schema, table.name))
                      ]
        if key_columns:
            table.append_constraint(PrimaryKeyConstraint(*key_columns))
        cursor.close()
        return