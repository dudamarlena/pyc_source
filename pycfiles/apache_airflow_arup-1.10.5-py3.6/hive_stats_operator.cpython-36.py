# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/hive_stats_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 7047 bytes
from builtins import zip
from collections import OrderedDict
import json
from airflow.exceptions import AirflowException
from airflow.hooks.mysql_hook import MySqlHook
from airflow.hooks.presto_hook import PrestoHook
from airflow.hooks.hive_hooks import HiveMetastoreHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class HiveStatsCollectionOperator(BaseOperator):
    __doc__ = '\n    Gathers partition statistics using a dynamically generated Presto\n    query, inserts the stats into a MySql table with this format. Stats\n    overwrite themselves if you rerun the same date/partition. ::\n\n        CREATE TABLE hive_stats (\n            ds VARCHAR(16),\n            table_name VARCHAR(500),\n            metric VARCHAR(200),\n            value BIGINT\n        );\n\n    :param table: the source table, in the format ``database.table_name``. (templated)\n    :type table: str\n    :param partition: the source partition. (templated)\n    :type partition: dict of {col:value}\n    :param extra_exprs: dict of expression to run against the table where\n        keys are metric names and values are Presto compatible expressions\n    :type extra_exprs: dict\n    :param col_blacklist: list of columns to blacklist, consider\n        blacklisting blobs, large json columns, ...\n    :type col_blacklist: list\n    :param assignment_func: a function that receives a column name and\n        a type, and returns a dict of metric names and an Presto expressions.\n        If None is returned, the global defaults are applied. If an\n        empty dictionary is returned, no stats are computed for that\n        column.\n    :type assignment_func: function\n    '
    template_fields = ('table', 'partition', 'ds', 'dttm')
    ui_color = '#aff7a6'

    @apply_defaults
    def __init__(self, table, partition, extra_exprs=None, col_blacklist=None, assignment_func=None, metastore_conn_id='metastore_default', presto_conn_id='presto_default', mysql_conn_id='airflow_db', *args, **kwargs):
        (super(HiveStatsCollectionOperator, self).__init__)(*args, **kwargs)
        self.table = table
        self.partition = partition
        self.extra_exprs = extra_exprs or {}
        self.col_blacklist = col_blacklist or {}
        self.metastore_conn_id = metastore_conn_id
        self.presto_conn_id = presto_conn_id
        self.mysql_conn_id = mysql_conn_id
        self.assignment_func = assignment_func
        self.ds = '{{ ds }}'
        self.dttm = '{{ execution_date.isoformat() }}'

    def get_default_exprs(self, col, col_type):
        if col in self.col_blacklist:
            return {}
        else:
            d = {(
 col, 'non_null'): 'COUNT({col})'}
            if col_type in ('double', 'int', 'bigint', 'float', 'double'):
                d[(col, 'sum')] = 'SUM({col})'
                d[(col, 'min')] = 'MIN({col})'
                d[(col, 'max')] = 'MAX({col})'
                d[(col, 'avg')] = 'AVG({col})'
            else:
                if col_type == 'boolean':
                    d[(col, 'true')] = 'SUM(CASE WHEN {col} THEN 1 ELSE 0 END)'
                    d[(col, 'false')] = 'SUM(CASE WHEN NOT {col} THEN 1 ELSE 0 END)'
                else:
                    if col_type in ('string', ):
                        d[(col, 'len')] = 'SUM(CAST(LENGTH({col}) AS BIGINT))'
                        d[(col, 'approx_distinct')] = 'APPROX_DISTINCT({col})'
            return {k:v.format(col=col) for k, v in d.items()}

    def execute(self, context=None):
        metastore = HiveMetastoreHook(metastore_conn_id=(self.metastore_conn_id))
        table = metastore.get_table(table_name=(self.table))
        field_types = {col.name:col.type for col in table.sd.cols}
        exprs = {('', 'count'): 'COUNT(*)'}
        for col, col_type in list(field_types.items()):
            d = {}
            if self.assignment_func:
                d = self.assignment_func(col, col_type)
                if d is None:
                    d = self.get_default_exprs(col, col_type)
            else:
                d = self.get_default_exprs(col, col_type)
            exprs.update(d)

        exprs.update(self.extra_exprs)
        exprs = OrderedDict(exprs)
        exprs_str = ',\n        '.join([v + ' AS ' + k[0] + '__' + k[1] for k, v in exprs.items()])
        where_clause = ["{0} = '{1}'".format(k, v) for k, v in self.partition.items()]
        where_clause = ' AND\n        '.join(where_clause)
        sql = 'SELECT {exprs_str} FROM {table} WHERE {where_clause};'.format(exprs_str=exprs_str,
          table=(self.table),
          where_clause=where_clause)
        hook = PrestoHook(presto_conn_id=(self.presto_conn_id))
        self.log.info('Executing SQL check: %s', sql)
        row = hook.get_first(hql=sql)
        self.log.info('Record: %s', row)
        if not row:
            raise AirflowException('The query returned None')
        part_json = json.dumps((self.partition), sort_keys=True)
        self.log.info('Deleting rows from previous runs if they exist')
        mysql = MySqlHook(self.mysql_conn_id)
        sql = "\n        SELECT 1 FROM hive_stats\n        WHERE\n            table_name='{table}' AND\n            partition_repr='{part_json}' AND\n            dttm='{dttm}'\n        LIMIT 1;\n        ".format(table=(self.table), part_json=part_json, dttm=(self.dttm))
        if mysql.get_records(sql):
            sql = "\n            DELETE FROM hive_stats\n            WHERE\n                table_name='{table}' AND\n                partition_repr='{part_json}' AND\n                dttm='{dttm}';\n            ".format(table=(self.table), part_json=part_json, dttm=(self.dttm))
            mysql.run(sql)
        self.log.info('Pivoting and loading cells into the Airflow db')
        rows = [(self.ds, self.dttm, self.table, part_json) + (r[0][0], r[0][1], r[1]) for r in zip(exprs, row)]
        mysql.insert_rows(table='hive_stats',
          rows=rows,
          target_fields=[
         'ds',
         'dttm',
         'table_name',
         'partition_repr',
         'col',
         'metric',
         'value'])