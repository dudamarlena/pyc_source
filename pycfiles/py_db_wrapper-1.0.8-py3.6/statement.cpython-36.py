# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/py_db_wrapper/sql/statement.py
# Compiled at: 2019-04-17 10:46:58
# Size of source mod 2**32: 2609 bytes
from py_db_wrapper.exceptions import STATEMENT_EXCEPTION

class Statement:
    TEMPLATE = ''

    def __init__(self, dialect):
        self.dialect = dialect

    def add_ticks_and_brackets(self, string):
        if self.dialect.brackets:
            if not self.dialect.ticks:
                return '[{}]'.format(string)
            if self.dialect.ticks:
                if not self.dialect.brackets:
                    return '`{}`'.format(string)
        else:
            if self.dialect.ticks:
                if self.dialect.brackets:
                    return '[`{}`]'.format(string)
        return string

    def build_sql(self, **kwargs):
        return (self.TEMPLATE.format)(**kwargs)


class CreateTableStatement(Statement):
    TEMPLATE = 'CREATE TABLE {schema}.{table} ({columns})'

    def __init__(self, dialect, columns=None):
        """
        kwargs:-
            columns. A tuple list like [(string, SqlType), (string, SqlType)]
        """
        super().__init__(dialect)
        self.columns = columns

    def process_columns(self):
        vals = ['{} {}'.format(self.add_ticks_and_brackets(name), sql_type.sql_string(self.dialect)) for name, sql_type in self.columns]
        return ', '.join(vals)

    def get_sql(self, schema, table):
        if self.columns:
            columns = self.process_columns()
            schema = self.add_ticks_and_brackets(schema)
            table = self.add_ticks_and_brackets(table)
            return self.build_sql(schema=schema, table=table, columns=columns)
        raise STATEMENT_EXCEPTION


class DescribeStatement(Statement):
    TEMPLATE = 'DESCRIBE {optional} {schema}.{table}'

    def __init__(self, dialect, optional=''):
        """
        kwargs:-
            columns. A tuple list like [(string, SqlType), (string, SqlType)]
        """
        super().__init__(dialect)
        self.optional = optional

    def get_sql(self, schema, table):
        schema = self.add_ticks_and_brackets(schema)
        table = self.add_ticks_and_brackets(table)
        return self.build_sql(optional=(self.optional), schema=schema, table=table)


class ShowTablesStatement(Statement):
    TEMPLATE = 'SHOW TABLES IN {schema}'

    def __init__(self, dialect, optional=''):
        """
        kwargs:-
            columns. A tuple list like [(string, SqlType), (string, SqlType)]
        """
        super().__init__(dialect)
        self.optional = optional

    def get_sql(self, schema):
        schema = self.add_ticks_and_brackets(schema)
        return self.build_sql(schema=schema)