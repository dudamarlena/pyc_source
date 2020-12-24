# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/mssql_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2437 bytes
from airflow.hooks.mssql_hook import MsSqlHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class MsSqlOperator(BaseOperator):
    __doc__ = '\n    Executes sql code in a specific Microsoft SQL database\n\n    :param sql: the sql code to be executed\n    :type sql: str or string pointing to a template file with .sql\n        extension. (templated)\n    :param mssql_conn_id: reference to a specific mssql database\n    :type mssql_conn_id: str\n    :param parameters: (optional) the parameters to render the SQL query with.\n    :type parameters: mapping or iterable\n    :param autocommit: if True, each command is automatically committed.\n        (default value: False)\n    :type autocommit: bool\n    :param database: name of database which overwrite defined one in connection\n    :type database: str\n    '
    template_fields = ('sql', )
    template_ext = ('.sql', )
    ui_color = '#ededed'

    @apply_defaults
    def __init__(self, sql, mssql_conn_id='mssql_default', parameters=None, autocommit=False, database=None, *args, **kwargs):
        (super(MsSqlOperator, self).__init__)(*args, **kwargs)
        self.mssql_conn_id = mssql_conn_id
        self.sql = sql
        self.parameters = parameters
        self.autocommit = autocommit
        self.database = database

    def execute(self, context):
        self.log.info('Executing: %s', self.sql)
        hook = MsSqlHook(mssql_conn_id=(self.mssql_conn_id), schema=(self.database))
        hook.run((self.sql), autocommit=(self.autocommit), parameters=(self.parameters))