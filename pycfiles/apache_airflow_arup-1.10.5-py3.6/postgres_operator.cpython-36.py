# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/postgres_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2696 bytes
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class PostgresOperator(BaseOperator):
    __doc__ = "\n    Executes sql code in a specific Postgres database\n\n    :param sql: the sql code to be executed. (templated)\n    :type sql: Can receive a str representing a sql statement,\n        a list of str (sql statements), or reference to a template file.\n        Template reference are recognized by str ending in '.sql'\n    :param postgres_conn_id: reference to a specific postgres database\n    :type postgres_conn_id: str\n    :param autocommit: if True, each command is automatically committed.\n        (default value: False)\n    :type autocommit: bool\n    :param parameters: (optional) the parameters to render the SQL query with.\n    :type parameters: mapping or iterable\n    :param database: name of database which overwrite defined one in connection\n    :type database: str\n    "
    template_fields = ('sql', )
    template_ext = ('.sql', )
    ui_color = '#ededed'

    @apply_defaults
    def __init__(self, sql, postgres_conn_id='postgres_default', autocommit=False, parameters=None, database=None, *args, **kwargs):
        (super(PostgresOperator, self).__init__)(*args, **kwargs)
        self.sql = sql
        self.postgres_conn_id = postgres_conn_id
        self.autocommit = autocommit
        self.parameters = parameters
        self.database = database

    def execute(self, context):
        self.log.info('Executing: %s', self.sql)
        self.hook = PostgresHook(postgres_conn_id=(self.postgres_conn_id), schema=(self.database))
        self.hook.run((self.sql), (self.autocommit), parameters=(self.parameters))
        for output in self.hook.conn.notices:
            self.log.info(output)