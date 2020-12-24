# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/yash/Desktop/django-query-profiler/tests/unit/test_sql_statement_type_from_sql.py
# Compiled at: 2020-01-01 01:31:22
# Size of source mod 2**32: 1515 bytes
from unittest.case import TestCase
from django_query_profiler.query_profiler_storage import SqlStatement

class SqlStatementFromSqlTest(TestCase):
    __doc__ = ' Tests for checking if we are able to derive the correct sql statement type, from a sql statement '

    def test_select(self):
        query = 'SELECT * FROM table'
        sql_statement = SqlStatement.from_sql(query)
        self.assertEqual(sql_statement, SqlStatement.SELECT)

    def test_insert(self):
        query = 'INSERT INTO table values(1, 2)'
        sql_statement = SqlStatement.from_sql(query)
        self.assertEqual(sql_statement, SqlStatement.INSERT)

    def test_update(self):
        query = 'update table set a=1 WHERE id=5'
        sql_statement = SqlStatement.from_sql(query)
        self.assertEqual(sql_statement, SqlStatement.UPDATE)

    def test_delete(self):
        query = 'DELEte FROM table WHERE id=5'
        sql_statement = SqlStatement.from_sql(query)
        self.assertEqual(sql_statement, SqlStatement.DELETE)

    def test_begin(self):
        query = 'BEGIN'
        sql_statement = SqlStatement.from_sql(query)
        self.assertEqual(sql_statement, SqlStatement.TRANSACTIONALS)

    def test_end(self):
        query = 'END'
        sql_statement = SqlStatement.from_sql(query)
        self.assertEqual(sql_statement, SqlStatement.TRANSACTIONALS)

    def test_other(self):
        query = 'END2'
        sql_statement = SqlStatement.from_sql(query)
        self.assertEqual(sql_statement, SqlStatement.OTHER)