# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/mysql_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2591 bytes
from airflow.hooks.mysql_hook import MySqlHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class MySqlOperator(BaseOperator):
    __doc__ = "\n    Executes sql code in a specific MySQL database\n\n    :param sql: the sql code to be executed. Can receive a str representing a\n        sql statement, a list of str (sql statements), or reference to a template file.\n        Template reference are recognized by str ending in '.sql'\n        (templated)\n    :type sql: str or list[str]\n    :param mysql_conn_id: reference to a specific mysql database\n    :type mysql_conn_id: str\n    :param parameters: (optional) the parameters to render the SQL query with.\n    :type parameters: mapping or iterable\n    :param autocommit: if True, each command is automatically committed.\n        (default value: False)\n    :type autocommit: bool\n    :param database: name of database which overwrite defined one in connection\n    :type database: str\n    "
    template_fields = ('sql', )
    template_ext = ('.sql', )
    ui_color = '#ededed'

    @apply_defaults
    def __init__(self, sql, mysql_conn_id='mysql_default', parameters=None, autocommit=False, database=None, *args, **kwargs):
        (super(MySqlOperator, self).__init__)(*args, **kwargs)
        self.mysql_conn_id = mysql_conn_id
        self.sql = sql
        self.autocommit = autocommit
        self.parameters = parameters
        self.database = database

    def execute(self, context):
        self.log.info('Executing: %s', self.sql)
        hook = MySqlHook(mysql_conn_id=(self.mysql_conn_id), schema=(self.database))
        hook.run((self.sql),
          autocommit=(self.autocommit),
          parameters=(self.parameters))