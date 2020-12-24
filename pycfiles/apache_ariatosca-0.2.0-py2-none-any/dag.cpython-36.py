# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/models/dag.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 59550 bytes
from __future__ import print_function
import copy, functools, os, pickle, re, sys, traceback, warnings
from collections import OrderedDict, defaultdict
from datetime import timedelta, datetime
from typing import Union, Optional, Iterable, Dict, Type, Callable, List
import jinja2, pendulum, six
from croniter import croniter
from dateutil.relativedelta import relativedelta
from future.standard_library import install_aliases
from sqlalchemy import Column, String, Boolean, Integer, Text, func, or_
from airflow import configuration, settings, utils
from airflow.dag.base_dag import BaseDag
from airflow.exceptions import AirflowException, AirflowDagCycleException
from airflow.executors import LocalExecutor, get_default_executor
from airflow.models.base import Base, ID_LEN
from airflow.models.dagbag import DagBag
from airflow.models.dagpickle import DagPickle
from airflow.models.dagrun import DagRun
from airflow.models.taskinstance import TaskInstance, clear_task_instances
from airflow.utils import timezone
from airflow.utils.dates import cron_presets, date_range as utils_date_range
from airflow.utils.db import provide_session
from airflow.utils.helpers import validate_key
from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.utils.sqlalchemy import UtcDateTime, Interval
from airflow.utils.state import State
install_aliases()
ScheduleInterval = Union[(str, timedelta, relativedelta)]

def get_last_dagrun(dag_id, session, include_externally_triggered=False):
    """
    Returns the last dag run for a dag, None if there was none.
    Last dag run can be any type of run eg. scheduled or backfilled.
    Overridden DagRuns are ignored.
    """
    DR = DagRun
    query = session.query(DR).filter(DR.dag_id == dag_id)
    if not include_externally_triggered:
        query = query.filter(DR.external_trigger == False)
    query = query.order_by(DR.execution_date.desc())
    return query.first()


