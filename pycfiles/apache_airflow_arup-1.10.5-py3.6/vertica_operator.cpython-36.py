# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/vertica_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1929 bytes
from airflow.contrib.hooks.vertica_hook import VerticaHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class VerticaOperator(BaseOperator):
    __doc__ = "\n    Executes sql code in a specific Vertica database\n\n    :param vertica_conn_id: reference to a specific Vertica database\n    :type vertica_conn_id: str\n    :param sql: the sql code to be executed. (templated)\n    :type sql: Can receive a str representing a sql statement,\n        a list of str (sql statements), or reference to a template file.\n        Template reference are recognized by str ending in '.sql'\n    "
    template_fields = ('sql', )
    template_ext = ('.sql', )
    ui_color = '#b4e0ff'

    @apply_defaults
    def __init__(self, sql, vertica_conn_id='vertica_default', *args, **kwargs):
        (super(VerticaOperator, self).__init__)(*args, **kwargs)
        self.vertica_conn_id = vertica_conn_id
        self.sql = sql

    def execute(self, context):
        self.log.info('Executing: %s', self.sql)
        hook = VerticaHook(vertica_conn_id=(self.vertica_conn_id))
        hook.run(sql=(self.sql))