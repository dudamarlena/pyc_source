# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/mssql_to_hive.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 5366 bytes
from builtins import chr
from collections import OrderedDict
import unicodecsv as csv
from tempfile import NamedTemporaryFile
import pymssql
from airflow.hooks.hive_hooks import HiveCliHook
from airflow.hooks.mssql_hook import MsSqlHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class MsSqlToHiveTransfer(BaseOperator):
    """MsSqlToHiveTransfer"""
    template_fields = ('sql', 'partition', 'hive_table')
    template_ext = ('.sql', )
    ui_color = '#a0e08c'

    @apply_defaults
    def __init__(self, sql, hive_table, create=True, recreate=False, partition=None, delimiter=chr(1), mssql_conn_id='mssql_default', hive_cli_conn_id='hive_cli_default', tblproperties=None, *args, **kwargs):
        (super(MsSqlToHiveTransfer, self).__init__)(*args, **kwargs)
        self.sql = sql
        self.hive_table = hive_table
        self.partition = partition
        self.create = create
        self.recreate = recreate
        self.delimiter = delimiter
        self.mssql_conn_id = mssql_conn_id
        self.hive_cli_conn_id = hive_cli_conn_id
        self.partition = partition or {}
        self.tblproperties = tblproperties

    @classmethod
    def type_map(cls, mssql_type):
        t = pymssql
        d = {t.BINARY.value: 'INT', 
         t.DECIMAL.value: 'FLOAT', 
         t.NUMBER.value: 'INT'}
        if mssql_type in d:
            return d[mssql_type]
        else:
            return 'STRING'

    def execute(self, context):
        hive = HiveCliHook(hive_cli_conn_id=(self.hive_cli_conn_id))
        mssql = MsSqlHook(mssql_conn_id=(self.mssql_conn_id))
        self.log.info('Dumping Microsoft SQL Server query results to local file')
        conn = mssql.get_conn()
        cursor = conn.cursor()
        cursor.execute(self.sql)
        with NamedTemporaryFile('w') as (f):
            csv_writer = csv.writer(f, delimiter=(self.delimiter), encoding='utf-8')
            field_dict = OrderedDict()
            col_count = 0
            for field in cursor.description:
                col_count += 1
                col_position = 'Column{position}'.format(position=col_count)
                field_dict[col_position if field[0] == '' else field[0]] = self.type_map(field[1])

            csv_writer.writerows(cursor)
            f.flush()
            cursor.close()
            conn.close()
            self.log.info('Loading file into Hive')
            hive.load_file((f.name),
              (self.hive_table),
              field_dict=field_dict,
              create=(self.create),
              partition=(self.partition),
              delimiter=(self.delimiter),
              recreate=(self.recreate),
              tblproperties=(self.tblproperties))