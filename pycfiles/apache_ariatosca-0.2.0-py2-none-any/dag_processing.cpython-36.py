# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/utils/dag_processing.py
# Compiled at: 2019-09-11 03:47:35
# Size of source mod 2**32: 48286 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging, multiprocessing, os, re, signal, sys, time, zipfile
from abc import ABCMeta, abstractmethod
from collections import defaultdict
from collections import namedtuple
from importlib import import_module
import enum
from typing import Optional
import psutil
from setproctitle import setproctitle
import six
from six.moves import reload_module
from tabulate import tabulate
import airflow.models
from airflow import configuration as conf
from airflow.dag.base_dag import BaseDag, BaseDagBag
from airflow.exceptions import AirflowException
from airflow.settings import Stats
from airflow.models import errors
from airflow.utils import timezone
from airflow.utils.helpers import reap_process_group
from airflow.utils.db import provide_session
from airflow.utils.log.logging_mixin import LoggingMixin
if six.PY2:
    ConnectionError = IOError

class SimpleDag(BaseDag):
    """SimpleDag"""

    def __init__(self, dag, pickle_id=None):
        """
        :param dag: the DAG
        :type dag: airflow.models.DAG
        :param pickle_id: ID associated with the pickled version of this DAG.
        :type pickle_id: unicode
        """
        self._dag_id = dag.dag_id
        self._task_ids = [task.task_id for task in dag.tasks]
        self._full_filepath = dag.full_filepath
        self._is_paused = dag.is_paused
        self._concurrency = dag.concurrency
        self._pickle_id = pickle_id
        self._task_special_args = {}
        for task in dag.tasks:
            special_args = {}
            if task.task_concurrency is not None:
                special_args['task_concurrency'] = task.task_concurrency
            if len(special_args) > 0:
                self._task_special_args[task.task_id] = special_args

    @property
    def dag_id(self):
        """
        :return: the DAG ID
        :rtype: unicode
        """
        return self._dag_id

    @property
    def task_ids(self):
        """
        :return: A list of task IDs that are in this DAG
        :rtype: list[unicode]
        """
        return self._task_ids

    @property
    def full_filepath(self):
        """
        :return: The absolute path to the file that contains this DAG's definition
        :rtype: unicode
        """
        return self._full_filepath

    @property
    def concurrency(self):
        """
        :return: maximum number of tasks that can run simultaneously from this DAG
        :rtype: int
        """
        return self._concurrency

    @property
    def is_paused(self):
        """
        :return: whether this DAG is paused or not
        :rtype: bool
        """
        return self._is_paused

    @property
    def pickle_id(self):
        """
        :return: The pickle ID for this DAG, if it has one. Otherwise None.
        :rtype: unicode
        """
        return self._pickle_id

    @property
    def task_special_args(self):
        return self._task_special_args

    def get_task_special_arg(self, task_id, special_arg_name):
        if task_id in self._task_special_args:
            if special_arg_name in self._task_special_args[task_id]:
                return self._task_special_args[task_id][special_arg_name]
        return


class SimpleTaskInstance(object):

    def __init__(self, ti):
        self._dag_id = ti.dag_id
        self._task_id = ti.task_id
        self._execution_date = ti.execution_date
        self._start_date = ti.start_date
        self._end_date = ti.end_date
        self._try_number = ti.try_number
        self._state = ti.state
        self._executor_config = ti.executor_config
        if hasattr(ti, 'run_as_user'):
            self._run_as_user = ti.run_as_user
        else:
            self._run_as_user = None
        if hasattr(ti, 'pool'):
            self._pool = ti.pool
        else:
            self._pool = None
        if hasattr(ti, 'priority_weight'):
            self._priority_weight = ti.priority_weight
        else:
            self._priority_weight = None
        self._queue = ti.queue
        self._key = ti.key

    @property
    def dag_id(self):
        return self._dag_id

    @property
    def task_id(self):
        return self._task_id

    @property
    def execution_date(self):
        return self._execution_date

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @property
    def try_number(self):
        return self._try_number

    @property
    def state(self):
        return self._state

    @property
    def pool(self):
        return self._pool

    @property
    def priority_weight(self):
        return self._priority_weight

    @property
    def queue(self):
        return self._queue

    @property
    def key(self):
        return self._key

    @property
    def executor_config(self):
        return self._executor_config

    @provide_session
    def construct_task_instance(self, session=None, lock_for_update=False):
        """
        Construct a TaskInstance from the database based on the primary key

        :param session: DB session.
        :param lock_for_update: if True, indicates that the database should
            lock the TaskInstance (issuing a FOR UPDATE clause) until the
            session is committed.
        """
        TI = airflow.models.TaskInstance
        qry = session.query(TI).filter(TI.dag_id == self._dag_id, TI.task_id == self._task_id, TI.execution_date == self._execution_date)
        if lock_for_update:
            ti = qry.with_for_update().first()
        else:
            ti = qry.first()
        return ti


