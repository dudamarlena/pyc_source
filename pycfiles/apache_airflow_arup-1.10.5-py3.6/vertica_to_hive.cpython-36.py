# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
    __doc__ = "\n    Moves data from Vertia to Hive. The operator runs\n    your query against Vertia, stores the file locally\n    before loading it into a Hive table. If the ``create`` or\n    ``recreate`` arguments are set to ``True``,\n    a ``CREATE TABLE`` and ``DROP TABLE`` statements are generated.\n    Hive data types are inferred from the cursor's metadata.\n    Note that the table generated in Hive uses ``STORED AS textfile``\n    which isn't the most efficient serialization format. If a\n    large amount of data is loaded and/or if the table gets\n    queried considerably, you may want to use this operator only to\n    stage the data into a temporary table before loading it into its\n    final destination using a ``HiveOperator``.\n\n    :param sql: SQL query to execute against the Vertia database. (templated)\n    :type sql: str\n    :param hive_table: target Hive table, use dot notation to target a\n        specific database. (templated)\n    :type hive_table: str\n    :param create: whether to create the table if it doesn't exist\n    :type create: bool\n    :param recreate: whether to drop and recreate the table at every execution\n    :type recreate: bool\n    :param partition: target partition as a dict of partition columns\n        and values. (templated)\n    :type partition: dict\n    :param delimiter: field delimiter in the file\n    :type delimiter: str\n    :param vertica_conn_id: source Vertica connection\n    :type vertica_conn_id: str\n    :param hive_conn_id: destination hive connection\n    :type hive_conn_id: str\n\n    "
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