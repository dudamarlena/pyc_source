# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/spark_submit_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 7946 bytes
from airflow.contrib.hooks.spark_submit_hook import SparkSubmitHook
from airflow.models import BaseOperator
from airflow.settings import WEB_COLORS
from airflow.utils.decorators import apply_defaults

class SparkSubmitOperator(BaseOperator):
    """SparkSubmitOperator"""
    template_fields = ('_application', '_conf', '_files', '_py_files', '_jars', '_driver_class_path',
                       '_packages', '_exclude_packages', '_keytab', '_principal',
                       '_name', '_application_args', '_env_vars')
    ui_color = WEB_COLORS['LIGHTORANGE']

    @apply_defaults
    def __init__(self, application='', conf=None, conn_id='spark_default', files=None, py_files=None, archives=None, driver_class_path=None, jars=None, java_class=None, packages=None, exclude_packages=None, repositories=None, total_executor_cores=None, executor_cores=None, executor_memory=None, driver_memory=None, keytab=None, principal=None, name='airflow-spark', num_executors=None, application_args=None, env_vars=None, verbose=False, spark_binary='spark-submit', *args, **kwargs):
        (super(SparkSubmitOperator, self).__init__)(*args, **kwargs)
        self._application = application
        self._conf = conf
        self._files = files
        self._py_files = py_files
        self._archives = archives
        self._driver_class_path = driver_class_path
        self._jars = jars
        self._java_class = java_class
        self._packages = packages
        self._exclude_packages = exclude_packages
        self._repositories = repositories
        self._total_executor_cores = total_executor_cores
        self._executor_cores = executor_cores
        self._executor_memory = executor_memory
        self._driver_memory = driver_memory
        self._keytab = keytab
        self._principal = principal
        self._name = name
        self._num_executors = num_executors
        self._application_args = application_args
        self._env_vars = env_vars
        self._verbose = verbose
        self._spark_binary = spark_binary
        self._hook = None
        self._conn_id = conn_id

    def execute(self, context):
        """
        Call the SparkSubmitHook to run the provided spark job
        """
        self._hook = SparkSubmitHook(conf=(self._conf),
          conn_id=(self._conn_id),
          files=(self._files),
          py_files=(self._py_files),
          archives=(self._archives),
          driver_class_path=(self._driver_class_path),
          jars=(self._jars),
          java_class=(self._java_class),
          packages=(self._packages),
          exclude_packages=(self._exclude_packages),
          repositories=(self._repositories),
          total_executor_cores=(self._total_executor_cores),
          executor_cores=(self._executor_cores),
          executor_memory=(self._executor_memory),
          driver_memory=(self._driver_memory),
          keytab=(self._keytab),
          principal=(self._principal),
          name=(self._name),
          num_executors=(self._num_executors),
          application_args=(self._application_args),
          env_vars=(self._env_vars),
          verbose=(self._verbose),
          spark_binary=(self._spark_binary))
        self._hook.submit(self._application)

    def on_kill(self):
        self._hook.on_kill()