class SimpleDagBag(BaseDagBag):
    """SimpleDagBag"""

    def __init__(self, simple_dags):
        """
        Constructor.

        :param simple_dags: SimpleDag objects that should be in this
        :type list(airflow.utils.dag_processing.SimpleDagBag)
        """
        self.simple_dags = simple_dags
        self.dag_id_to_simple_dag = {}
        for simple_dag in simple_dags:
            self.dag_id_to_simple_dag[simple_dag.dag_id] = simple_dag

    @property
    def dag_ids(self):
        """
        :return: IDs of all the DAGs in this
        :rtype: list[unicode]
        """
        return self.dag_id_to_simple_dag.keys()

    def get_dag(self, dag_id):
        """
        :param dag_id: DAG ID
        :type dag_id: unicode
        :return: if the given DAG ID exists in the bag, return the BaseDag
        corresponding to that ID. Otherwise, throw an Exception
        :rtype: airflow.utils.dag_processing.SimpleDag
        """
        if dag_id not in self.dag_id_to_simple_dag:
            raise AirflowException('Unknown DAG ID {}'.format(dag_id))
        return self.dag_id_to_simple_dag[dag_id]


def correct_maybe_zipped(fileloc):
    """
    If the path contains a folder with a .zip suffix, then
    the folder is treated as a zip archive and path to zip is returned.
    """
    _, archive, filename = re.search('((.*\\.zip){})?(.*)'.format(re.escape(os.sep)), fileloc).groups()
    if archive:
        if zipfile.is_zipfile(archive):
            return archive
    return fileloc


COMMENT_PATTERN = re.compile('\\s*#.*')

def list_py_file_paths(directory, safe_mode=conf.getboolean('core', 'DAG_DISCOVERY_SAFE_MODE', fallback=True), include_examples=None):
    """
    Traverse a directory and look for Python files.

    :param directory: the directory to traverse
    :type directory: unicode
    :param safe_mode: whether to use a heuristic to determine whether a file
        contains Airflow DAG definitions. If not provided, use the
        core.DAG_DISCOVERY_SAFE_MODE configuration setting. If not set, default
        to safe.
    :return: a list of paths to Python files in the specified directory
    :rtype: list[unicode]
    """
    if include_examples is None:
        include_examples = conf.getboolean('core', 'LOAD_EXAMPLES')
    file_paths = []
    if directory is None:
        return []
    else:
        if os.path.isfile(directory):
            return [directory]
        else:
            if os.path.isdir(directory):
                patterns_by_dir = {}
                for root, dirs, files in os.walk(directory, followlinks=True):
                    patterns = patterns_by_dir.get(root, [])
                    ignore_file = os.path.join(root, '.airflowignore')
                    if os.path.isfile(ignore_file):
                        with open(ignore_file, 'r') as (f):
                            lines_no_comments = [COMMENT_PATTERN.sub('', line) for line in f.read().split('\n')]
                            patterns += [re.compile(line) for line in lines_no_comments if line]
                    dirs[:] = [d for d in dirs if not any(p.search(os.path.join(root, d)) for p in patterns)]
                    for d in dirs:
                        patterns_by_dir[os.path.join(root, d)] = patterns

                    for f in files:
                        try:
                            file_path = os.path.join(root, f)
                            if not os.path.isfile(file_path):
                                continue
                            mod_name, file_ext = os.path.splitext(os.path.split(file_path)[(-1)])
                            if file_ext != '.py':
                                if not zipfile.is_zipfile(file_path):
                                    continue
                            if any([re.findall(p, file_path) for p in patterns]):
                                continue
                            might_contain_dag = True
                            if safe_mode:
                                if not zipfile.is_zipfile(file_path):
                                    with open(file_path, 'rb') as (fp):
                                        content = fp.read()
                                        might_contain_dag = all([s in content for s in ('DAG',
                                                                                        'airflow')])
                            if not might_contain_dag:
                                continue
                            file_paths.append(file_path)
                        except Exception:
                            log = LoggingMixin().log
                            log.exception('Error while examining %s', f)

            if include_examples:
                import airflow.example_dags
                example_dag_folder = airflow.example_dags.__path__[0]
                file_paths.extend(list_py_file_paths(example_dag_folder, safe_mode, False))
        return file_paths


