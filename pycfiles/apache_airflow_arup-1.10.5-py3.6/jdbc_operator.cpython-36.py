# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/jdbc_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2355 bytes
from airflow.hooks.jdbc_hook import JdbcHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class JdbcOperator(BaseOperator):
    __doc__ = "\n    Executes sql code in a database using jdbc driver.\n\n    Requires jaydebeapi.\n\n    :param sql: the sql code to be executed. (templated)\n    :type sql: Can receive a str representing a sql statement,\n        a list of str (sql statements), or reference to a template file.\n        Template reference are recognized by str ending in '.sql'\n    :param jdbc_conn_id: reference to a predefined database\n    :type jdbc_conn_id: str\n    :param autocommit: if True, each command is automatically committed.\n        (default value: False)\n    :type autocommit: bool\n    :param parameters: (optional) the parameters to render the SQL query with.\n    :type parameters: mapping or iterable\n    "
    template_fields = ('sql', )
    template_ext = ('.sql', )
    ui_color = '#ededed'

    @apply_defaults
    def __init__(self, sql, jdbc_conn_id='jdbc_default', autocommit=False, parameters=None, *args, **kwargs):
        (super(JdbcOperator, self).__init__)(*args, **kwargs)
        self.parameters = parameters
        self.sql = sql
        self.jdbc_conn_id = jdbc_conn_id
        self.autocommit = autocommit

    def execute(self, context):
        self.log.info('Executing: %s', self.sql)
        self.hook = JdbcHook(jdbc_conn_id=(self.jdbc_conn_id))
        self.hook.run((self.sql), (self.autocommit), parameters=(self.parameters))