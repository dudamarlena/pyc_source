# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/presto_to_mysql.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3152 bytes
from airflow.hooks.presto_hook import PrestoHook
from airflow.hooks.mysql_hook import MySqlHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class PrestoToMySqlTransfer(BaseOperator):
    __doc__ = "\n    Moves data from Presto to MySQL, note that for now the data is loaded\n    into memory before being pushed to MySQL, so this operator should\n    be used for smallish amount of data.\n\n    :param sql: SQL query to execute against Presto. (templated)\n    :type sql: str\n    :param mysql_table: target MySQL table, use dot notation to target a\n        specific database. (templated)\n    :type mysql_table: str\n    :param mysql_conn_id: source mysql connection\n    :type mysql_conn_id: str\n    :param presto_conn_id: source presto connection\n    :type presto_conn_id: str\n    :param mysql_preoperator: sql statement to run against mysql prior to\n        import, typically use to truncate of delete in place\n        of the data coming in, allowing the task to be idempotent (running\n        the task twice won't double load data). (templated)\n    :type mysql_preoperator: str\n    "
    template_fields = ('sql', 'mysql_table', 'mysql_preoperator')
    template_ext = ('.sql', )
    ui_color = '#a0e08c'

    @apply_defaults
    def __init__(self, sql, mysql_table, presto_conn_id='presto_default', mysql_conn_id='mysql_default', mysql_preoperator=None, *args, **kwargs):
        (super(PrestoToMySqlTransfer, self).__init__)(*args, **kwargs)
        self.sql = sql
        self.mysql_table = mysql_table
        self.mysql_conn_id = mysql_conn_id
        self.mysql_preoperator = mysql_preoperator
        self.presto_conn_id = presto_conn_id

    def execute(self, context):
        presto = PrestoHook(presto_conn_id=(self.presto_conn_id))
        self.log.info('Extracting data from Presto: %s', self.sql)
        results = presto.get_records(self.sql)
        mysql = MySqlHook(mysql_conn_id=(self.mysql_conn_id))
        if self.mysql_preoperator:
            self.log.info('Running MySQL preoperator')
            self.log.info(self.mysql_preoperator)
            mysql.run(self.mysql_preoperator)
        self.log.info('Inserting rows into MySQL')
        mysql.insert_rows(table=(self.mysql_table), rows=results)