class AbstractDagFileProcessor(object):
    """AbstractDagFileProcessor"""
    __metaclass__ = ABCMeta

    @abstractmethod
    def start(self):
        """
        Launch the process to process the file
        """
        raise NotImplementedError()

    @abstractmethod
    def terminate(self, sigkill=False):
        """
        Terminate (and then kill) the process launched to process the file
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def pid(self):
        """
        :return: the PID of the process launched to process the given file
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def exit_code(self):
        """
        After the process is finished, this can be called to get the return code
        :return: the exit code of the process
        :rtype: int
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def done(self):
        """
        Check if the process launched to process this file is done.
        :return: whether the process is finished running
        :rtype: bool
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def result(self):
        """
        :return: result of running SchedulerJob.process_file()
        :rtype: list[airflow.utils.dag_processing.SimpleDag]
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def start_time(self):
        """
        :return: When this started to process the file
        :rtype: datetime
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def file_path(self):
        """
        :return: the path to the file that this is processing
        :rtype: unicode
        """
        raise NotImplementedError()


DagParsingStat = namedtuple('DagParsingStat', ['file_paths', 'done', 'all_files_processed'])

class DagParsingSignal(enum.Enum):
    AGENT_HEARTBEAT = 'agent_heartbeat'
    TERMINATE_MANAGER = 'terminate_manager'
    END_MANAGER = 'end_manager'


