# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/spark_jdbc_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 10133 bytes
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from airflow.contrib.hooks.spark_jdbc_hook import SparkJDBCHook
from airflow.utils.decorators import apply_defaults

class SparkJDBCOperator(SparkSubmitOperator):
    __doc__ = '\n    This operator extends the SparkSubmitOperator specifically for performing data\n    transfers to/from JDBC-based databases with Apache Spark. As with the\n    SparkSubmitOperator, it assumes that the "spark-submit" binary is available on the\n    PATH.\n\n    :param spark_app_name: Name of the job (default airflow-spark-jdbc)\n    :type spark_app_name: str\n    :param spark_conn_id: Connection id as configured in Airflow administration\n    :type spark_conn_id: str\n    :param spark_conf: Any additional Spark configuration properties\n    :type spark_conf: dict\n    :param spark_py_files: Additional python files used (.zip, .egg, or .py)\n    :type spark_py_files: str\n    :param spark_files: Additional files to upload to the container running the job\n    :type spark_files: str\n    :param spark_jars: Additional jars to upload and add to the driver and\n                       executor classpath\n    :type spark_jars: str\n    :param num_executors: number of executor to run. This should be set so as to manage\n                          the number of connections made with the JDBC database\n    :type num_executors: int\n    :param executor_cores: Number of cores per executor\n    :type executor_cores: int\n    :param executor_memory: Memory per executor (e.g. 1000M, 2G)\n    :type executor_memory: str\n    :param driver_memory: Memory allocated to the driver (e.g. 1000M, 2G)\n    :type driver_memory: str\n    :param verbose: Whether to pass the verbose flag to spark-submit for debugging\n    :type verbose: bool\n    :param keytab: Full path to the file that contains the keytab\n    :type keytab: str\n    :param principal: The name of the kerberos principal used for keytab\n    :type principal: str\n    :param cmd_type: Which way the data should flow. 2 possible values:\n                     spark_to_jdbc: data written by spark from metastore to jdbc\n                     jdbc_to_spark: data written by spark from jdbc to metastore\n    :type cmd_type: str\n    :param jdbc_table: The name of the JDBC table\n    :type jdbc_table: str\n    :param jdbc_conn_id: Connection id used for connection to JDBC database\n    :type jdbc_conn_id: str\n    :param jdbc_driver: Name of the JDBC driver to use for the JDBC connection. This\n                        driver (usually a jar) should be passed in the \'jars\' parameter\n    :type jdbc_driver: str\n    :param metastore_table: The name of the metastore table,\n    :type metastore_table: str\n    :param jdbc_truncate: (spark_to_jdbc only) Whether or not Spark should truncate or\n                         drop and recreate the JDBC table. This only takes effect if\n                         \'save_mode\' is set to Overwrite. Also, if the schema is\n                         different, Spark cannot truncate, and will drop and recreate\n    :type jdbc_truncate: bool\n    :param save_mode: The Spark save-mode to use (e.g. overwrite, append, etc.)\n    :type save_mode: str\n    :param save_format: (jdbc_to_spark-only) The Spark save-format to use (e.g. parquet)\n    :type save_format: str\n    :param batch_size: (spark_to_jdbc only) The size of the batch to insert per round\n                       trip to the JDBC database. Defaults to 1000\n    :type batch_size: int\n    :param fetch_size: (jdbc_to_spark only) The size of the batch to fetch per round trip\n                       from the JDBC database. Default depends on the JDBC driver\n    :type fetch_size: int\n    :param num_partitions: The maximum number of partitions that can be used by Spark\n                           simultaneously, both for spark_to_jdbc and jdbc_to_spark\n                           operations. This will also cap the number of JDBC connections\n                           that can be opened\n    :type num_partitions: int\n    :param partition_column: (jdbc_to_spark-only) A numeric column to be used to\n                             partition the metastore table by. If specified, you must\n                             also specify:\n                             num_partitions, lower_bound, upper_bound\n    :type partition_column: str\n    :param lower_bound: (jdbc_to_spark-only) Lower bound of the range of the numeric\n                        partition column to fetch. If specified, you must also specify:\n                        num_partitions, partition_column, upper_bound\n    :type lower_bound: int\n    :param upper_bound: (jdbc_to_spark-only) Upper bound of the range of the numeric\n                        partition column to fetch. If specified, you must also specify:\n                        num_partitions, partition_column, lower_bound\n    :type upper_bound: int\n    :param create_table_column_types: (spark_to_jdbc-only) The database column data types\n                                      to use instead of the defaults, when creating the\n                                      table. Data type information should be specified in\n                                      the same format as CREATE TABLE columns syntax\n                                      (e.g: "name CHAR(64), comments VARCHAR(1024)").\n                                      The specified types should be valid spark sql data\n                                      types.\n    '

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