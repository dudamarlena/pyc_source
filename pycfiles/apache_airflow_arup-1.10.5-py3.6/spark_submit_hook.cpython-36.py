# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/spark_submit_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 25288 bytes
import os, subprocess, re, time
from airflow.hooks.base_hook import BaseHook
from airflow.exceptions import AirflowException
from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.contrib.kubernetes import kube_client

class SparkSubmitHook(BaseHook, LoggingMixin):
    __doc__ = '\n    This hook is a wrapper around the spark-submit binary to kick off a spark-submit job.\n    It requires that the "spark-submit" binary is in the PATH or the spark_home to be\n    supplied.\n\n    :param conf: Arbitrary Spark configuration properties\n    :type conf: dict\n    :param conn_id: The connection id as configured in Airflow administration. When an\n        invalid connection_id is supplied, it will default to yarn.\n    :type conn_id: str\n    :param files: Upload additional files to the executor running the job, separated by a\n        comma. Files will be placed in the working directory of each executor.\n        For example, serialized objects.\n    :type files: str\n    :param py_files: Additional python files used by the job, can be .zip, .egg or .py.\n    :type py_files: str\n    :param: archives: Archives that spark should unzip (and possibly tag with #ALIAS) into\n        the application working directory.\n    :param driver_class_path: Additional, driver-specific, classpath settings.\n    :type driver_class_path: str\n    :param jars: Submit additional jars to upload and place them in executor classpath.\n    :type jars: str\n    :param java_class: the main class of the Java application\n    :type java_class: str\n    :param packages: Comma-separated list of maven coordinates of jars to include on the\n        driver and executor classpaths\n    :type packages: str\n    :param exclude_packages: Comma-separated list of maven coordinates of jars to exclude\n        while resolving the dependencies provided in \'packages\'\n    :type exclude_packages: str\n    :param repositories: Comma-separated list of additional remote repositories to search\n        for the maven coordinates given with \'packages\'\n    :type repositories: str\n    :param total_executor_cores: (Standalone & Mesos only) Total cores for all executors\n        (Default: all the available cores on the worker)\n    :type total_executor_cores: int\n    :param executor_cores: (Standalone, YARN and Kubernetes only) Number of cores per\n        executor (Default: 2)\n    :type executor_cores: int\n    :param executor_memory: Memory per executor (e.g. 1000M, 2G) (Default: 1G)\n    :type executor_memory: str\n    :param driver_memory: Memory allocated to the driver (e.g. 1000M, 2G) (Default: 1G)\n    :type driver_memory: str\n    :param keytab: Full path to the file that contains the keytab\n    :type keytab: str\n    :param principal: The name of the kerberos principal used for keytab\n    :type principal: str\n    :param name: Name of the job (default airflow-spark)\n    :type name: str\n    :param num_executors: Number of executors to launch\n    :type num_executors: int\n    :param application_args: Arguments for the application being submitted\n    :type application_args: list\n    :param env_vars: Environment variables for spark-submit. It\n        supports yarn and k8s mode too.\n    :type env_vars: dict\n    :param verbose: Whether to pass the verbose flag to spark-submit process for debugging\n    :type verbose: bool\n    :param spark_binary: The command to use for spark submit.\n                         Some distros may use spark2-submit.\n    :type spark_binary: str\n    '

    def __init__(self, conf=None, conn_id='spark_default', files=None, py_files=None, archives=None, driver_class_path=None, jars=None, java_class=None, packages=None, exclude_packages=None, repositories=None, total_executor_cores=None, executor_cores=None, executor_memory=None, driver_memory=None, keytab=None, principal=None, name='default-name', num_executors=None, application_args=None, env_vars=None, verbose=False, spark_binary=None):
        self._conf = conf
        self._conn_id = conn_id
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
        self._submit_sp = None
        self._yarn_application_id = None
        self._kubernetes_driver_pod = None
        self._spark_binary = spark_binary
        self._connection = self._resolve_connection()
        self._is_yarn = 'yarn' in self._connection['master']
        self._is_kubernetes = 'k8s' in self._connection['master']
        if self._is_kubernetes:
            if kube_client is None:
                raise RuntimeError('{} specified by kubernetes dependencies are not installed!'.format(self._connection['master']))
        self._should_track_driver_status = self._resolve_should_track_driver_status()
        self._driver_id = None
        self._driver_status = None
        self._spark_exit_code = None

    def _resolve_should_track_driver_status(self):
        """
        Determines whether or not this hook should poll the spark driver status through
        subsequent spark-submit status requests after the initial spark-submit request
        :return: if the driver status should be tracked
        """
        return 'spark://' in self._connection['master'] and self._connection['deploy_mode'] == 'cluster'

    def _resolve_connection(self):
        conn_data = {'master':'yarn', 
         'queue':None, 
         'deploy_mode':None, 
         'spark_home':None, 
         'spark_binary':self._spark_binary or 'spark-submit', 
         'namespace':'default'}
        try:
            conn = self.get_connection(self._conn_id)
            if conn.port:
                conn_data['master'] = '{}:{}'.format(conn.host, conn.port)
            else:
                conn_data['master'] = conn.host
            extra = conn.extra_dejson
            conn_data['queue'] = extra.get('queue', None)
            conn_data['deploy_mode'] = extra.get('deploy-mode', None)
            conn_data['spark_home'] = extra.get('spark-home', None)
            conn_data['spark_binary'] = self._spark_binary or extra.get('spark-binary', 'spark-submit')
            conn_data['namespace'] = extra.get('namespace', 'default')
        except AirflowException:
            self.log.info('Could not load connection string %s, defaulting to %s', self._conn_id, conn_data['master'])

        return conn_data

    def get_conn(self):
        pass

    def _get_spark_binary_path(self):
        if self._connection['spark_home']:
            connection_cmd = [os.path.join(self._connection['spark_home'], 'bin', self._connection['spark_binary'])]
        else:
            connection_cmd = [
             self._connection['spark_binary']]
        return connection_cmd

    def _build_spark_submit_command(self, application):
        """
        Construct the spark-submit command to execute.
        :param application: command to append to the spark-submit command
        :type application: str
        :return: full command to be executed
        """
        connection_cmd = self._get_spark_binary_path()
        connection_cmd += ['--master', self._connection['master']]
        if self._conf:
            for key in self._conf:
                connection_cmd += ['--conf', '{}={}'.format(key, str(self._conf[key]))]

        if self._env_vars:
            if self._is_kubernetes or self._is_yarn:
                if self._is_yarn:
                    tmpl = 'spark.yarn.appMasterEnv.{}={}'
                else:
                    tmpl = 'spark.kubernetes.driverEnv.{}={}'
                for key in self._env_vars:
                    connection_cmd += [
                     '--conf',
                     tmpl.format(key, str(self._env_vars[key]))]

        if self._env_vars and self._connection['deploy_mode'] != 'cluster':
            self._env = self._env_vars
        else:
            if self._env_vars:
                if self._connection['deploy_mode'] == 'cluster':
                    raise AirflowException('SparkSubmitHook env_vars is not supported in standalone-cluster mode.')
        if self._is_kubernetes:
            connection_cmd += ['--conf',
             'spark.kubernetes.namespace={}'.format(self._connection['namespace'])]
        if self._files:
            connection_cmd += ['--files', self._files]
        if self._py_files:
            connection_cmd += ['--py-files', self._py_files]
        if self._archives:
            connection_cmd += ['--archives', self._archives]
        if self._driver_class_path:
            connection_cmd += ['--driver-class-path', self._driver_class_path]
        if self._jars:
            connection_cmd += ['--jars', self._jars]
        if self._packages:
            connection_cmd += ['--packages', self._packages]
        if self._exclude_packages:
            connection_cmd += ['--exclude-packages', self._exclude_packages]
        if self._repositories:
            connection_cmd += ['--repositories', self._repositories]
        if self._num_executors:
            connection_cmd += ['--num-executors', str(self._num_executors)]
        if self._total_executor_cores:
            connection_cmd += ['--total-executor-cores', str(self._total_executor_cores)]
        if self._executor_cores:
            connection_cmd += ['--executor-cores', str(self._executor_cores)]
        if self._executor_memory:
            connection_cmd += ['--executor-memory', self._executor_memory]
        if self._driver_memory:
            connection_cmd += ['--driver-memory', self._driver_memory]
        if self._keytab:
            connection_cmd += ['--keytab', self._keytab]
        if self._principal:
            connection_cmd += ['--principal', self._principal]
        if self._name:
            connection_cmd += ['--name', self._name]
        if self._java_class:
            connection_cmd += ['--class', self._java_class]
        if self._verbose:
            connection_cmd += ['--verbose']
        if self._connection['queue']:
            connection_cmd += ['--queue', self._connection['queue']]
        if self._connection['deploy_mode']:
            connection_cmd += ['--deploy-mode', self._connection['deploy_mode']]
        connection_cmd += [application]
        if self._application_args:
            connection_cmd += self._application_args
        self.log.info('Spark-Submit cmd: %s', connection_cmd)
        return connection_cmd

    def _build_track_driver_status_command(self):
        """
        Construct the command to poll the driver status.

        :return: full command to be executed
        """
        connection_cmd = self._get_spark_binary_path()
        connection_cmd += ['--master', self._connection['master']]
        if self._driver_id:
            connection_cmd += ['--status', self._driver_id]
        else:
            raise AirflowException('Invalid status: attempted to poll driver status but no driver id is known. Giving up.')
        self.log.debug('Poll driver status cmd: %s', connection_cmd)
        return connection_cmd

    def submit(self, application='', **kwargs):
        """
        Remote Popen to execute the spark-submit job

        :param application: Submitted application, jar or py file
        :type application: str
        :param kwargs: extra arguments to Popen (see subprocess.Popen)
        """
        spark_submit_cmd = self._build_spark_submit_command(application)
        if hasattr(self, '_env'):
            env = os.environ.copy()
            env.update(self._env)
            kwargs['env'] = env
        self._submit_sp = (subprocess.Popen)(spark_submit_cmd, stdout=subprocess.PIPE, 
         stderr=subprocess.STDOUT, 
         bufsize=-1, 
         universal_newlines=True, **kwargs)
        self._process_spark_submit_log(iter(self._submit_sp.stdout.readline, ''))
        returncode = self._submit_sp.wait()
        if returncode or self._is_kubernetes and self._spark_exit_code != 0:
            raise AirflowException('Cannot execute: {}. Error code is: {}.'.format(spark_submit_cmd, returncode))
        self.log.debug('Should track driver: {}'.format(self._should_track_driver_status))
        if self._should_track_driver_status:
            if self._driver_id is None:
                raise AirflowException('No driver id is known: something went wrong when executing the spark submit command')
            self._driver_status = 'SUBMITTED'
            self._start_driver_status_tracking()
            if self._driver_status != 'FINISHED':
                raise AirflowException('ERROR : Driver {} badly exited with status {}'.format(self._driver_id, self._driver_status))

    def _process_spark_submit_log(self, itr):
        """
        Processes the log files and extracts useful information out of it.

        If the deploy-mode is 'client', log the output of the submit command as those
        are the output logs of the Spark worker directly.

        Remark: If the driver needs to be tracked for its status, the log-level of the
        spark deploy needs to be at least INFO (log4j.logger.org.apache.spark.deploy=INFO)

        :param itr: An iterator which iterates over the input of the subprocess
        """
        for line in itr:
            line = line.strip()
            if self._is_yarn and self._connection['deploy_mode'] == 'cluster':
                match = re.search('(application[0-9_]+)', line)
                if match:
                    self._yarn_application_id = match.groups()[0]
                    self.log.info('Identified spark driver id: %s', self._yarn_application_id)
            else:
                if self._is_kubernetes:
                    match = re.search('\\s*pod name: ((.+?)-([a-z0-9]+)-driver)', line)
                    if match:
                        self._kubernetes_driver_pod = match.groups()[0]
                        self.log.info('Identified spark driver pod: %s', self._kubernetes_driver_pod)
                    match_exit_code = re.search('\\s*Exit code: (\\d+)', line)
                    if match_exit_code:
                        self._spark_exit_code = int(match_exit_code.groups()[0])
                else:
                    if self._should_track_driver_status:
                        if not self._driver_id:
                            match_driver_id = re.search('(driver-[0-9\\-]+)', line)
                            if match_driver_id:
                                self._driver_id = match_driver_id.groups()[0]
                                self.log.info('identified spark driver id: {}'.format(self._driver_id))
            self.log.info(line)

    def _process_spark_status_log(self, itr):
        """
        parses the logs of the spark driver status query process

        :param itr: An iterator which iterates over the input of the subprocess
        """
        for line in itr:
            line = line.strip()
            if 'driverState' in line:
                self._driver_status = line.split(' : ')[1].replace(',', '').replace('"', '').strip()
            self.log.debug('spark driver status log: {}'.format(line))

    def _start_driver_status_tracking(self):
        """
        Polls the driver based on self._driver_id to get the status.
        Finish successfully when the status is FINISHED.
        Finish failed when the status is ERROR/UNKNOWN/KILLED/FAILED.

        Possible status:

        SUBMITTED
            Submitted but not yet scheduled on a worker
        RUNNING
            Has been allocated to a worker to run
        FINISHED
            Previously ran and exited cleanly
        RELAUNCHING
            Exited non-zero or due to worker failure, but has not yet
            started running again
        UNKNOWN
            The status of the driver is temporarily not known due to
            master failure recovery
        KILLED
            A user manually killed this driver
        FAILED
            The driver exited non-zero and was not supervised
        ERROR
            Unable to run or restart due to an unrecoverable error
            (e.g. missing jar file)
        """
        missed_job_status_reports = 0
        max_missed_job_status_reports = 10
        while self._driver_status not in ('FINISHED', 'UNKNOWN', 'KILLED', 'FAILED',
                                          'ERROR'):
            time.sleep(1)
            self.log.debug('polling status of spark driver with id {}'.format(self._driver_id))
            poll_drive_status_cmd = self._build_track_driver_status_command()
            status_process = subprocess.Popen(poll_drive_status_cmd, stdout=(subprocess.PIPE),
              stderr=(subprocess.STDOUT),
              bufsize=(-1),
              universal_newlines=True)
            self._process_spark_status_log(iter(status_process.stdout.readline, ''))
            returncode = status_process.wait()
            if returncode:
                if missed_job_status_reports < max_missed_job_status_reports:
                    missed_job_status_reports = missed_job_status_reports + 1
                else:
                    raise AirflowException('Failed to poll for the driver status {} times: returncode = {}'.format(max_missed_job_status_reports, returncode))

    def _build_spark_driver_kill_command(self):
        """
        Construct the spark-submit command to kill a driver.
        :return: full command to kill a driver
        """
        if self._connection['spark_home']:
            connection_cmd = [
             os.path.join(self._connection['spark_home'], 'bin', self._connection['spark_binary'])]
        else:
            connection_cmd = [
             self._connection['spark_binary']]
        connection_cmd += ['--master', self._connection['master']]
        connection_cmd += ['--kill', self._driver_id]
        self.log.debug('Spark-Kill cmd: %s', connection_cmd)
        return connection_cmd

    def on_kill(self):
        self.log.debug('Kill Command is being called')
        if self._should_track_driver_status:
            if self._driver_id:
                self.log.info('Killing driver {} on cluster'.format(self._driver_id))
                kill_cmd = self._build_spark_driver_kill_command()
                driver_kill = subprocess.Popen(kill_cmd, stdout=(subprocess.PIPE),
                  stderr=(subprocess.PIPE))
                self.log.info('Spark driver {} killed with return code: {}'.format(self._driver_id, driver_kill.wait()))
        if self._submit_sp and self._submit_sp.poll() is None:
            self.log.info('Sending kill signal to %s', self._connection['spark_binary'])
            self._submit_sp.kill()
            if self._yarn_application_id:
                self.log.info('Killing application {} on YARN'.format(self._yarn_application_id))
                kill_cmd = 'yarn application -kill {}'.format(self._yarn_application_id).split()
                yarn_kill = subprocess.Popen(kill_cmd, stdout=(subprocess.PIPE),
                  stderr=(subprocess.PIPE))
                self.log.info('YARN killed with return code: %s', yarn_kill.wait())
            if self._kubernetes_driver_pod:
                self.log.info('Killing pod %s on Kubernetes', self._kubernetes_driver_pod)
                try:
                    client = kube_client.get_kube_client()
                    api_response = client.delete_namespaced_pod((self._kubernetes_driver_pod),
                      (self._connection['namespace']),
                      body=(client.V1DeleteOptions()),
                      pretty=True)
                    self.log.info('Spark on K8s killed with response: %s', api_response)
                except kube_client.ApiException as e:
                    self.log.info('Exception when attempting to kill Spark on K8s:')
                    self.log.exception(e)