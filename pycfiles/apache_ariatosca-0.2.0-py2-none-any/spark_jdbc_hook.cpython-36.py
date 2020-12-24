# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/spark_jdbc_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 11618 bytes
import os
from airflow.contrib.hooks.spark_submit_hook import SparkSubmitHook
from airflow.exceptions import AirflowException

class SparkJDBCHook(SparkSubmitHook):
    """SparkJDBCHook"""

    def __init__(self, spark_app_name='airflow-spark-jdbc', spark_conn_id='spark-default', spark_conf=None, spark_py_files=None, spark_files=None, spark_jars=None, num_executors=None, executor_cores=None, executor_memory=None, driver_memory=None, verbose=False, principal=None, keytab=None, cmd_type='spark_to_jdbc', jdbc_table=None, jdbc_conn_id='jdbc-default', jdbc_driver=None, metastore_table=None, jdbc_truncate=False, save_mode=None, save_format=None, batch_size=None, fetch_size=None, num_partitions=None, partition_column=None, lower_bound=None, upper_bound=None, create_table_column_types=None, *args, **kwargs):
        (super(SparkJDBCHook, self).__init__)(*args, **kwargs)
        self._name = spark_app_name
        self._conn_id = spark_conn_id
        self._conf = spark_conf
        self._py_files = spark_py_files
        self._files = spark_files
        self._jars = spark_jars
        self._num_executors = num_executors
        self._executor_cores = executor_cores
        self._executor_memory = executor_memory
        self._driver_memory = driver_memory
        self._verbose = verbose
        self._keytab = keytab
        self._principal = principal
        self._cmd_type = cmd_type
        self._jdbc_table = jdbc_table
        self._jdbc_conn_id = jdbc_conn_id
        self._jdbc_driver = jdbc_driver
        self._metastore_table = metastore_table
        self._jdbc_truncate = jdbc_truncate
        self._save_mode = save_mode
        self._save_format = save_format
        self._batch_size = batch_size
        self._fetch_size = fetch_size
        self._num_partitions = num_partitions
        self._partition_column = partition_column
        self._lower_bound = lower_bound
        self._upper_bound = upper_bound
        self._create_table_column_types = create_table_column_types
        self._jdbc_connection = self._resolve_jdbc_connection()

    def _resolve_jdbc_connection(self):
        conn_data = {'url':'', 
         'schema':'', 
         'conn_prefix':'', 
         'user':'', 
         'password':''}
        try:
            conn = self.get_connection(self._jdbc_conn_id)
            if conn.port:
                conn_data['url'] = '{}:{}'.format(conn.host, conn.port)
            else:
                conn_data['url'] = conn.host
            conn_data['schema'] = conn.schema
            conn_data['user'] = conn.login
            conn_data['password'] = conn.password
            extra = conn.extra_dejson
            conn_data['conn_prefix'] = extra.get('conn_prefix', '')
        except AirflowException:
            self.log.debug('Could not load jdbc connection string %s, defaulting to %s', self._jdbc_conn_id, '')

        return conn_data

    def _build_jdbc_application_arguments(self, jdbc_conn):
        arguments = []
        arguments += ['-cmdType', self._cmd_type]
        if self._jdbc_connection['url']:
            arguments += ['-url',
             '{0}{1}/{2}'.format(jdbc_conn['conn_prefix'], jdbc_conn['url'], jdbc_conn['schema'])]
        if self._jdbc_connection['user']:
            arguments += ['-user', self._jdbc_connection['user']]
        if self._jdbc_connection['password']:
            arguments += ['-password', self._jdbc_connection['password']]
        if self._metastore_table:
            arguments += ['-metastoreTable', self._metastore_table]
        if self._jdbc_table:
            arguments += ['-jdbcTable', self._jdbc_table]
        if self._jdbc_truncate:
            arguments += ['-jdbcTruncate', str(self._jdbc_truncate)]
        if self._jdbc_driver:
            arguments += ['-jdbcDriver', self._jdbc_driver]
        if self._batch_size:
            arguments += ['-batchsize', str(self._batch_size)]
        if self._fetch_size:
            arguments += ['-fetchsize', str(self._fetch_size)]
        if self._num_partitions:
            arguments += ['-numPartitions', str(self._num_partitions)]
        if self._partition_column:
            if self._lower_bound:
                if self._upper_bound:
                    if self._num_partitions:
                        arguments += ['-partitionColumn', self._partition_column,
                         '-lowerBound', self._lower_bound,
                         '-upperBound', self._upper_bound]
        if self._save_mode:
            arguments += ['-saveMode', self._save_mode]
        if self._save_format:
            arguments += ['-saveFormat', self._save_format]
        if self._create_table_column_types:
            arguments += ['-createTableColumnTypes', self._create_table_column_types]
        return arguments

    def submit_jdbc_job(self):
        self._application_args = self._build_jdbc_application_arguments(self._jdbc_connection)
        self.submit(application=(os.path.dirname(os.path.abspath(__file__)) + '/spark_jdbc_script.py'))

    def get_conn(self):
        pass