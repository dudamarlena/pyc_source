# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/spark_sql_hook.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 6066 bytes
import subprocess
from airflow.hooks.base_hook import BaseHook
from airflow.exceptions import AirflowException

class SparkSqlHook(BaseHook):
    """SparkSqlHook"""

    def __init__(self, sql, conf=None, conn_id='spark_sql_default', total_executor_cores=None, executor_cores=None, executor_memory=None, keytab=None, principal=None, master='yarn', name='default-name', num_executors=None, verbose=True, yarn_queue='default'):
        self._sql = sql
        self._conf = conf
        self._conn = self.get_connection(conn_id)
        self._total_executor_cores = total_executor_cores
        self._executor_cores = executor_cores
        self._executor_memory = executor_memory
        self._keytab = keytab
        self._principal = principal
        self._master = master
        self._name = name
        self._num_executors = num_executors
        self._verbose = verbose
        self._yarn_queue = yarn_queue
        self._sp = None

    def get_conn(self):
        pass

    def _prepare_command(self, cmd):
        """
        Construct the spark-sql command to execute. Verbose output is enabled
        as default.

        :param cmd: command to append to the spark-sql command
        :type cmd: str
        :return: full command to be executed
        """
        connection_cmd = [
         'spark-sql']
        if self._conf:
            for conf_el in self._conf.split(','):
                connection_cmd += ['--conf', conf_el]

        if self._total_executor_cores:
            connection_cmd += ['--total-executor-cores', str(self._total_executor_cores)]
        if self._executor_cores:
            connection_cmd += ['--executor-cores', str(self._executor_cores)]
        if self._executor_memory:
            connection_cmd += ['--executor-memory', self._executor_memory]
        if self._keytab:
            connection_cmd += ['--keytab', self._keytab]
        if self._principal:
            connection_cmd += ['--principal', self._principal]
        if self._num_executors:
            connection_cmd += ['--num-executors', str(self._num_executors)]
        if self._sql:
            sql = self._sql.strip()
            if sql.endswith('.sql') or sql.endswith('.hql'):
                connection_cmd += ['-f', sql]
            else:
                connection_cmd += ['-e', sql]
        if self._master:
            connection_cmd += ['--master', self._master]
        if self._name:
            connection_cmd += ['--name', self._name]
        if self._verbose:
            connection_cmd += ['--verbose']
        if self._yarn_queue:
            connection_cmd += ['--queue', self._yarn_queue]
        connection_cmd += cmd
        self.log.debug('Spark-Sql cmd: %s', connection_cmd)
        return connection_cmd

    def run_query(self, cmd='', **kwargs):
        """
        Remote Popen (actually execute the Spark-sql query)

        :param cmd: command to remotely execute
        :param kwargs: extra arguments to Popen (see subprocess.Popen)
        """
        spark_sql_cmd = self._prepare_command(cmd)
        self._sp = (subprocess.Popen)(spark_sql_cmd, stdout=subprocess.PIPE, 
         stderr=subprocess.STDOUT, **kwargs)
        for line in iter(self._sp.stdout.readline, ''):
            self.log.info(line)

        returncode = self._sp.wait()
        if returncode:
            raise AirflowException('Cannot execute {} on {}. Process exit code: {}.'.format(cmd, self._conn.host, returncode))

    def kill(self):
        if self._sp:
            if self._sp.poll() is None:
                self.log.info('Killing the Spark-Sql job')
                self._sp.kill()