class DagFileProcessorAgent(LoggingMixin):
    """DagFileProcessorAgent"""

    def __init__(self, dag_directory, file_paths, max_runs, processor_factory, processor_timeout, async_mode):
        """
        :param dag_directory: Directory where DAG definitions are kept. All
            files in file_paths should be under this directory
        :type dag_directory: unicode
        :param file_paths: list of file paths that contain DAG definitions
        :type file_paths: list[unicode]
        :param max_runs: The number of times to parse and schedule each file. -1
            for unlimited.
        :type max_runs: int
        :param processor_factory: function that creates processors for DAG
            definition files. Arguments are (dag_definition_path, log_file_path)
        :type processor_factory: (unicode, unicode, list) -> (AbstractDagFileProcessor)
        :param processor_timeout: How long to wait before timing out a DAG file processor
        :type processor_timeout: timedelta
        :param async_mode: Whether to start agent in async mode
        :type async_mode: bool
        """
        self._file_paths = file_paths
        self._file_path_queue = []
        self._dag_directory = dag_directory
        self._max_runs = max_runs
        self._processor_factory = processor_factory
        self._processor_timeout = processor_timeout
        self._async_mode = async_mode
        self._processors = {}
        self._last_runtime = {}
        self._last_finish_time = {}
        self._run_count = defaultdict(int)
        self._process = None
        self._done = False
        self._all_files_processed = True
        self._parent_signal_conn = None
        self._collected_dag_buffer = []

    def start(self):
        """
        Launch DagFileProcessorManager processor and start DAG parsing loop in manager.
        """
        self._parent_signal_conn, child_signal_conn = multiprocessing.Pipe()
        self._process = multiprocessing.Process(target=(type(self)._run_processor_manager),
          args=(
         self._dag_directory,
         self._file_paths,
         self._max_runs,
         self._processor_factory,
         self._processor_timeout,
         child_signal_conn,
         self._async_mode))
        self._process.start()
        self.log.info('Launched DagFileProcessorManager with pid: %s', self._process.pid)

    def heartbeat(self):
        """
        Should only be used when launched DAG file processor manager in sync mode.
        Send agent heartbeat signal to the manager, requesting that it runs one
        processing "loop".

        Call wait_until_finished to ensure that any launched processors have
        finished before continuing
        """
        if not self._process.is_alive():
            return
        try:
            self._parent_signal_conn.send(DagParsingSignal.AGENT_HEARTBEAT)
        except ConnectionError:
            pass

    def wait_until_finished(self):
        while self._parent_signal_conn.poll():
            try:
                result = self._parent_signal_conn.recv()
            except EOFError:
                break

            self._process_message(result)
            if isinstance(result, DagParsingStat):
                return

    @staticmethod
    def _run_processor_manager(dag_directory, file_paths, max_runs, processor_factory, processor_timeout, signal_conn, async_mode):
        os.setpgid(0, 0)
        setproctitle('airflow scheduler -- DagFileProcessorManager')
        os.environ['CONFIG_PROCESSOR_MANAGER_LOGGER'] = 'True'
        os.environ['AIRFLOW__CORE__COLORED_CONSOLE_LOG'] = 'False'
        reload_module(import_module(airflow.settings.LOGGING_CLASS_PATH.rsplit('.', 1)[0]))
        reload_module(airflow.settings)
        airflow.settings.initialize()
        del os.environ['CONFIG_PROCESSOR_MANAGER_LOGGER']
        processor_manager = DagFileProcessorManager(dag_directory, file_paths, max_runs, processor_factory, processor_timeout, signal_conn, async_mode)
        processor_manager.start()

    def harvest_simple_dags(self):
        """
        Harvest DAG parsing results from result queue and sync metadata from stat queue.

        :return: List of parsing result in SimpleDag format.
        """
        while self._parent_signal_conn.poll():
            try:
                result = self._parent_signal_conn.recv()
            except (EOFError, ConnectionError):
                break

            self._process_message(result)

        simple_dags = self._collected_dag_buffer
        self._collected_dag_buffer = []
        self._heartbeat_manager()
        return simple_dags

    def _process_message(self, message):
        self.log.debug('Received message of type %s', type(message).__name__)
        if isinstance(message, DagParsingStat):
            self._sync_metadata(message)
        else:
            self._collected_dag_buffer.append(message)

    def _heartbeat_manager(self):
        """
        Heartbeat DAG file processor and restart it if we are not done.
        """
        if self._process:
            if not self._process.is_alive():
                self._process.join(timeout=0)
                if not self.done:
                    self.log.warning('DagFileProcessorManager (PID=%d) exited with exit code %d - re-launching', self._process.pid, self._process.exitcode)
                    self.start()

    def _sync_metadata(self, stat):
        """
        Sync metadata from stat queue and only keep the latest stat.
        """
        self._file_paths = stat.file_paths
        self._done = stat.done
        self._all_files_processed = stat.all_files_processed

    @property
    def file_paths(self):
        return self._file_paths

    @property
    def done(self):
        return self._done

    @property
    def all_files_processed(self):
        return self._all_files_processed

    def terminate(self):
        """
        Send termination signal to DAG parsing processor manager
        and expect it to terminate all DAG file processors.
        """
        if self._process:
            if self._process.is_alive():
                self.log.info('Sending termination message to manager.')
                self._parent_signal_conn.send(DagParsingSignal.TERMINATE_MANAGER)

    def end(self):
        """
        Terminate (and then kill) the manager process launched.
        :return:
        """
        if not self._process:
            self.log.warning('Ending without manager process.')
            return
        reap_process_group((self._process.pid), log=(self.log))
        self._parent_signal_conn.close()


