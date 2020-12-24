# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/spark_jdbc_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 11618 bytes
import os
from airflow.contrib.hooks.spark_submit_hook import SparkSubmitHook
from airflow.exceptions import AirflowException

class SparkJDBCHook(SparkSubmitHook):
    __doc__ = '\n    This hook extends the SparkSubmitHook specifically for performing data\n    transfers to/from JDBC-based databases with Apache Spark.\n\n    :param spark_app_name: Name of the job (default airflow-spark-jdbc)\n    :type spark_app_name: str\n    :param spark_conn_id: Connection id as configured in Airflow administration\n    :type spark_conn_id: str\n    :param spark_conf: Any additional Spark configuration properties\n    :type spark_conf: dict\n    :param spark_py_files: Additional python files used (.zip, .egg, or .py)\n    :type spark_py_files: str\n    :param spark_files: Additional files to upload to the container running the job\n    :type spark_files: str\n    :param spark_jars: Additional jars to upload and add to the driver and\n                       executor classpath\n    :type spark_jars: str\n    :param num_executors: number of executor to run. This should be set so as to manage\n                          the number of connections made with the JDBC database\n    :type num_executors: int\n    :param executor_cores: Number of cores per executor\n    :type executor_cores: int\n    :param executor_memory: Memory per executor (e.g. 1000M, 2G)\n    :type executor_memory: str\n    :param driver_memory: Memory allocated to the driver (e.g. 1000M, 2G)\n    :type driver_memory: str\n    :param verbose: Whether to pass the verbose flag to spark-submit for debugging\n    :type verbose: bool\n    :param keytab: Full path to the file that contains the keytab\n    :type keytab: str\n    :param principal: The name of the kerberos principal used for keytab\n    :type principal: str\n    :param cmd_type: Which way the data should flow. 2 possible values:\n                     spark_to_jdbc: data written by spark from metastore to jdbc\n                     jdbc_to_spark: data written by spark from jdbc to metastore\n    :type cmd_type: str\n    :param jdbc_table: The name of the JDBC table\n    :type jdbc_table: str\n    :param jdbc_conn_id: Connection id used for connection to JDBC database\n    :type jdbc_conn_id: str\n    :param jdbc_driver: Name of the JDBC driver to use for the JDBC connection. This\n                        driver (usually a jar) should be passed in the \'jars\' parameter\n    :type jdbc_driver: str\n    :param metastore_table: The name of the metastore table,\n    :type metastore_table: str\n    :param jdbc_truncate: (spark_to_jdbc only) Whether or not Spark should truncate or\n                         drop and recreate the JDBC table. This only takes effect if\n                         \'save_mode\' is set to Overwrite. Also, if the schema is\n                         different, Spark cannot truncate, and will drop and recreate\n    :type jdbc_truncate: bool\n    :param save_mode: The Spark save-mode to use (e.g. overwrite, append, etc.)\n    :type save_mode: str\n    :param save_format: (jdbc_to_spark-only) The Spark save-format to use (e.g. parquet)\n    :type save_format: str\n    :param batch_size: (spark_to_jdbc only) The size of the batch to insert per round\n                       trip to the JDBC database. Defaults to 1000\n    :type batch_size: int\n    :param fetch_size: (jdbc_to_spark only) The size of the batch to fetch per round trip\n                       from the JDBC database. Default depends on the JDBC driver\n    :type fetch_size: int\n    :param num_partitions: The maximum number of partitions that can be used by Spark\n                           simultaneously, both for spark_to_jdbc and jdbc_to_spark\n                           operations. This will also cap the number of JDBC connections\n                           that can be opened\n    :type num_partitions: int\n    :param partition_column: (jdbc_to_spark-only) A numeric column to be used to\n                             partition the metastore table by. If specified, you must\n                             also specify:\n                             num_partitions, lower_bound, upper_bound\n    :type partition_column: str\n    :param lower_bound: (jdbc_to_spark-only) Lower bound of the range of the numeric\n                        partition column to fetch. If specified, you must also specify:\n                        num_partitions, partition_column, upper_bound\n    :type lower_bound: int\n    :param upper_bound: (jdbc_to_spark-only) Upper bound of the range of the numeric\n                        partition column to fetch. If specified, you must also specify:\n                        num_partitions, partition_column, lower_bound\n    :type upper_bound: int\n    :param create_table_column_types: (spark_to_jdbc-only) The database column data types\n                                      to use instead of the defaults, when creating the\n                                      table. Data type information should be specified in\n                                      the same format as CREATE TABLE columns syntax\n                                      (e.g: "name CHAR(64), comments VARCHAR(1024)").\n                                      The specified types should be valid spark sql data\n                                      types.\n    '

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