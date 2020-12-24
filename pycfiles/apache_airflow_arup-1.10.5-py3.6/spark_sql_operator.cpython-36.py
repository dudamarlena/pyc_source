# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/spark_sql_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4307 bytes
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.contrib.hooks.spark_sql_hook import SparkSqlHook

class SparkSqlOperator(BaseOperator):
    __doc__ = '\n    Execute Spark SQL query\n\n    :param sql: The SQL query to execute. (templated)\n    :type sql: str\n    :param conf: arbitrary Spark configuration property\n    :type conf: str (format: PROP=VALUE)\n    :param conn_id: connection_id string\n    :type conn_id: str\n    :param total_executor_cores: (Standalone & Mesos only) Total cores for all\n        executors (Default: all the available cores on the worker)\n    :type total_executor_cores: int\n    :param executor_cores: (Standalone & YARN only) Number of cores per\n        executor (Default: 2)\n    :type executor_cores: int\n    :param executor_memory: Memory per executor (e.g. 1000M, 2G) (Default: 1G)\n    :type executor_memory: str\n    :param keytab: Full path to the file that contains the keytab\n    :type keytab: str\n    :param master: spark://host:port, mesos://host:port, yarn, or local\n    :type master: str\n    :param name: Name of the job\n    :type name: str\n    :param num_executors: Number of executors to launch\n    :type num_executors: int\n    :param verbose: Whether to pass the verbose flag to spark-sql\n    :type verbose: bool\n    :param yarn_queue: The YARN queue to submit to (Default: "default")\n    :type yarn_queue: str\n    '
    template_fields = [
     '_sql']
    template_ext = ['.sql', '.hql']

    @apply_defaults
    def __init__(self, sql, conf=None, conn_id='spark_sql_default', total_executor_cores=None, executor_cores=None, executor_memory=None, keytab=None, principal=None, master='yarn', name='default-name', num_executors=None, yarn_queue='default', *args, **kwargs):
        (super(SparkSqlOperator, self).__init__)(*args, **kwargs)
        self._sql = sql
        self._conf = conf
        self._conn_id = conn_id
        self._total_executor_cores = total_executor_cores
        self._executor_cores = executor_cores
        self._executor_memory = executor_memory
        self._keytab = keytab
        self._principal = principal
        self._master = master
        self._name = name
        self._num_executors = num_executors
        self._yarn_queue = yarn_queue
        self._hook = None

    def execute(self, context):
        """
        Call the SparkSqlHook to run the provided sql query
        """
        self._hook = SparkSqlHook(sql=(self._sql), conf=(self._conf),
          conn_id=(self._conn_id),
          total_executor_cores=(self._total_executor_cores),
          executor_cores=(self._executor_cores),
          executor_memory=(self._executor_memory),
          keytab=(self._keytab),
          principal=(self._principal),
          name=(self._name),
          num_executors=(self._num_executors),
          master=(self._master),
          yarn_queue=(self._yarn_queue))
        self._hook.run_query()

    def on_kill(self):
        self._hook.kill()