class DagFileProcessorManager(LoggingMixin):
    """DagFileProcessorManager"""

    def __init__(self, dag_directory, file_paths, max_runs, processor_factory, processor_timeout, signal_conn, async_mode=True):
        """
        :param dag_directory: Directory where DAG definitions are kept. All
            files in file_paths should be under this directory
        :type dag_directory: unicode
        :param file_paths: list of file paths that contain DAG definitions
        :type file_paths: list[unicode]
        :param max_runs: The number of times to parse and schedule each file. -1
            for unlimited.
        :type max_runs: int
        :param processor_factory: function that creates processors for DAG
            definition files. Arguments are (dag_definition_path)
        :type processor_factory: (unicode, unicode, list) -> (AbstractDagFileProcessor)
        :param processor_timeout: How long to wait before timing out a DAG file processor
        :type processor_timeout: timedelta
        :param signal_conn: connection to communicate signal with processor agent.
        :type signal_conn: airflow.models.connection.Connection
        :param async_mode: whether to start the manager in async mode
        :type async_mode: bool
        """
        self._file_paths = file_paths
        self._file_path_queue = []
        self._dag_directory = dag_directory
        self._max_runs = max_runs
        self._processor_factory = processor_factory
        self._signal_conn = signal_conn
        self._async_mode = async_mode
        self._parallelism = conf.getint('scheduler', 'max_threads')
        if 'sqlite' in conf.get('core', 'sql_alchemy_conn'):
            if self._parallelism > 1:
                self.log.error('Cannot use more than 1 thread when using sqlite. Setting parallelism to 1')
                self._parallelism = 1
        self._file_process_interval = conf.getint('scheduler', 'min_file_process_interval')
        self.print_stats_interval = conf.getint('scheduler', 'print_stats_interval')
        self._processors = {}
        self._last_runtime = {}
        self._last_finish_time = {}
        self._last_zombie_query_time = timezone.utcnow()
        self.last_dag_dir_refresh_time = timezone.utcnow()
        self.last_stat_print_time = timezone.datetime(2000, 1, 1)
        self._zombie_query_interval = 10
        self._run_count = defaultdict(int)
        self._heart_beat_key = 'heart-beat'
        self._processor_timeout = processor_timeout
        self.dag_dir_list_interval = conf.getint('scheduler', 'dag_dir_list_interval')
        self._log = logging.getLogger('airflow.processor_manager')
        signal.signal(signal.SIGINT, self._exit_gracefully)
        signal.signal(signal.SIGTERM, self._exit_gracefully)

    def _exit_gracefully(self, signum, frame):
        """
        Helper method to clean up DAG file processors to avoid leaving orphan processes.
        """
        self.log.info('Exiting gracefully upon receiving signal %s', signum)
        self.terminate()
        self.end()
        self.log.debug('Finished terminating DAG processors.')
        sys.exit(os.EX_OK)

    def start(self):
        """
        Use multiple processes to parse and generate tasks for the
        DAGs in parallel. By processing them in separate processes,
        we can get parallelism and isolation from potentially harmful
        user code.
        """
        self.log.info('Processing files using up to %s processes at a time ', self._parallelism)
        self.log.info('Process each file at most once every %s seconds', self._file_process_interval)
        self.log.info('Checking for new files in %s every %s seconds', self._dag_directory, self.dag_dir_list_interval)
        poll_time = None
        if self._async_mode:
            poll_time = 0.0
            self.log.debug('Starting DagFileProcessorManager in async mode')
        else:
            poll_time = None
            self.log.debug('Starting DagFileProcessorManager in sync mode')
        while 1:
            loop_start_time = time.time()
            if self._signal_conn.poll(poll_time):
                agent_signal = self._signal_conn.recv()
                self.log.debug('Recived %s singal from DagFileProcessorAgent', agent_signal)
                if agent_signal == DagParsingSignal.TERMINATE_MANAGER:
                    self.terminate()
                    break
                else:
                    if agent_signal == DagParsingSignal.END_MANAGER:
                        self.end()
                        sys.exit(os.EX_OK)
                    else:
                        if agent_signal == DagParsingSignal.AGENT_HEARTBEAT:
                            pass
                        else:
                            if not self._async_mode:
                                continue
                            else:
                                self._refresh_dag_dir()
                                simple_dags = self.heartbeat()
                                for simple_dag in simple_dags:
                                    self._signal_conn.send(simple_dag)

                                if not self._async_mode:
                                    self.log.debug("Waiting for processors to finish since we're using sqlite")
                                    self.wait_until_finished()
                                    simple_dags = self.collect_results()
                                    for simple_dag in simple_dags:
                                        self._signal_conn.send(simple_dag)

                                self._print_stat()
                                all_files_processed = all(self.get_last_finish_time(x) is not None for x in self.file_paths)
                                max_runs_reached = self.max_runs_reached()
                                dag_parsing_stat = DagParsingStat(self._file_paths, max_runs_reached, all_files_processed)
                                self._signal_conn.send(dag_parsing_stat)
                                if max_runs_reached:
                                    self.log.info('Exiting dag parsing loop as all files have been processed %s times', self._max_runs)
                                    break
                            if self._async_mode:
                                loop_duration = time.time() - loop_start_time
                                if loop_duration < 1:
                                    poll_time = 1 - loop_duration
                                else:
                                    poll_time = 0.0

    def _refresh_dag_dir(self):
        """
        Refresh file paths from dag dir if we haven't done it for too long.
        """
        elapsed_time_since_refresh = (timezone.utcnow() - self.last_dag_dir_refresh_time).total_seconds()
        if elapsed_time_since_refresh > self.dag_dir_list_interval:
            self.log.info('Searching for files in %s', self._dag_directory)
            self._file_paths = list_py_file_paths(self._dag_directory)
            self.last_dag_dir_refresh_time = timezone.utcnow()
            self.log.info('There are %s files in %s', len(self._file_paths), self._dag_directory)
            self.set_file_paths(self._file_paths)
            try:
                self.log.debug('Removing old import errors')
                self.clear_nonexistent_import_errors()
            except Exception:
                self.log.exception('Error removing old import errors')

    def _print_stat(self):
        """
        Occasionally print out stats about how fast the files are getting processed
        """
        if (timezone.utcnow() - self.last_stat_print_time).total_seconds() > self.print_stats_interval:
            if len(self._file_paths) > 0:
                self._log_file_processing_stats(self._file_paths)
            self.last_stat_print_time = timezone.utcnow()

    @provide_session
    def clear_nonexistent_import_errors(self, session):
        """
        Clears import errors for files that no longer exist.

        :param session: session for ORM operations
        :type session: sqlalchemy.orm.session.Session
        """
        query = session.query(errors.ImportError)
        if self._file_paths:
            query = query.filter(~errors.ImportError.filename.in_(self._file_paths))
        query.delete(synchronize_session='fetch')
        session.commit()

    def _log_file_processing_stats(self, known_file_paths):
        """
        Print out stats about how files are getting processed.

        :param known_file_paths: a list of file paths that may contain Airflow
            DAG definitions
        :type known_file_paths: list[unicode]
        :return: None
        """
        headers = [
         'File Path',
         'PID',
         'Runtime',
         'Last Runtime',
         'Last Run']
        rows = []
        for file_path in known_file_paths:
            last_runtime = self.get_last_runtime(file_path)
            file_name = os.path.basename(file_path)
            file_name = os.path.splitext(file_name)[0].replace(os.sep, '.')
            if last_runtime:
                Stats.gauge('dag_processing.last_runtime.{}'.format(file_name), last_runtime)
            processor_pid = self.get_pid(file_path)
            processor_start_time = self.get_start_time(file_path)
            runtime = (timezone.utcnow() - processor_start_time).total_seconds() if processor_start_time else None
            last_run = self.get_last_finish_time(file_path)
            if last_run:
                seconds_ago = (timezone.utcnow() - last_run).total_seconds()
                Stats.gauge('dag_processing.last_run.seconds_ago.{}'.format(file_name), seconds_ago)
            rows.append((file_path,
             processor_pid,
             runtime,
             last_runtime,
             last_run))

        rows = sorted(rows, key=(lambda x: x[3] or 0.0))
        formatted_rows = []
        for file_path, pid, runtime, last_runtime, last_run in rows:
            formatted_rows.append((file_path,
             pid,
             '{:.2f}s'.format(runtime) if runtime else None,
             '{:.2f}s'.format(last_runtime) if last_runtime else None,
             last_run.strftime('%Y-%m-%dT%H:%M:%S') if last_run else None))

        log_str = '\n' + '=' * 80 + '\n' + 'DAG File Processing Stats\n\n' + tabulate(formatted_rows, headers=headers) + '\n' + '=' * 80
        self.log.info(log_str)

    @property
    def file_paths(self):
        return self._file_paths

    def get_pid(self, file_path):
        """
        :param file_path: the path to the file that's being processed
        :type file_path: unicode
        :return: the PID of the process processing the given file or None if
            the specified file is not being processed
        :rtype: int
        """
        if file_path in self._processors:
            return self._processors[file_path].pid

    def get_all_pids(self):
        """
        :return: a list of the PIDs for the processors that are running
        :rtype: List[int]
        """
        return [x.pid for x in self._processors.values()]

    def get_runtime(self, file_path):
        """
        :param file_path: the path to the file that's being processed
        :type file_path: unicode
        :return: the current runtime (in seconds) of the process that's
            processing the specified file or None if the file is not currently
            being processed
        """
        if file_path in self._processors:
            return (timezone.utcnow() - self._processors[file_path].start_time).total_seconds()

    def get_last_runtime(self, file_path):
        """
        :param file_path: the path to the file that was processed
        :type file_path: unicode
        :return: the runtime (in seconds) of the process of the last run, or
            None if the file was never processed.
        :rtype: float
        """
        return self._last_runtime.get(file_path)

    def get_last_finish_time(self, file_path):
        """
        :param file_path: the path to the file that was processed
        :type file_path: unicode
        :return: the finish time of the process of the last run, or None if the
            file was never processed.
        :rtype: datetime
        """
        return self._last_finish_time.get(file_path)

    def get_start_time(self, file_path):
        """
        :param file_path: the path to the file that's being processed
        :type file_path: unicode
        :return: the start time of the process that's processing the
            specified file or None if the file is not currently being processed
        :rtype: datetime
        """
        if file_path in self._processors:
            return self._processors[file_path].start_time

    def set_file_paths(self, new_file_paths):
        """
        Update this with a new set of paths to DAG definition files.

        :param new_file_paths: list of paths to DAG definition files
        :type new_file_paths: list[unicode]
        :return: None
        """
        self._file_paths = new_file_paths
        self._file_path_queue = [x for x in self._file_path_queue if x in new_file_paths]
        filtered_processors = {}
        for file_path, processor in self._processors.items():
            if file_path in new_file_paths:
                filtered_processors[file_path] = processor
            else:
                self.log.warning('Stopping processor for %s', file_path)
                processor.terminate()

        self._processors = filtered_processors

    def wait_until_finished(self):
        """
        Sleeps until all the processors are done.
        """
        for file_path, processor in self._processors.items():
            while not processor.done:
                time.sleep(0.1)

    def collect_results(self):
        """
        Collect the result from any finished DAG processors

        :return: a list of SimpleDags that were produced by processors that
            have finished since the last time this was called
        :rtype: list[airflow.utils.dag_processing.SimpleDag]
        """
        self._kill_timed_out_processors()
        finished_processors = {}
        running_processors = {}
        for file_path, processor in self._processors.items():
            if processor.done:
                self.log.debug('Processor for %s finished', file_path)
                now = timezone.utcnow()
                finished_processors[file_path] = processor
                self._last_runtime[file_path] = (now - processor.start_time).total_seconds()
                self._last_finish_time[file_path] = now
                self._run_count[file_path] += 1
            else:
                running_processors[file_path] = processor

        self._processors = running_processors
        self.log.debug('%s/%s DAG parsing processes running', len(self._processors), self._parallelism)
        self.log.debug('%s file paths queued for processing', len(self._file_path_queue))
        simple_dags = []
        for file_path, processor in finished_processors.items():
            if processor.result is None:
                self.log.warning('Processor for %s exited with return code %s.', processor.file_path, processor.exit_code)
            else:
                for simple_dag in processor.result:
                    simple_dags.append(simple_dag)

        return simple_dags

    def heartbeat(self):
        """
        This should be periodically called by the manager loop. This method will
        kick off new processes to process DAG definition files and read the
        results from the finished processors.

        :return: a list of SimpleDags that were produced by processors that
            have finished since the last time this was called
        :rtype: list[airflow.utils.dag_processing.SimpleDag]
        """
        simple_dags = self.collect_results()
        if len(self._file_path_queue) == 0:
            file_paths_in_progress = self._processors.keys()
            now = timezone.utcnow()
            file_paths_recently_processed = []
            for file_path in self._file_paths:
                last_finish_time = self.get_last_finish_time(file_path)
                if last_finish_time is not None and (now - last_finish_time).total_seconds() < self._file_process_interval:
                    file_paths_recently_processed.append(file_path)

            files_paths_at_run_limit = [file_path for file_path, num_runs in self._run_count.items() if num_runs == self._max_runs]
            files_paths_to_queue = list(set(self._file_paths) - set(file_paths_in_progress) - set(file_paths_recently_processed) - set(files_paths_at_run_limit))
            for file_path, processor in self._processors.items():
                self.log.debug('File path %s is still being processed (started: %s)', processor.file_path, processor.start_time.isoformat())

            self.log.debug('Queuing the following files for processing:\n\t%s', '\n\t'.join(files_paths_to_queue))
            self._file_path_queue.extend(files_paths_to_queue)
        while self._parallelism - len(self._processors) > 0 and len(self._file_path_queue) > 0:
            file_path = self._file_path_queue.pop(0)
            processor = self._processor_factory(file_path)
            processor.start()
            self.log.debug('Started a process (PID: %s) to generate tasks for %s', processor.pid, file_path)
            self._processors[file_path] = processor

        self._run_count[self._heart_beat_key] += 1
        return simple_dags

    def _kill_timed_out_processors(self):
        """
        Kill any file processors that timeout to defend against process hangs.
        """
        now = timezone.utcnow()
        for file_path, processor in self._processors.items():
            duration = now - processor.start_time
            if duration > self._processor_timeout:
                self.log.info('Processor for %s with PID %s started at %s has timed out, killing it.', processor.file_path, processor.pid, processor.start_time.isoformat())
                Stats.incr('dag_file_processor_timeouts', 1, 1)
                processor.kill()

    def max_runs_reached(self):
        """
        :return: whether all file paths have been processed max_runs times
        """
        if self._max_runs == -1:
            return False
        else:
            for file_path in self._file_paths:
                if self._run_count[file_path] < self._max_runs:
                    return False

            if self._run_count[self._heart_beat_key] < self._max_runs:
                return False
            return True

    def terminate(self):
        """
        Stops all running processors
        :return: None
        """
        for processor in self._processors.values():
            processor.terminate()

    def end(self):
        """
        Kill all child processes on exit since we don't want to leave
        them as orphaned.
        """
        pids_to_kill = self.get_all_pids()
        if len(pids_to_kill) > 0:
            this_process = psutil.Process(os.getpid())
            child_processes = [x for x in this_process.children(recursive=True) if x.is_running() if x.pid in pids_to_kill]
            for child in child_processes:
                self.log.info('Terminating child PID: %s', child.pid)
                child.terminate()

            timeout = 5
            self.log.info('Waiting up to %s seconds for processes to exit...', timeout)
            try:
                psutil.wait_procs(child_processes,
                  timeout=timeout, callback=(lambda x: self.log.info('Terminated PID %s', x.pid)))
            except psutil.TimeoutExpired:
                self.log.debug('Ran out of time while waiting for processes to exit')

            child_processes = [x for x in this_process.children(recursive=True) if x.is_running() if x.pid in pids_to_kill]
            if len(child_processes) > 0:
                self.log.info('SIGKILL processes that did not terminate gracefully')
                for child in child_processes:
                    self.log.info('Killing child PID: %s', child.pid)
                    child.kill()
                    child.wait()