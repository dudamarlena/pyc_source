# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/snowflake_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3034 bytes
from airflow.contrib.hooks.snowflake_hook import SnowflakeHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class SnowflakeOperator(BaseOperator):
    __doc__ = "\n    Executes sql code in a Snowflake database\n\n    :param snowflake_conn_id: reference to specific snowflake connection id\n    :type snowflake_conn_id: str\n    :param sql: the sql code to be executed. (templated)\n    :type sql: Can receive a str representing a sql statement,\n        a list of str (sql statements), or reference to a template file.\n        Template reference are recognized by str ending in '.sql'\n    :param warehouse: name of warehouse (will overwrite any warehouse\n        defined in the connection's extra JSON)\n    :type warehouse: str\n    :param database: name of database (will overwrite database defined\n        in connection)\n    :type database: str\n    :param schema: name of schema (will overwrite schema defined in\n        connection)\n    :type schema: str\n    :param role: name of role (will overwrite any role defined in\n        connection's extra JSON)\n    "
    template_fields = ('sql', )
    template_ext = ('.sql', )
    ui_color = '#ededed'

    @apply_defaults
    def __init__(self, sql, snowflake_conn_id='snowflake_default', parameters=None, autocommit=True, warehouse=None, database=None, role=None, schema=None, *args, **kwargs):
        (super(SnowflakeOperator, self).__init__)(*args, **kwargs)
        self.snowflake_conn_id = snowflake_conn_id
        self.sql = sql
        self.autocommit = autocommit
        self.parameters = parameters
        self.warehouse = warehouse
        self.database = database
        self.role = role
        self.schema = schema

    def get_hook(self):
        return SnowflakeHook(snowflake_conn_id=(self.snowflake_conn_id), warehouse=(self.warehouse),
          database=(self.database),
          role=(self.role),
          schema=(self.schema))

    def execute(self, context):
        self.log.info('Executing: %s', self.sql)
        hook = self.get_hook()
        hook.run((self.sql),
          autocommit=(self.autocommit),
          parameters=(self.parameters))