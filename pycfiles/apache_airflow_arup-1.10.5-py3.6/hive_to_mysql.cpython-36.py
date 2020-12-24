# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
    __doc__ = "\n    Moves data from Hive to MySQL, note that for now the data is loaded\n    into memory before being pushed to MySQL, so this operator should\n    be used for smallish amount of data.\n\n    :param sql: SQL query to execute against Hive server. (templated)\n    :type sql: str\n    :param mysql_table: target MySQL table, use dot notation to target a\n        specific database. (templated)\n    :type mysql_table: str\n    :param mysql_conn_id: source mysql connection\n    :type mysql_conn_id: str\n    :param hiveserver2_conn_id: destination hive connection\n    :type hiveserver2_conn_id: str\n    :param mysql_preoperator: sql statement to run against mysql prior to\n        import, typically use to truncate of delete in place\n        of the data coming in, allowing the task to be idempotent (running\n        the task twice won't double load data). (templated)\n    :type mysql_preoperator: str\n    :param mysql_postoperator: sql statement to run against mysql after the\n        import, typically used to move data from staging to\n        production and issue cleanup commands. (templated)\n    :type mysql_postoperator: str\n    :param bulk_load: flag to use bulk_load option.  This loads mysql directly\n        from a tab-delimited text file using the LOAD DATA LOCAL INFILE command.\n        This option requires an extra connection parameter for the\n        destination MySQL connection: {'local_infile': true}.\n    :type bulk_load: bool\n    "
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