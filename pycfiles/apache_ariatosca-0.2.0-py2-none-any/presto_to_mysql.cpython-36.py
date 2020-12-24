# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/presto_to_mysql.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3152 bytes
from airflow.hooks.presto_hook import PrestoHook
from airflow.hooks.mysql_hook import MySqlHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class PrestoToMySqlTransfer(BaseOperator):
    """PrestoToMySqlTransfer"""
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