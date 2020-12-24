# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/hive_to_mysql.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4606 bytes
from tempfile import NamedTemporaryFile
from airflow.hooks.hive_hooks import HiveServer2Hook
from airflow.hooks.mysql_hook import MySqlHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.utils.operator_helpers import context_to_airflow_vars

class HiveToMySqlTransfer(BaseOperator):
    """HiveToMySqlTransfer"""
    template_fields = ('sql', 'mysql_table', 'mysql_preoperator', 'mysql_postoperator')
    template_ext = ('.sql', )
    ui_color = '#a0e08c'

    @apply_defaults
    def __init__(self, sql, mysql_table, hiveserver2_conn_id='hiveserver2_default', mysql_conn_id='mysql_default', mysql_preoperator=None, mysql_postoperator=None, bulk_load=False, *args, **kwargs):
        (super(HiveToMySqlTransfer, self).__init__)(*args, **kwargs)
        self.sql = sql
        self.mysql_table = mysql_table
        self.mysql_conn_id = mysql_conn_id
        self.mysql_preoperator = mysql_preoperator
        self.mysql_postoperator = mysql_postoperator
        self.hiveserver2_conn_id = hiveserver2_conn_id
        self.bulk_load = bulk_load

    def execute(self, context):
        hive = HiveServer2Hook(hiveserver2_conn_id=(self.hiveserver2_conn_id))
        self.log.info('Extracting data from Hive: %s', self.sql)
        if self.bulk_load:
            tmpfile = NamedTemporaryFile()
            hive.to_csv((self.sql), (tmpfile.name), delimiter='\t', lineterminator='\n',
              output_header=False,
              hive_conf=(context_to_airflow_vars(context)))
        else:
            results = hive.get_records(self.sql)
        mysql = MySqlHook(mysql_conn_id=(self.mysql_conn_id))
        if self.mysql_preoperator:
            self.log.info('Running MySQL preoperator')
            mysql.run(self.mysql_preoperator)
        else:
            self.log.info('Inserting rows into MySQL')
            if self.bulk_load:
                mysql.bulk_load(table=(self.mysql_table), tmp_file=(tmpfile.name))
                tmpfile.close()
            else:
                mysql.insert_rows(table=(self.mysql_table), rows=results)
        if self.mysql_postoperator:
            self.log.info('Running MySQL postoperator')
            mysql.run(self.mysql_postoperator)
        self.log.info('Done.')