@functools.total_ordering
class DAG(BaseDag, LoggingMixin):
    """DAG"""
    _comps = {
     'dag_id',
     'task_ids',
     'parent_dag',
     'start_date',
     'schedule_interval',
     'full_filepath',
     'template_searchpath',
     'last_loaded'}

    def __init__(self, dag_id, description='', schedule_interval=timedelta(days=1), start_date=None, end_date=None, full_filepath=None, template_searchpath=None, template_undefined=jinja2.Undefined, user_defined_macros=None, user_defined_filters=None, default_args=None, concurrency=configuration.conf.getint('core', 'dag_concurrency'), max_active_runs=configuration.conf.getint('core', 'max_active_runs_per_dag'), dagrun_timeout=None, sla_miss_callback=None, default_view=None, orientation=configuration.conf.get('webserver', 'dag_orientation'), catchup=configuration.conf.getboolean('scheduler', 'catchup_by_default'), on_success_callback=None, on_failure_callback=None, doc_md=None, params=None, access_control=None, is_paused_upon_creation=None):
        self.user_defined_macros = user_defined_macros
        self.user_defined_filters = user_defined_filters
        self.default_args = copy.deepcopy(default_args or {})
        self.params = params or {}
        if 'params' in self.default_args:
            self.params.update(self.default_args['params'])
            del self.default_args['params']
        validate_key(dag_id)
        self._dag_id = dag_id
        self._full_filepath = full_filepath if full_filepath else ''
        self._concurrency = concurrency
        self._pickle_id = None
        self._description = description
        self.fileloc = sys._getframe().f_back.f_code.co_filename
        self.task_dict = dict()
        if start_date:
            if start_date.tzinfo:
                self.timezone = start_date.tzinfo
        if 'start_date' in self.default_args:
            if self.default_args['start_date']:
                if isinstance(self.default_args['start_date'], six.string_types):
                    self.default_args['start_date'] = timezone.parse(self.default_args['start_date'])
                self.timezone = self.default_args['start_date'].tzinfo
        if not hasattr(self, 'timezone') or not self.timezone:
            self.timezone = settings.TIMEZONE
        if 'end_date' in self.default_args:
            if self.default_args['end_date']:
                if isinstance(self.default_args['end_date'], six.string_types):
                    self.default_args['end_date'] = timezone.parse((self.default_args['end_date']), timezone=(self.timezone))
        self.start_date = timezone.convert_to_utc(start_date)
        self.end_date = timezone.convert_to_utc(end_date)
        if 'start_date' in self.default_args:
            self.default_args['start_date'] = timezone.convert_to_utc(self.default_args['start_date'])
        if 'end_date' in self.default_args:
            self.default_args['end_date'] = timezone.convert_to_utc(self.default_args['end_date'])
        else:
            self.schedule_interval = schedule_interval
            if isinstance(schedule_interval, six.string_types):
                if schedule_interval in cron_presets:
                    self._schedule_interval = cron_presets.get(schedule_interval)
            if schedule_interval == '@once':
                self._schedule_interval = None
            else:
                self._schedule_interval = schedule_interval
        if isinstance(template_searchpath, six.string_types):
            template_searchpath = [
             template_searchpath]
        self.template_searchpath = template_searchpath
        self.template_undefined = template_undefined
        self.parent_dag = None
        self.last_loaded = timezone.utcnow()
        self.safe_dag_id = dag_id.replace('.', '__dot__')
        self.max_active_runs = max_active_runs
        self.dagrun_timeout = dagrun_timeout
        self.sla_miss_callback = sla_miss_callback
        self._default_view = default_view
        self.orientation = orientation
        self.catchup = catchup
        self.is_subdag = False
        self.partial = False
        self.on_success_callback = on_success_callback
        self.on_failure_callback = on_failure_callback
        self.doc_md = doc_md
        self._old_context_manager_dags = []
        self._access_control = access_control
        self.is_paused_upon_creation = is_paused_upon_creation

    def __repr__(self):
        return '<DAG: {self.dag_id}>'.format(self=self)

    def __eq__(self, other):
        if type(self) == type(other):
            if self.dag_id == other.dag_id:
                return all(getattr(self, c, None) == getattr(other, c, None) for c in self._comps)
        return False

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        return self.dag_id < other.dag_id

    def __hash__(self):
        hash_components = [
         type(self)]
        for c in self._comps:
            if c == 'task_ids':
                val = tuple(self.task_dict.keys())
            else:
                val = getattr(self, c, None)
            try:
                hash(val)
                hash_components.append(val)
            except TypeError:
                hash_components.append(repr(val))

        return hash(tuple(hash_components))

    def __enter__(self):
        self._old_context_manager_dags.append(settings.CONTEXT_MANAGER_DAG)
        settings.CONTEXT_MANAGER_DAG = self
        return self

    def __exit__(self, _type, _value, _tb):
        settings.CONTEXT_MANAGER_DAG = self._old_context_manager_dags.pop()

    def get_default_view(self):
        """This is only there for backward compatible jinja2 templates"""
        if self._default_view is None:
            return configuration.conf.get('webserver', 'dag_default_view').lower()
        else:
            return self._default_view

    def date_range(self, start_date, num=None, end_date=timezone.utcnow()):
        if num:
            end_date = None
        return utils_date_range(start_date=start_date,
          end_date=end_date,
          num=num,
          delta=(self._schedule_interval))

    def is_fixed_time_schedule(self):
        """
        Figures out if the DAG schedule has a fixed time (e.g. 3 AM).

        :return: True if the schedule has a fixed time, False if not.
        """
        now = datetime.now()
        cron = croniter(self._schedule_interval, now)
        start = cron.get_next(datetime)
        cron_next = cron.get_next(datetime)
        if cron_next.minute == start.minute:
            if cron_next.hour == start.hour:
                return True
        return False

    def following_schedule(self, dttm):
        """
        Calculates the following schedule for this dag in UTC.

        :param dttm: utc datetime
        :return: utc datetime
        """
        if isinstance(self._schedule_interval, six.string_types):
            dttm = pendulum.instance(dttm)
            naive = timezone.make_naive(dttm, self.timezone)
            cron = croniter(self._schedule_interval, naive)
            if not self.is_fixed_time_schedule():
                delta = cron.get_next(datetime) - naive
                following = dttm.in_timezone(self.timezone).add_timedelta(delta)
            else:
                naive = cron.get_next(datetime)
                tz = pendulum.timezone(self.timezone.name)
                following = timezone.make_aware(naive, tz)
            return timezone.convert_to_utc(following)
        if self._schedule_interval is not None:
            return dttm + self._schedule_interval

    def previous_schedule(self, dttm):
        """
        Calculates the previous schedule for this dag in UTC

        :param dttm: utc datetime
        :return: utc datetime
        """
        if isinstance(self._schedule_interval, six.string_types):
            dttm = pendulum.instance(dttm)
            naive = timezone.make_naive(dttm, self.timezone)
            cron = croniter(self._schedule_interval, naive)
            if not self.is_fixed_time_schedule():
                delta = naive - cron.get_prev(datetime)
                previous = dttm.in_timezone(self.timezone).subtract_timedelta(delta)
            else:
                naive = cron.get_prev(datetime)
                tz = pendulum.timezone(self.timezone.name)
                previous = timezone.make_aware(naive, tz)
            return timezone.convert_to_utc(previous)
        if self._schedule_interval is not None:
            return dttm - self._schedule_interval

    def get_run_dates(self, start_date, end_date=None):
        """
        Returns a list of dates between the interval received as parameter using this
        dag's schedule interval. Returned dates can be used for execution dates.

        :param start_date: the start date of the interval
        :type start_date: datetime
        :param end_date: the end date of the interval, defaults to timezone.utcnow()
        :type end_date: datetime
        :return: a list of dates within the interval following the dag's schedule
        :rtype: list
        """
        run_dates = []
        using_start_date = start_date
        using_end_date = end_date
        using_start_date = using_start_date or min([t.start_date for t in self.tasks])
        using_end_date = using_end_date or timezone.utcnow()
        next_run_date = self.normalize_schedule(using_start_date) if not self.is_subdag else using_start_date
        while next_run_date and next_run_date <= using_end_date:
            run_dates.append(next_run_date)
            next_run_date = self.following_schedule(next_run_date)

        return run_dates

    def normalize_schedule(self, dttm):
        """
        Returns dttm + interval unless dttm is first interval then it returns dttm
        """
        following = self.following_schedule(dttm)
        if not following:
            return dttm
        else:
            if self.previous_schedule(following) != dttm:
                return following
            return dttm

    @provide_session
    def get_last_dagrun(self, session=None, include_externally_triggered=False):
        return get_last_dagrun((self.dag_id), session=session, include_externally_triggered=include_externally_triggered)

    @property
    def dag_id(self):
        return self._dag_id

    @dag_id.setter
    def dag_id(self, value):
        self._dag_id = value

    @property
    def full_filepath(self):
        return self._full_filepath

    @full_filepath.setter
    def full_filepath(self, value):
        self._full_filepath = value

    @property
    def concurrency(self):
        return self._concurrency

    @concurrency.setter
    def concurrency(self, value):
        self._concurrency = value

    @property
    def access_control(self):
        return self._access_control

    @access_control.setter
    def access_control(self, value):
        self._access_control = value

    @property
    def description(self):
        return self._description

    @property
    def pickle_id(self):
        return self._pickle_id

    @pickle_id.setter
    def pickle_id(self, value):
        self._pickle_id = value

    @property
    def tasks(self):
        return list(self.task_dict.values())

    @tasks.setter
    def tasks(self, val):
        raise AttributeError('DAG.tasks can not be modified. Use dag.add_task() instead.')

    @property
    def task_ids(self):
        return list(self.task_dict.keys())

    @property
    def filepath(self):
        """
        File location of where the dag object is instantiated
        """
        fn = self.full_filepath.replace(settings.DAGS_FOLDER + '/', '')
        fn = fn.replace(os.path.dirname(__file__) + '/', '')
        return fn

    @property
    def folder(self):
        """
        Folder location of where the dag object is instantiated
        """
        return os.path.dirname(self.full_filepath)

    @property
    def owner(self):
        """
        Return list of all owners found in DAG tasks.

        :return: Comma separated list of owners in DAG tasks
        :rtype: str
        """
        return ', '.join({t.owner for t in self.tasks})

    @provide_session
    def _get_concurrency_reached(self, session=None):
        TI = TaskInstance
        qry = session.query(func.count(TI.task_id)).filter(TI.dag_id == self.dag_id, TI.state == State.RUNNING)
        return qry.scalar() >= self.concurrency

    @property
    def concurrency_reached(self):
        """
        Returns a boolean indicating whether the concurrency limit for this DAG
        has been reached
        """
        return self._get_concurrency_reached()

    @provide_session
    def _get_is_paused(self, session=None):
        qry = session.query(DagModel).filter(DagModel.dag_id == self.dag_id)
        return qry.value('is_paused')

    @property
    def is_paused(self):
        """
        Returns a boolean indicating whether this DAG is paused
        """
        return self._get_is_paused()

    @provide_session
    def handle_callback(self, dagrun, success=True, reason=None, session=None):
        """
        Triggers the appropriate callback depending on the value of success, namely the
        on_failure_callback or on_success_callback. This method gets the context of a
        single TaskInstance part of this DagRun and passes that to the callable along
        with a 'reason', primarily to differentiate DagRun failures.

        .. note: The logs end up in
            ``$AIRFLOW_HOME/logs/scheduler/latest/PROJECT/DAG_FILE.py.log``

        :param dagrun: DagRun object
        :param success: Flag to specify if failure or success callback should be called
        :param reason: Completion reason
        :param session: Database session
        """
        callback = self.on_success_callback if success else self.on_failure_callback
        if callback:
            self.log.info('Executing dag callback function: {}'.format(callback))
            tis = dagrun.get_task_instances()
            ti = tis[(-1)]
            ti.task = self.get_task(ti.task_id)
            context = ti.get_template_context(session=session)
            context.update({'reason': reason})
            callback(context)

    def get_active_runs(self):
        """
        Returns a list of dag run execution dates currently running

        :return: List of execution dates
        """
        runs = DagRun.find(dag_id=(self.dag_id), state=(State.RUNNING))
        active_dates = []
        for run in runs:
            active_dates.append(run.execution_date)

        return active_dates

    @provide_session
    def get_num_active_runs(self, external_trigger=None, session=None):
        """
        Returns the number of active "running" dag runs

        :param external_trigger: True for externally triggered active dag runs
        :type external_trigger: bool
        :param session:
        :return: number greater than 0 for active dag runs
        """
        query = session.query(DagRun).filter(DagRun.dag_id == self.dag_id).filter(DagRun.state == State.RUNNING)
        if external_trigger is not None:
            query = query.filter(DagRun.external_trigger == external_trigger)
        return query.count()

    @provide_session
    def get_dagrun(self, execution_date, session=None):
        """
        Returns the dag run for a given execution date if it exists, otherwise
        none.

        :param execution_date: The execution date of the DagRun to find.
        :param session:
        :return: The DagRun if found, otherwise None.
        """
        dagrun = session.query(DagRun).filter(DagRun.dag_id == self.dag_id, DagRun.execution_date == execution_date).first()
        return dagrun

    @provide_session
    def get_dagruns_between(self, start_date, end_date, session=None):
        """
        Returns the list of dag runs between start_date (inclusive) and end_date (inclusive).

        :param start_date: The starting execution date of the DagRun to find.
        :param end_date: The ending execution date of the DagRun to find.
        :param session:
        :return: The list of DagRuns found.
        """
        dagruns = session.query(DagRun).filter(DagRun.dag_id == self.dag_id, DagRun.execution_date >= start_date, DagRun.execution_date <= end_date).all()
        return dagruns

    @provide_session
    def _get_latest_execution_date(self, session=None):
        return session.query(func.max(DagRun.execution_date)).filter(DagRun.dag_id == self.dag_id).scalar()

    @property
    def latest_execution_date(self):
        """
        Returns the latest date for which at least one dag run exists
        """
        return self._get_latest_execution_date()

    @property
    def subdags(self):
        """
        Returns a list of the subdag objects associated to this DAG
        """
        from airflow.operators.subdag_operator import SubDagOperator
        subdag_lst = []
        for task in self.tasks:
            if isinstance(task, SubDagOperator) or type(task).__name__ == 'SubDagOperator':
                subdag_lst.append(task.subdag)
                subdag_lst += task.subdag.subdags

        return subdag_lst

    def resolve_template_files(self):
        for t in self.tasks:
            t.resolve_template_files()

    def get_template_env(self):
        """
        Returns a jinja2 Environment while taking into account the DAGs
        template_searchpath, user_defined_macros and user_defined_filters
        """
        searchpath = [
         self.folder]
        if self.template_searchpath:
            searchpath += self.template_searchpath
        env = jinja2.Environment(loader=(jinja2.FileSystemLoader(searchpath)),
          undefined=(self.template_undefined),
          extensions=[
         'jinja2.ext.do'],
          cache_size=0)
        if self.user_defined_macros:
            env.globals.update(self.user_defined_macros)
        if self.user_defined_filters:
            env.filters.update(self.user_defined_filters)
        return env

    def set_dependency(self, upstream_task_id, downstream_task_id):
        """
        Simple utility method to set dependency between two tasks that
        already have been added to the DAG using add_task()
        """
        self.get_task(upstream_task_id).set_downstream(self.get_task(downstream_task_id))

    @provide_session
    def get_task_instances(self, start_date=None, end_date=None, state=None, session=None):
        if not start_date:
            start_date = (timezone.utcnow() - timedelta(30)).date()
            start_date = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))
        end_date = end_date or timezone.utcnow()
        tis = session.query(TaskInstance).filter(TaskInstance.dag_id == self.dag_id, TaskInstance.execution_date >= start_date, TaskInstance.execution_date <= end_date, TaskInstance.task_id.in_([t.task_id for t in self.tasks]))
        if state:
            tis = tis.filter(TaskInstance.state == state)
        tis = tis.order_by(TaskInstance.execution_date).all()
        return tis

    @property
    def roots(self):
        return [t for t in self.tasks if not t.downstream_list]

    def topological_sort(self):
        """
        Sorts tasks in topographical order, such that a task comes after any of its
        upstream dependencies.

        Heavily inspired by:
        http://blog.jupo.org/2012/04/06/topological-sorting-acyclic-directed-graphs/

        :return: list of tasks in topological order
        """
        graph_unsorted = OrderedDict((task.task_id, task) for task in self.tasks)
        graph_sorted = []
        if len(self.tasks) == 0:
            return tuple(graph_sorted)
        else:
            while graph_unsorted:
                acyclic = False
                for node in list(graph_unsorted.values()):
                    for edge in node.upstream_list:
                        if edge.task_id in graph_unsorted:
                            break
                    else:
                        acyclic = True
                        del graph_unsorted[node.task_id]
                        graph_sorted.append(node)

                if not acyclic:
                    raise AirflowException('A cyclic dependency occurred in dag: {}'.format(self.dag_id))

            return tuple(graph_sorted)

    @provide_session
    def set_dag_runs_state(self, state=State.RUNNING, session=None, start_date=None, end_date=None):
        query = session.query(DagRun).filter_by(dag_id=(self.dag_id))
        if start_date:
            query = query.filter(DagRun.execution_date >= start_date)
        if end_date:
            query = query.filter(DagRun.execution_date <= end_date)
        drs = query.all()
        dirty_ids = []
        for dr in drs:
            dr.state = state
            dirty_ids.append(dr.dag_id)

    @provide_session
    def clear(self, start_date=None, end_date=None, only_failed=False, only_running=False, confirm_prompt=False, include_subdags=True, include_parentdag=True, reset_dag_runs=True, dry_run=False, session=None, get_tis=False):
        """
        Clears a set of task instances associated with the current dag for
        a specified date range.
        """
        TI = TaskInstance
        tis = session.query(TI)
        if include_subdags:
            conditions = []
            for dag in self.subdags + [self]:
                conditions.append(TI.dag_id.like(dag.dag_id) & TI.task_id.in_(dag.task_ids))

            tis = tis.filter(or_(*conditions))
        else:
            tis = session.query(TI).filter(TI.dag_id == self.dag_id)
            tis = tis.filter(TI.task_id.in_(self.task_ids))
        if include_parentdag:
            if self.is_subdag:
                p_dag = self.parent_dag.sub_dag(task_regex=('^{}$'.format(self.dag_id.split('.')[1])),
                  include_upstream=False,
                  include_downstream=True)
                tis = tis.union(p_dag.clear(start_date=start_date,
                  end_date=end_date,
                  only_failed=only_failed,
                  only_running=only_running,
                  confirm_prompt=confirm_prompt,
                  include_subdags=include_subdags,
                  include_parentdag=False,
                  reset_dag_runs=reset_dag_runs,
                  get_tis=True,
                  session=session))
        if start_date:
            tis = tis.filter(TI.execution_date >= start_date)
        if end_date:
            tis = tis.filter(TI.execution_date <= end_date)
        if only_failed:
            tis = tis.filter(or_(TI.state == State.FAILED, TI.state == State.UPSTREAM_FAILED))
        if only_running:
            tis = tis.filter(TI.state == State.RUNNING)
        if get_tis:
            return tis
        if dry_run:
            tis = tis.all()
            session.expunge_all()
            return tis
        count = tis.count()
        do_it = True
        if count == 0:
            return 0
        else:
            if confirm_prompt:
                ti_list = '\n'.join([str(t) for t in tis])
                question = 'You are about to delete these {count} tasks:\n{ti_list}\n\nAre you sure? (yes/no): '.format(count=count,
                  ti_list=ti_list)
                do_it = utils.helpers.ask_yesno(question)
            else:
                if do_it:
                    clear_task_instances((tis.all()), session,
                      dag=self)
                    if reset_dag_runs:
                        self.set_dag_runs_state(session=session, start_date=start_date,
                          end_date=end_date)
                else:
                    count = 0
                    print('Bail. Nothing was cleared.')
            session.commit()
            return count

    @classmethod
    def clear_dags(cls, dags, start_date=None, end_date=None, only_failed=False, only_running=False, confirm_prompt=False, include_subdags=True, include_parentdag=False, reset_dag_runs=True, dry_run=False):
        all_tis = []
        for dag in dags:
            tis = dag.clear(start_date=start_date,
              end_date=end_date,
              only_failed=only_failed,
              only_running=only_running,
              confirm_prompt=False,
              include_subdags=include_subdags,
              include_parentdag=include_parentdag,
              reset_dag_runs=reset_dag_runs,
              dry_run=True)
            all_tis.extend(tis)

        if dry_run:
            return all_tis
        count = len(all_tis)
        do_it = True
        if count == 0:
            print('Nothing to clear.')
            return 0
        else:
            if confirm_prompt:
                ti_list = '\n'.join([str(t) for t in all_tis])
                question = 'You are about to delete these {} tasks:\n{}\n\nAre you sure? (yes/no): '.format(count, ti_list)
                do_it = utils.helpers.ask_yesno(question)
            else:
                if do_it:
                    for dag in dags:
                        dag.clear(start_date=start_date, end_date=end_date,
                          only_failed=only_failed,
                          only_running=only_running,
                          confirm_prompt=False,
                          include_subdags=include_subdags,
                          reset_dag_runs=reset_dag_runs,
                          dry_run=False)

                else:
                    count = 0
                    print('Bail. Nothing was cleared.')
            return count

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in list(self.__dict__.items()):
            if k not in ('user_defined_macros', 'user_defined_filters', 'params'):
                setattr(result, k, copy.deepcopy(v, memo))

        result.user_defined_macros = self.user_defined_macros
        result.user_defined_filters = self.user_defined_filters
        result.params = self.params
        return result

    def sub_dag(self, task_regex, include_downstream=False, include_upstream=True):
        """
        Returns a subset of the current dag as a deep copy of the current dag
        based on a regex that should match one or many tasks, and includes
        upstream and downstream neighbours based on the flag passed.
        """
        task_dict = self.task_dict
        self.task_dict = {}
        dag = copy.deepcopy(self)
        self.task_dict = task_dict
        regex_match = [t for t in self.tasks if re.findall(task_regex, t.task_id)]
        also_include = []
        for t in regex_match:
            if include_downstream:
                also_include += t.get_flat_relatives(upstream=False)
            if include_upstream:
                also_include += t.get_flat_relatives(upstream=True)

        dag.task_dict = {t.task_id:copy.deepcopy(t, {id(t.dag): t.dag}) for t in regex_match + also_include}
        for t in dag.tasks:
            t._upstream_task_ids = t._upstream_task_ids.intersection(dag.task_dict.keys())
            t._downstream_task_ids = t._downstream_task_ids.intersection(dag.task_dict.keys())

        if len(dag.tasks) < len(self.tasks):
            dag.partial = True
        return dag

    def has_task(self, task_id):
        return task_id in (t.task_id for t in self.tasks)

    def get_task(self, task_id):
        if task_id in self.task_dict:
            return self.task_dict[task_id]
        raise AirflowException('Task {task_id} not found'.format(task_id=task_id))

    def pickle_info(self):
        d = dict()
        d['is_picklable'] = True
        try:
            dttm = timezone.utcnow()
            pickled = pickle.dumps(self)
            d['pickle_len'] = len(pickled)
            d['pickling_duration'] = '{}'.format(timezone.utcnow() - dttm)
        except Exception as e:
            self.log.debug(e)
            d['is_picklable'] = False
            d['stacktrace'] = traceback.format_exc()

        return d

    @provide_session
    def pickle(self, session=None):
        dag = session.query(DagModel).filter(DagModel.dag_id == self.dag_id).first()
        dp = None
        if dag:
            if dag.pickle_id:
                dp = session.query(DagPickle).filter(DagPickle.id == dag.pickle_id).first()
        if not dp or dp.pickle != self:
            dp = DagPickle(dag=self)
            session.add(dp)
            self.last_pickled = timezone.utcnow()
            session.commit()
            self.pickle_id = dp.id
        return dp

    def tree_view(self):
        """
        Shows an ascii tree representation of the DAG
        """

        def get_downstream(task, level=0):
            print(' ' * level * 4 + str(task))
            level += 1
            for t in task.upstream_list:
                get_downstream(t, level)

        for t in self.roots:
            get_downstream(t)

    def add_task(self, task):
        """
        Add a task to the DAG

        :param task: the task you want to add
        :type task: task
        """
        if not self.start_date:
            if not task.start_date:
                raise AirflowException('Task is missing the start_date parameter')
            else:
                if not task.start_date:
                    task.start_date = self.start_date
                else:
                    if self.start_date:
                        task.start_date = max(task.start_date, self.start_date)
            task.end_date = task.end_date or self.end_date
        else:
            if task.end_date:
                if self.end_date:
                    task.end_date = min(task.end_date, self.end_date)
            if task.task_id in self.task_dict:
                warnings.warn(('The requested task could not be added to the DAG because a task with task_id {} is already in the DAG. Starting in Airflow 2.0, trying to overwrite a task will raise an exception.'.format(task.task_id)),
                  category=PendingDeprecationWarning)
            else:
                self.task_dict[task.task_id] = task
                task.dag = self
        self.task_count = len(self.task_dict)

    def add_tasks(self, tasks):
        """
        Add a list of tasks to the DAG

        :param tasks: a lit of tasks you want to add
        :type tasks: list of tasks
        """
        for task in tasks:
            self.add_task(task)

    def run(self, start_date=None, end_date=None, mark_success=False, local=False, executor=None, donot_pickle=configuration.conf.getboolean('core', 'donot_pickle'), ignore_task_deps=False, ignore_first_depends_on_past=False, pool=None, delay_on_limit_secs=1.0, verbose=False, conf=None, rerun_failed_tasks=False, run_backwards=False):
        """
        Runs the DAG.

        :param start_date: the start date of the range to run
        :type start_date: datetime.datetime
        :param end_date: the end date of the range to run
        :type end_date: datetime.datetime
        :param mark_success: True to mark jobs as succeeded without running them
        :type mark_success: bool
        :param local: True to run the tasks using the LocalExecutor
        :type local: bool
        :param executor: The executor instance to run the tasks
        :type executor: airflow.executor.BaseExecutor
        :param donot_pickle: True to avoid pickling DAG object and send to workers
        :type donot_pickle: bool
        :param ignore_task_deps: True to skip upstream tasks
        :type ignore_task_deps: bool
        :param ignore_first_depends_on_past: True to ignore depends_on_past
            dependencies for the first set of tasks only
        :type ignore_first_depends_on_past: bool
        :param pool: Resource pool to use
        :type pool: str
        :param delay_on_limit_secs: Time in seconds to wait before next attempt to run
            dag run when max_active_runs limit has been reached
        :type delay_on_limit_secs: float
        :param verbose: Make logging output more verbose
        :type verbose: bool
        :param conf: user defined dictionary passed from CLI
        :type conf: dict
        :param rerun_failed_tasks:
        :type: bool
        :param run_backwards:
        :type: bool

        """
        from airflow.jobs import BackfillJob
        if not executor:
            if local:
                executor = LocalExecutor()
        if not executor:
            executor = get_default_executor()
        job = BackfillJob(self,
          start_date=start_date,
          end_date=end_date,
          mark_success=mark_success,
          executor=executor,
          donot_pickle=donot_pickle,
          ignore_task_deps=ignore_task_deps,
          ignore_first_depends_on_past=ignore_first_depends_on_past,
          pool=pool,
          delay_on_limit_secs=delay_on_limit_secs,
          verbose=verbose,
          conf=conf,
          rerun_failed_tasks=rerun_failed_tasks,
          run_backwards=run_backwards)
        job.run()

    def cli(self):
        """
        Exposes a CLI specific to this DAG
        """
        from airflow.bin import cli
        parser = cli.CLIFactory.get_parser(dag_parser=True)
        args = parser.parse_args()
        args.func(args, self)

    @provide_session
    def create_dagrun(self, run_id, state, execution_date=None, start_date=None, external_trigger=False, conf=None, session=None):
        """
        Creates a dag run from this dag including the tasks associated with this dag.
        Returns the dag run.

        :param run_id: defines the the run id for this dag run
        :type run_id: str
        :param execution_date: the execution date of this dag run
        :type execution_date: datetime.datetime
        :param state: the state of the dag run
        :type state: airflow.utils.state.State
        :param start_date: the date this dag run should be evaluated
        :type start_date: datetime
        :param external_trigger: whether this dag run is externally triggered
        :type external_trigger: bool
        :param session: database session
        :type session: sqlalchemy.orm.session.Session
        """
        run = DagRun(dag_id=(self.dag_id),
          run_id=run_id,
          execution_date=execution_date,
          start_date=start_date,
          external_trigger=external_trigger,
          conf=conf,
          state=state)
        session.add(run)
        session.commit()
        run.dag = self
        run.verify_integrity(session=session)
        run.refresh_from_db()
        return run

    @provide_session
    def sync_to_db(self, owner=None, sync_time=None, session=None):
        """
        Save attributes about this DAG to the DB. Note that this method
        can be called for both DAGs and SubDAGs. A SubDag is actually a
        SubDagOperator.

        :param dag: the DAG object to save to the DB
        :type dag: airflow.models.DAG
        :param sync_time: The time that the DAG should be marked as sync'ed
        :type sync_time: datetime
        :return: None
        """
        if owner is None:
            owner = self.owner
        if sync_time is None:
            sync_time = timezone.utcnow()
        orm_dag = session.query(DagModel).filter(DagModel.dag_id == self.dag_id).first()
        if not orm_dag:
            orm_dag = DagModel(dag_id=(self.dag_id))
            if self.is_paused_upon_creation is not None:
                orm_dag.is_paused = self.is_paused_upon_creation
            self.log.info('Creating ORM DAG for %s', self.dag_id)
        orm_dag.fileloc = self.parent_dag.fileloc if self.is_subdag else self.fileloc
        orm_dag.is_subdag = self.is_subdag
        orm_dag.owners = owner
        orm_dag.is_active = True
        orm_dag.last_scheduler_run = sync_time
        orm_dag.default_view = self._default_view
        orm_dag.description = self.description
        orm_dag.schedule_interval = self.schedule_interval
        session.merge(orm_dag)
        session.commit()
        for subdag in self.subdags:
            subdag.sync_to_db(owner=owner, sync_time=sync_time, session=session)

    @staticmethod
    @provide_session
    def deactivate_unknown_dags(active_dag_ids, session=None):
        """
        Given a list of known DAGs, deactivate any other DAGs that are
        marked as active in the ORM

        :param active_dag_ids: list of DAG IDs that are active
        :type active_dag_ids: list[unicode]
        :return: None
        """
        if len(active_dag_ids) == 0:
            return
        for dag in session.query(DagModel).filter(~DagModel.dag_id.in_(active_dag_ids)).all():
            dag.is_active = False
            session.merge(dag)

        session.commit()

    @staticmethod
    @provide_session
    def deactivate_stale_dags(expiration_date, session=None):
        """
        Deactivate any DAGs that were last touched by the scheduler before
        the expiration date. These DAGs were likely deleted.

        :param expiration_date: set inactive DAGs that were touched before this
            time
        :type expiration_date: datetime
        :return: None
        """
        log = LoggingMixin().log
        for dag in session.query(DagModel).filter(DagModel.last_scheduler_run < expiration_date, DagModel.is_active).all():
            log.info('Deactivating DAG ID %s since it was last touched by the scheduler at %s', dag.dag_id, dag.last_scheduler_run.isoformat())
            dag.is_active = False
            session.merge(dag)
            session.commit()

    @staticmethod
    @provide_session
    def get_num_task_instances(dag_id, task_ids=None, states=None, session=None):
        """
        Returns the number of task instances in the given DAG.

        :param session: ORM session
        :param dag_id: ID of the DAG to get the task concurrency of
        :type dag_id: unicode
        :param task_ids: A list of valid task IDs for the given DAG
        :type task_ids: list[unicode]
        :param states: A list of states to filter by if supplied
        :type states: list[state]
        :return: The number of running tasks
        :rtype: int
        """
        qry = session.query(func.count(TaskInstance.task_id)).filter(TaskInstance.dag_id == dag_id)
        if task_ids:
            qry = qry.filter(TaskInstance.task_id.in_(task_ids))
        if states is not None:
            if None in states:
                qry = qry.filter(or_(TaskInstance.state.in_(states), TaskInstance.state.is_(None)))
            else:
                qry = qry.filter(TaskInstance.state.in_(states))
        return qry.scalar()

    def test_cycle(self):
        """
        Check to see if there are any cycles in the DAG. Returns False if no cycle found,
        otherwise raises exception.
        """
        from airflow.models.dagbag import DagBag
        visit_map = defaultdict(int)
        for task_id in self.task_dict.keys():
            if visit_map[task_id] == DagBag.CYCLE_NEW:
                self._test_cycle_helper(visit_map, task_id)

        return False

    def _test_cycle_helper(self, visit_map, task_id):
        """
        Checks if a cycle exists from the input task using DFS traversal
        """
        from airflow.models.dagbag import DagBag
        if visit_map[task_id] == DagBag.CYCLE_DONE:
            return False
        visit_map[task_id] = DagBag.CYCLE_IN_PROGRESS
        task = self.task_dict[task_id]
        for descendant_id in task.get_direct_relative_ids():
            if visit_map[descendant_id] == DagBag.CYCLE_IN_PROGRESS:
                msg = 'Cycle detected in DAG. Faulty task: {0} to {1}'.format(task_id, descendant_id)
                raise AirflowDagCycleException(msg)
            else:
                self._test_cycle_helper(visit_map, descendant_id)

        visit_map[task_id] = DagBag.CYCLE_DONE


