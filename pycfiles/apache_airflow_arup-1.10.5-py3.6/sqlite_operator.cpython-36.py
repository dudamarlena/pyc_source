# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/sqlite_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2037 bytes
from airflow.hooks.sqlite_hook import SqliteHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class SqliteOperator(BaseOperator):
    __doc__ = "\n    Executes sql code in a specific Sqlite database\n\n    :param sql: the sql code to be executed. (templated)\n    :type sql: str or string pointing to a template file. File must have\n        a '.sql' extensions.\n    :param sqlite_conn_id: reference to a specific sqlite database\n    :type sqlite_conn_id: str\n    :param parameters: (optional) the parameters to render the SQL query with.\n    :type parameters: mapping or iterable\n    "
    template_fields = ('sql', )
    template_ext = ('.sql', )
    ui_color = '#cdaaed'

    @apply_defaults
    def __init__(self, sql, sqlite_conn_id='sqlite_default', parameters=None, *args, **kwargs):
        (super(SqliteOperator, self).__init__)(*args, **kwargs)
        self.sqlite_conn_id = sqlite_conn_id
        self.sql = sql
        self.parameters = parameters or []

    def execute(self, context):
        self.log.info('Executing: %s', self.sql)
        hook = SqliteHook(sqlite_conn_id=(self.sqlite_conn_id))
        hook.run((self.sql), parameters=(self.parameters))