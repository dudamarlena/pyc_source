# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/models/dagbag.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 18569 bytes
from __future__ import division
from __future__ import unicode_literals
import hashlib, imp, importlib, os, sys, textwrap, zipfile
from collections import namedtuple
from datetime import datetime, timedelta
import six
from croniter import croniter, CroniterBadCronError, CroniterBadDateError, CroniterNotAlphaError
from sqlalchemy import or_
from airflow import configuration, settings
from airflow.dag.base_dag import BaseDagBag
from airflow.exceptions import AirflowDagCycleException
from airflow.executors import get_default_executor
from airflow.settings import Stats
from airflow.utils import timezone
from airflow.utils.dag_processing import list_py_file_paths, correct_maybe_zipped
from airflow.utils.db import provide_session
from airflow.utils.helpers import pprinttable
from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.utils.state import State
from airflow.utils.timeout import timeout

class DagBag(BaseDagBag, LoggingMixin):
    __doc__ = '\n    A dagbag is a collection of dags, parsed out of a folder tree and has high\n    level configuration settings, like what database to use as a backend and\n    what executor to use to fire off tasks. This makes it easier to run\n    distinct environments for say production and development, tests, or for\n    different teams or security profiles. What would have been system level\n    settings are now dagbag level so that one system can run multiple,\n    independent settings sets.\n\n    :param dag_folder: the folder to scan to find DAGs\n    :type dag_folder: unicode\n    :param executor: the executor to use when executing task instances\n        in this DagBag\n    :param include_examples: whether to include the examples that ship\n        with airflow or not\n    :type include_examples: bool\n    :param has_logged: an instance boolean that gets flipped from False to True after a\n        file has been skipped. This is to prevent overloading the user with logging\n        messages about skipped files. Therefore only once per DagBag is a file logged\n        being skipped.\n    '
    CYCLE_NEW = 0
    CYCLE_IN_PROGRESS = 1
    CYCLE_DONE = 2

    def __init__(self, dag_folder=None, executor=None, include_examples=configuration.conf.getboolean('core', 'LOAD_EXAMPLES'), safe_mode=configuration.conf.getboolean('core', 'DAG_DISCOVERY_SAFE_MODE')):
        if executor is None:
            executor = get_default_executor()
        dag_folder = dag_folder or settings.DAGS_FOLDER
        self.log.info('Filling up the DagBag from %s', dag_folder)
        self.dag_folder = dag_folder
        self.dags = {}
        self.file_last_changed = {}
        self.executor = executor
        self.import_errors = {}
        self.has_logged = False
        self.collect_dags(dag_folder=dag_folder,
          include_examples=include_examples,
          safe_mode=safe_mode)

    def size(self):
        """
        :return: the amount of dags contained in this dagbag
        """
        return len(self.dags)

    @property
    def dag_ids(self):
        return self.dags.keys()

    def get_dag(self, dag_id):
        """
        Gets the DAG out of the dictionary, and refreshes it if expired
        """
        from airflow.models.dag import DagModel
        root_dag_id = dag_id
        if dag_id in self.dags:
            dag = self.dags[dag_id]
            if dag.is_subdag:
                root_dag_id = dag.parent_dag.dag_id
        orm_dag = DagModel.get_current(root_dag_id)
        if orm_dag:
            if root_dag_id not in self.dags or orm_dag.last_expired and dag.last_loaded < orm_dag.last_expired:
                found_dags = self.process_file(filepath=(correct_maybe_zipped(orm_dag.fileloc)),
                  only_if_updated=False)
                if found_dags:
                    if dag_id in [found_dag.dag_id for found_dag in found_dags]:
                        return self.dags[dag_id]
                if dag_id in self.dags:
                    del self.dags[dag_id]
        return self.dags.get(dag_id)

    def process_file(self, filepath, only_if_updated=True, safe_mode=True):
        """
        Given a path to a python module or zip file, this method imports
        the module and look for dag objects within it.
        """
        from airflow.models.dag import DAG
        found_dags = []
        if filepath is None or not os.path.isfile(filepath):
            return found_dags
        else:
            try:
                file_last_changed_on_disk = datetime.fromtimestamp(os.path.getmtime(filepath))
                if only_if_updated:
                    if filepath in self.file_last_changed:
                        if file_last_changed_on_disk == self.file_last_changed[filepath]:
                            return found_dags
            except Exception as e:
                self.log.exception(e)
                return found_dags

            mods = []
            is_zipfile = zipfile.is_zipfile(filepath)
            if not is_zipfile:
                if safe_mode:
                    with open(filepath, 'rb') as (f):
                        content = f.read()
                        if not all([s in content for s in (b'DAG', b'airflow')]):
                            self.file_last_changed[filepath] = file_last_changed_on_disk
                            if not self.has_logged:
                                self.has_logged = True
                                self.log.info('File %s assumed to contain no DAGs. Skipping.', filepath)
                            return found_dags
                self.log.debug('Importing %s', filepath)
                org_mod_name, _ = os.path.splitext(os.path.split(filepath)[(-1)])
                mod_name = 'unusual_prefix_' + hashlib.sha1(filepath.encode('utf-8')).hexdigest() + '_' + org_mod_name
                if mod_name in sys.modules:
                    del sys.modules[mod_name]
                with timeout(configuration.conf.getint('core', 'DAGBAG_IMPORT_TIMEOUT')):
                    try:
                        m = imp.load_source(mod_name, filepath)
                        mods.append(m)
                    except Exception as e:
                        self.log.exception('Failed to import: %s', filepath)
                        self.import_errors[filepath] = str(e)
                        self.file_last_changed[filepath] = file_last_changed_on_disk

            else:
                zip_file = zipfile.ZipFile(filepath)
                for mod in zip_file.infolist():
                    head, _ = os.path.split(mod.filename)
                    mod_name, ext = os.path.splitext(mod.filename)
                    if not head:
                        if ext == '.py' or ext == '.pyc':
                            if mod_name == '__init__':
                                self.log.warning('Found __init__.%s at root of %s', ext, filepath)
                            else:
                                if safe_mode:
                                    with zip_file.open(mod.filename) as (zf):
                                        self.log.debug('Reading %s from %s', mod.filename, filepath)
                                        content = zf.read()
                                        if not all([s in content for s in (b'DAG',
                                                                           b'airflow')]):
                                            self.file_last_changed[filepath] = file_last_changed_on_disk
                                            if not self.has_logged:
                                                self.has_logged = True
                                                self.log.info('File %s assumed to contain no DAGs. Skipping.', filepath)
                                if mod_name in sys.modules:
                                    del sys.modules[mod_name]
                                try:
                                    sys.path.insert(0, filepath)
                                    m = importlib.import_module(mod_name)
                                    mods.append(m)
                                except Exception as e:
                                    self.log.exception('Failed to import: %s', filepath)
                                    self.import_errors[filepath] = str(e)
                                    self.file_last_changed[filepath] = file_last_changed_on_disk

            for m in mods:
                for dag in list(m.__dict__.values()):
                    if isinstance(dag, DAG):
                        if not dag.full_filepath:
                            dag.full_filepath = filepath
                            if dag.fileloc != filepath:
                                if not is_zipfile:
                                    dag.fileloc = filepath
                        else:
                            try:
                                dag.is_subdag = False
                                self.bag_dag(dag, parent_dag=dag, root_dag=dag)
                                if isinstance(dag._schedule_interval, six.string_types):
                                    croniter(dag._schedule_interval)
                                found_dags.append(dag)
                                found_dags += dag.subdags
                            except (CroniterBadCronError, CroniterBadDateError,
                             CroniterNotAlphaError) as cron_e:
                                self.log.exception('Failed to bag_dag: %s', dag.full_filepath)
                                self.import_errors[dag.full_filepath] = 'Invalid Cron expression: ' + str(cron_e)
                                self.file_last_changed[dag.full_filepath] = file_last_changed_on_disk
                            except AirflowDagCycleException as cycle_exception:
                                self.log.exception('Failed to bag_dag: %s', dag.full_filepath)
                                self.import_errors[dag.full_filepath] = str(cycle_exception)
                                self.file_last_changed[dag.full_filepath] = file_last_changed_on_disk

            self.file_last_changed[filepath] = file_last_changed_on_disk
            return found_dags

    @provide_session
    def kill_zombies(self, session=None):
        """
        Fail zombie tasks, which are tasks that haven't
        had a heartbeat for too long, in the current DagBag.

        :param session: DB session.
        :type session: sqlalchemy.orm.session.Session
        """
        from airflow.models.taskinstance import TaskInstance as TI
        from airflow.jobs import LocalTaskJob as LJ
        zombie_threshold_secs = configuration.getint('scheduler', 'scheduler_zombie_task_threshold')
        limit_dttm = timezone.utcnow() - timedelta(seconds=zombie_threshold_secs)
        self.log.debug('Failing jobs without heartbeat after %s', limit_dttm)
        tis = session.query(TI).join(LJ, TI.job_id == LJ.id).filter(TI.state == State.RUNNING).filter(TI.dag_id.in_(self.dags)).filter(or_(LJ.state != State.RUNNING, LJ.latest_heartbeat < limit_dttm)).all()
        for ti in tis:
            self.log.info('Detected zombie job with dag_id %s, task_id %s, and execution date %s', ti.dag_id, ti.task_id, ti.execution_date.isoformat())
            ti.test_mode = configuration.getboolean('core', 'unit_test_mode')
            ti.task = self.dags[ti.dag_id].get_task(ti.task_id)
            ti.handle_failure('{} detected as zombie'.format(ti), ti.test_mode, ti.get_template_context())
            self.log.info('Marked zombie job %s as %s', ti, ti.state)
            Stats.incr('zombies_killed')

        session.commit()

    def bag_dag(self, dag, parent_dag, root_dag):
        """
        Adds the DAG into the bag, recurses into sub dags.
        Throws AirflowDagCycleException if a cycle is detected in this dag or its subdags
        """
        dag.test_cycle()
        dag.resolve_template_files()
        dag.last_loaded = timezone.utcnow()
        for task in dag.tasks:
            settings.policy(task)

        subdags = dag.subdags
        try:
            for subdag in subdags:
                subdag.full_filepath = dag.full_filepath
                subdag.parent_dag = dag
                subdag.is_subdag = True
                self.bag_dag(subdag, parent_dag=dag, root_dag=root_dag)

            self.dags[dag.dag_id] = dag
            self.log.debug('Loaded DAG %s', dag)
        except AirflowDagCycleException as cycle_exception:
            self.log.exception('Exception bagging dag: %s', dag.dag_id)
            if dag == root_dag:
                for subdag in subdags:
                    if subdag.dag_id in self.dags:
                        del self.dags[subdag.dag_id]

            raise cycle_exception

    def collect_dags(self, dag_folder=None, only_if_updated=True, include_examples=configuration.conf.getboolean('core', 'LOAD_EXAMPLES'), safe_mode=configuration.conf.getboolean('core', 'DAG_DISCOVERY_SAFE_MODE')):
        """
        Given a file path or a folder, this method looks for python modules,
        imports them and adds them to the dagbag collection.

        Note that if a ``.airflowignore`` file is found while processing
        the directory, it will behave much like a ``.gitignore``,
        ignoring files that match any of the regex patterns specified
        in the file.

        **Note**: The patterns in .airflowignore are treated as
        un-anchored regexes, not shell-like glob patterns.
        """
        start_dttm = timezone.utcnow()
        dag_folder = dag_folder or self.dag_folder
        stats = []
        FileLoadStat = namedtuple('FileLoadStat', 'file duration dag_num task_num dags')
        dag_folder = correct_maybe_zipped(dag_folder)
        dags_by_name = {}
        for filepath in list_py_file_paths(dag_folder, safe_mode=safe_mode, include_examples=include_examples):
            try:
                ts = timezone.utcnow()
                found_dags = self.process_file(filepath,
                  only_if_updated=only_if_updated, safe_mode=safe_mode)
                dag_ids = [dag.dag_id for dag in found_dags]
                dag_id_names = str(dag_ids)
                td = timezone.utcnow() - ts
                td = td.total_seconds() + float(td.microseconds) / 1000000
                dags_by_name[dag_id_names] = dag_ids
                stats.append(FileLoadStat(filepath.replace(dag_folder, ''), td, len(found_dags), sum([len(dag.tasks) for dag in found_dags]), dag_id_names))
            except Exception as e:
                self.log.exception(e)

        Stats.gauge('collect_dags', (timezone.utcnow() - start_dttm).total_seconds(), 1)
        Stats.gauge('dagbag_size', len(self.dags), 1)
        Stats.gauge('dagbag_import_errors', len(self.import_errors), 1)
        self.dagbag_stats = sorted(stats,
          key=(lambda x: x.duration), reverse=True)
        for file_stat in self.dagbag_stats:
            dag_ids = dags_by_name[file_stat.dags]
            if file_stat.dag_num >= 1:
                dag_names = '_'.join(dag_ids)
                Stats.timing('dag.loading-duration.{}'.format(dag_names), file_stat.duration)

    def dagbag_report(self):
        """Prints a report around DagBag loading stats"""
        report = textwrap.dedent('\n\n        -------------------------------------------------------------------\n        DagBag loading stats for {dag_folder}\n        -------------------------------------------------------------------\n        Number of DAGs: {dag_num}\n        Total task number: {task_num}\n        DagBag parsing time: {duration}\n        {table}\n        ')
        stats = self.dagbag_stats
        return report.format(dag_folder=(self.dag_folder),
          duration=(sum([o.duration for o in stats])),
          dag_num=(sum([o.dag_num for o in stats])),
          task_num=(sum([o.task_num for o in stats])),
          table=(pprinttable(stats)))