class DagModel(Base):
    __tablename__ = 'dag'
    dag_id = Column((String(ID_LEN)), primary_key=True)
    is_paused_at_creation = configuration.conf.getboolean('core', 'dags_are_paused_at_creation')
    is_paused = Column(Boolean, default=is_paused_at_creation)
    is_subdag = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    last_scheduler_run = Column(UtcDateTime)
    last_pickled = Column(UtcDateTime)
    last_expired = Column(UtcDateTime)
    scheduler_lock = Column(Boolean)
    pickle_id = Column(Integer)
    fileloc = Column(String(2000))
    owners = Column(String(2000))
    description = Column(Text)
    default_view = Column(String(25))
    schedule_interval = Column(Interval)

    def __repr__(self):
        return '<DAG: {self.dag_id}>'.format(self=self)

    @property
    def timezone(self):
        return settings.TIMEZONE

    @staticmethod
    @provide_session
    def get_dagmodel(dag_id, session=None):
        return session.query(DagModel).filter(DagModel.dag_id == dag_id).first()

    @classmethod
    @provide_session
    def get_current(cls, dag_id, session=None):
        return session.query(cls).filter(cls.dag_id == dag_id).first()

    def get_default_view(self):
        if self.default_view is None:
            return configuration.conf.get('webserver', 'dag_default_view').lower()
        else:
            return self.default_view

    @provide_session
    def get_last_dagrun(self, session=None, include_externally_triggered=False):
        return get_last_dagrun((self.dag_id), session=session, include_externally_triggered=include_externally_triggered)

    @property
    def safe_dag_id(self):
        return self.dag_id.replace('.', '__dot__')

    def get_dag(self):
        return DagBag(dag_folder=(self.fileloc)).get_dag(self.dag_id)

    @provide_session
    def create_dagrun(self, run_id, state, execution_date, start_date=None, external_trigger=False, conf=None, session=None):
        """
        Creates a dag run from this dag including the tasks associated with this dag.
        Returns the dag run.

        :param run_id: defines the the run id for this dag run
        :type run_id: str
        :param execution_date: the execution date of this dag run
        :type execution_date: datetime.datetime
        :param state: the state of the dag run
        :type state: airflow.utils.state.State
        :param start_date: the date this dag run should be evaluated
        :type start_date: datetime.datetime
        :param external_trigger: whether this dag run is externally triggered
        :type external_trigger: bool
        :param session: database session
        :type session: sqlalchemy.orm.session.Session
        """
        return self.get_dag().create_dagrun(run_id=run_id, state=state,
          execution_date=execution_date,
          start_date=start_date,
          external_trigger=external_trigger,
          conf=conf,
          session=session)

    @provide_session
    def set_is_paused(self, is_paused, including_subdags=True, session=None):
        """
        Pause/Un-pause a DAG.

        :param is_paused: Is the DAG paused
        :param including_subdags: whether to include the DAG's subdags
        :param session: session
        """
        dag_ids = [
         self.dag_id]
        if including_subdags:
            subdags = self.get_dag().subdags
            dag_ids.extend([subdag.dag_id for subdag in subdags])
        dag_models = session.query(DagModel).filter(DagModel.dag_id.in_(dag_ids)).all()
        try:
            for dag_model in dag_models:
                dag_model.is_paused = is_paused

            session.commit()
        except Exception:
            session.rollback()
            raise