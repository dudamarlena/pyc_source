# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/spark_jdbc_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 10133 bytes
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from airflow.contrib.hooks.spark_jdbc_hook import SparkJDBCHook
from airflow.utils.decorators import apply_defaults

class SparkJDBCOperator(SparkSubmitOperator):
    """SparkJDBCOperator"""

    @apply_defaults
    def __init__(self, spark_app_name='airflow-spark-jdbc', spark_conn_id='spark-default', spark_conf=None, spark_py_files=None, spark_files=None, spark_jars=None, num_executors=None, executor_cores=None, executor_memory=None, driver_memory=None, verbose=False, keytab=None, principal=None, cmd_type='spark_to_jdbc', jdbc_table=None, jdbc_conn_id='jdbc-default', jdbc_driver=None, metastore_table=None, jdbc_truncate=False, save_mode=None, save_format=None, batch_size=None, fetch_size=None, num_partitions=None, partition_column=None, lower_bound=None, upper_bound=None, create_table_column_types=None, *args, **kwargs):
        (super(SparkJDBCOperator, self).__init__)(*args, **kwargs)
        self._spark_app_name = spark_app_name
        self._spark_conn_id = spark_conn_id
        self._spark_conf = spark_conf
        self._spark_py_files = spark_py_files
        self._spark_files = spark_files
        self._spark_jars = spark_jars
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

    def execute(self, context):
        """
        Call the SparkSubmitHook to run the provided spark job
        """
        self._hook = SparkJDBCHook(spark_app_name=(self._spark_app_name),
          spark_conn_id=(self._spark_conn_id),
          spark_conf=(self._spark_conf),
          spark_py_files=(self._spark_py_files),
          spark_files=(self._spark_files),
          spark_jars=(self._spark_jars),
          num_executors=(self._num_executors),
          executor_cores=(self._executor_cores),
          executor_memory=(self._executor_memory),
          driver_memory=(self._driver_memory),
          verbose=(self._verbose),
          keytab=(self._keytab),
          principal=(self._principal),
          cmd_type=(self._cmd_type),
          jdbc_table=(self._jdbc_table),
          jdbc_conn_id=(self._jdbc_conn_id),
          jdbc_driver=(self._jdbc_driver),
          metastore_table=(self._metastore_table),
          jdbc_truncate=(self._jdbc_truncate),
          save_mode=(self._save_mode),
          save_format=(self._save_format),
          batch_size=(self._batch_size),
          fetch_size=(self._fetch_size),
          num_partitions=(self._num_partitions),
          partition_column=(self._partition_column),
          lower_bound=(self._lower_bound),
          upper_bound=(self._upper_bound),
          create_table_column_types=(self._create_table_column_types))
        self._hook.submit_jdbc_job()

    def on_kill(self):
        self._hook.on_kill()