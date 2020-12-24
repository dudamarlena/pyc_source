# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/vertica_to_hive.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 5346 bytes
from builtins import chr
from collections import OrderedDict
import unicodecsv as csv
from tempfile import NamedTemporaryFile
from airflow.hooks.hive_hooks import HiveCliHook
from airflow.contrib.hooks.vertica_hook import VerticaHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class VerticaToHiveTransfer(BaseOperator):
    """VerticaToHiveTransfer"""
    template_fields = ('sql', 'partition', 'hive_table')
    template_ext = ('.sql', )
    ui_color = '#b4e0ff'

    @apply_defaults
    def __init__(self, sql, hive_table, create=True, recreate=False, partition=None, delimiter=chr(1), vertica_conn_id='vertica_default', hive_cli_conn_id='hive_cli_default', *args, **kwargs):
        (super(VerticaToHiveTransfer, self).__init__)(*args, **kwargs)
        self.sql = sql
        self.hive_table = hive_table
        self.partition = partition
        self.create = create
        self.recreate = recreate
        self.delimiter = str(delimiter)
        self.vertica_conn_id = vertica_conn_id
        self.hive_cli_conn_id = hive_cli_conn_id
        self.partition = partition or {}

    @classmethod
    def type_map(cls, vertica_type):
        d = {5:'BOOLEAN', 
         6:'INT', 
         7:'FLOAT', 
         8:'STRING', 
         9:'STRING', 
         16:'FLOAT'}
        if vertica_type in d:
            return d[vertica_type]
        else:
            return 'STRING'

    def execute(self, context):
        hive = HiveCliHook(hive_cli_conn_id=(self.hive_cli_conn_id))
        vertica = VerticaHook(vertica_conn_id=(self.vertica_conn_id))
        self.log.info('Dumping Vertica query results to local file')
        conn = vertica.get_conn()
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

            csv_writer.writerows(cursor.iterate())
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
              recreate=(self.recreate))