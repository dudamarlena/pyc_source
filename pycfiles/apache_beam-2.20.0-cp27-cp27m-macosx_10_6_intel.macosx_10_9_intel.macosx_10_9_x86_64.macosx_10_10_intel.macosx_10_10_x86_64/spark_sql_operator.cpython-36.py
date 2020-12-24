# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/spark_sql_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4307 bytes
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.contrib.hooks.spark_sql_hook import SparkSqlHook

class SparkSqlOperator(BaseOperator):
    """SparkSqlOperator"""
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