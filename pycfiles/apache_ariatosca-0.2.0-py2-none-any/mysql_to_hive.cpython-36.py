# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/mysql_to_hive.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 5432 bytes
from builtins import chr
from collections import OrderedDict
import unicodecsv as csv
from tempfile import NamedTemporaryFile
import MySQLdb
from airflow.hooks.hive_hooks import HiveCliHook
from airflow.hooks.mysql_hook import MySqlHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class MySqlToHiveTransfer(BaseOperator):
    """MySqlToHiveTransfer"""
    template_fields = ('sql', 'partition', 'hive_table')
    template_ext = ('.sql', )
    ui_color = '#a0e08c'

    @apply_defaults
    def __init__(self, sql, hive_table, create=True, recreate=False, partition=None, delimiter=chr(1), mysql_conn_id='mysql_default', hive_cli_conn_id='hive_cli_default', tblproperties=None, *args, **kwargs):
        (super(MySqlToHiveTransfer, self).__init__)(*args, **kwargs)
        self.sql = sql
        self.hive_table = hive_table
        self.partition = partition
        self.create = create
        self.recreate = recreate
        self.delimiter = str(delimiter)
        self.mysql_conn_id = mysql_conn_id
        self.hive_cli_conn_id = hive_cli_conn_id
        self.partition = partition or {}
        self.tblproperties = tblproperties

    @classmethod
    def type_map(cls, mysql_type):
        t = MySQLdb.constants.FIELD_TYPE
        d = {t.BIT: 'INT', 
         t.DECIMAL: 'DOUBLE', 
         t.NEWDECIMAL: 'DOUBLE', 
         t.DOUBLE: 'DOUBLE', 
         t.FLOAT: 'DOUBLE', 
         t.INT24: 'INT', 
         t.LONG: 'BIGINT', 
         t.LONGLONG: 'DECIMAL(38,0)', 
         t.SHORT: 'INT', 
         t.TINY: 'SMALLINT', 
         t.YEAR: 'INT', 
         t.TIMESTAMP: 'TIMESTAMP'}
        if mysql_type in d:
            return d[mysql_type]
        else:
            return 'STRING'

    def execute(self, context):
        hive = HiveCliHook(hive_cli_conn_id=(self.hive_cli_conn_id))
        mysql = MySqlHook(mysql_conn_id=(self.mysql_conn_id))
        self.log.info('Dumping MySQL query results to local file')
        conn = mysql.get_conn()
        cursor = conn.cursor()
        cursor.execute(self.sql)
        with NamedTemporaryFile('wb') as (f):
            csv_writer = csv.writer(f, delimiter=(self.delimiter), encoding='utf-8')
            field_dict = OrderedDict()
            for field in cursor.description:
                field_dict[field[0]] = self.type_map(field[1])

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