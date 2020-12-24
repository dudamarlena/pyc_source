# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/models/baseoperator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 39393 bytes
from abc import ABCMeta, abstractmethod
from cached_property import cached_property
import copy, functools, logging, sys, warnings
from datetime import timedelta, datetime
from typing import Iterable, Optional, Dict, Callable, Set
import jinja2, six
from airflow import configuration, settings
from airflow.exceptions import AirflowException
from airflow.lineage import prepare_lineage, apply_lineage, DataSet
from airflow.models.dag import DAG
from airflow.models.pool import Pool
from airflow.models.taskinstance import TaskInstance, clear_task_instances
from airflow.models.xcom import XCOM_RETURN_KEY
from airflow.ti_deps.deps.not_in_retry_period_dep import NotInRetryPeriodDep
from airflow.ti_deps.deps.prev_dagrun_dep import PrevDagrunDep
from airflow.ti_deps.deps.trigger_rule_dep import TriggerRuleDep
from airflow.utils import timezone
from airflow.utils.db import provide_session
from airflow.utils.decorators import apply_defaults
from airflow.utils.helpers import validate_key
from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.utils.operator_resources import Resources
from airflow.utils.trigger_rule import TriggerRule
from airflow.utils.weight_rule import WeightRule

@functools.total_ordering
class BaseOperator(LoggingMixin):
    __doc__ = '\n    Abstract base class for all operators. Since operators create objects that\n    become nodes in the dag, BaseOperator contains many recursive methods for\n    dag crawling behavior. To derive this class, you are expected to override\n    the constructor as well as the \'execute\' method.\n\n    Operators derived from this class should perform or trigger certain tasks\n    synchronously (wait for completion). Example of operators could be an\n    operator that runs a Pig job (PigOperator), a sensor operator that\n    waits for a partition to land in Hive (HiveSensorOperator), or one that\n    moves data from Hive to MySQL (Hive2MySqlOperator). Instances of these\n    operators (tasks) target specific operations, running specific scripts,\n    functions or data transfers.\n\n    This class is abstract and shouldn\'t be instantiated. Instantiating a\n    class derived from this one results in the creation of a task object,\n    which ultimately becomes a node in DAG objects. Task dependencies should\n    be set by using the set_upstream and/or set_downstream methods.\n\n    :param task_id: a unique, meaningful id for the task\n    :type task_id: str\n    :param owner: the owner of the task, using the unix username is recommended\n    :type owner: str\n    :param retries: the number of retries that should be performed before\n        failing the task\n    :type retries: int\n    :param retry_delay: delay between retries\n    :type retry_delay: datetime.timedelta\n    :param retry_exponential_backoff: allow progressive longer waits between\n        retries by using exponential backoff algorithm on retry delay (delay\n        will be converted into seconds)\n    :type retry_exponential_backoff: bool\n    :param max_retry_delay: maximum delay interval between retries\n    :type max_retry_delay: datetime.timedelta\n    :param start_date: The ``start_date`` for the task, determines\n        the ``execution_date`` for the first task instance. The best practice\n        is to have the start_date rounded\n        to your DAG\'s ``schedule_interval``. Daily jobs have their start_date\n        some day at 00:00:00, hourly jobs have their start_date at 00:00\n        of a specific hour. Note that Airflow simply looks at the latest\n        ``execution_date`` and adds the ``schedule_interval`` to determine\n        the next ``execution_date``. It is also very important\n        to note that different tasks\' dependencies\n        need to line up in time. If task A depends on task B and their\n        start_date are offset in a way that their execution_date don\'t line\n        up, A\'s dependencies will never be met. If you are looking to delay\n        a task, for example running a daily task at 2AM, look into the\n        ``TimeSensor`` and ``TimeDeltaSensor``. We advise against using\n        dynamic ``start_date`` and recommend using fixed ones. Read the\n        FAQ entry about start_date for more information.\n    :type start_date: datetime.datetime\n    :param end_date: if specified, the scheduler won\'t go beyond this date\n    :type end_date: datetime.datetime\n    :param depends_on_past: when set to true, task instances will run\n        sequentially while relying on the previous task\'s schedule to\n        succeed. The task instance for the start_date is allowed to run.\n    :type depends_on_past: bool\n    :param wait_for_downstream: when set to true, an instance of task\n        X will wait for tasks immediately downstream of the previous instance\n        of task X to finish successfully before it runs. This is useful if the\n        different instances of a task X alter the same asset, and this asset\n        is used by tasks downstream of task X. Note that depends_on_past\n        is forced to True wherever wait_for_downstream is used.\n    :type wait_for_downstream: bool\n    :param queue: which queue to target when running this job. Not\n        all executors implement queue management, the CeleryExecutor\n        does support targeting specific queues.\n    :type queue: str\n    :param dag: a reference to the dag the task is attached to (if any)\n    :type dag: airflow.models.DAG\n    :param priority_weight: priority weight of this task against other task.\n        This allows the executor to trigger higher priority tasks before\n        others when things get backed up. Set priority_weight as a higher\n        number for more important tasks.\n    :type priority_weight: int\n    :param weight_rule: weighting method used for the effective total\n        priority weight of the task. Options are:\n        ``{ downstream | upstream | absolute }`` default is ``downstream``\n        When set to ``downstream`` the effective weight of the task is the\n        aggregate sum of all downstream descendants. As a result, upstream\n        tasks will have higher weight and will be scheduled more aggressively\n        when using positive weight values. This is useful when you have\n        multiple dag run instances and desire to have all upstream tasks to\n        complete for all runs before each dag can continue processing\n        downstream tasks. When set to ``upstream`` the effective weight is the\n        aggregate sum of all upstream ancestors. This is the opposite where\n        downtream tasks have higher weight and will be scheduled more\n        aggressively when using positive weight values. This is useful when you\n        have multiple dag run instances and prefer to have each dag complete\n        before starting upstream tasks of other dags.  When set to\n        ``absolute``, the effective weight is the exact ``priority_weight``\n        specified without additional weighting. You may want to do this when\n        you know exactly what priority weight each task should have.\n        Additionally, when set to ``absolute``, there is bonus effect of\n        significantly speeding up the task creation process as for very large\n        DAGS. Options can be set as string or using the constants defined in\n        the static class ``airflow.utils.WeightRule``\n    :type weight_rule: str\n    :param pool: the slot pool this task should run in, slot pools are a\n        way to limit concurrency for certain tasks\n    :type pool: str\n    :param sla: time by which the job is expected to succeed. Note that\n        this represents the ``timedelta`` after the period is closed. For\n        example if you set an SLA of 1 hour, the scheduler would send an email\n        soon after 1:00AM on the ``2016-01-02`` if the ``2016-01-01`` instance\n        has not succeeded yet.\n        The scheduler pays special attention for jobs with an SLA and\n        sends alert\n        emails for sla misses. SLA misses are also recorded in the database\n        for future reference. All tasks that share the same SLA time\n        get bundled in a single email, sent soon after that time. SLA\n        notification are sent once and only once for each task instance.\n    :type sla: datetime.timedelta\n    :param execution_timeout: max time allowed for the execution of\n        this task instance, if it goes beyond it will raise and fail.\n    :type execution_timeout: datetime.timedelta\n    :param on_failure_callback: a function to be called when a task instance\n        of this task fails. a context dictionary is passed as a single\n        parameter to this function. Context contains references to related\n        objects to the task instance and is documented under the macros\n        section of the API.\n    :type on_failure_callback: callable\n    :param on_retry_callback: much like the ``on_failure_callback`` except\n        that it is executed when retries occur.\n    :type on_retry_callback: callable\n    :param on_success_callback: much like the ``on_failure_callback`` except\n        that it is executed when the task succeeds.\n    :type on_success_callback: callable\n    :param trigger_rule: defines the rule by which dependencies are applied\n        for the task to get triggered. Options are:\n        ``{ all_success | all_failed | all_done | one_success |\n        one_failed | none_failed | none_skipped | dummy}``\n        default is ``all_success``. Options can be set as string or\n        using the constants defined in the static class\n        ``airflow.utils.TriggerRule``\n    :type trigger_rule: str\n    :param resources: A map of resource parameter names (the argument names of the\n        Resources constructor) to their values.\n    :type resources: dict\n    :param run_as_user: unix username to impersonate while running the task\n    :type run_as_user: str\n    :param task_concurrency: When set, a task will be able to limit the concurrent\n        runs across execution_dates\n    :type task_concurrency: int\n    :param executor_config: Additional task-level configuration parameters that are\n        interpreted by a specific executor. Parameters are namespaced by the name of\n        executor.\n\n        **Example**: to run this task in a specific docker container through\n        the KubernetesExecutor ::\n\n            MyOperator(...,\n                executor_config={\n                "KubernetesExecutor":\n                    {"image": "myCustomDockerImage"}\n                    }\n            )\n\n    :type executor_config: dict\n    :param do_xcom_push: if True, an XCom is pushed containing the Operator\'s\n        result\n    :type do_xcom_push: bool\n    '
    template_fields = []
    template_ext = []
    ui_color = '#fff'
    ui_fgcolor = '#000'
    _base_operator_shallow_copy_attrs = ('user_defined_macros', 'user_defined_filters',
                                         'params', '_log')
    shallow_copy_attrs = ()
    operator_extra_links = ()
    _comps = {
     'task_id',
     'dag_id',
     'owner',
     'email',
     'email_on_retry',
     'retry_delay',
     'retry_exponential_backoff',
     'max_retry_delay',
     'start_date',
     'schedule_interval',
     'depends_on_past',
     'wait_for_downstream',
     'priority_weight',
     'sla',
     'execution_timeout',
     'on_failure_callback',
     'on_success_callback',
     'on_retry_callback',
     'do_xcom_push'}

    @apply_defaults
    def __init__(self, task_id, owner, email, email_on_retry, email_on_failure, retries, retry_delay, retry_exponential_backoff, max_retry_delay, start_date, end_date, schedule_interval, depends_on_past, wait_for_downstream, dag, params, default_args, priority_weight, weight_rule, queue, pool, sla, execution_timeout, on_failure_callback, on_success_callback, on_retry_callback, trigger_rule, resources, run_as_user, task_concurrency, executor_config, do_xcom_push, inlets=configuration.conf.get('operators', 'DEFAULT_OWNER')NoneTrueTrue0timedelta(seconds=300)FalseNoneNoneNoneNoneFalseFalseNoneNoneNone1WeightRule.DOWNSTREAMconfiguration.conf.get('celery', 'default_queue')Pool.DEFAULT_POOL_NAMENoneNoneNoneNoneNoneTriggerRule.ALL_SUCCESSNoneNoneNoneNoneTrueNone, outlets=None, *args, **kwargs):
        if args or kwargs:
            warnings.warn('Invalid arguments were passed to {c} (task_id: {t}). Support for passing such arguments will be dropped in Airflow 2.0. Invalid arguments were:\n*args: {a}\n**kwargs: {k}'.format(c=(self.__class__.__name__),
              a=args,
              k=kwargs,
              t=task_id),
              category=PendingDeprecationWarning,
              stacklevel=3)
        else:
            validate_key(task_id)
            self.task_id = task_id
            self.owner = owner
            self.email = email
            self.email_on_retry = email_on_retry
            self.email_on_failure = email_on_failure
            self.start_date = start_date
            if start_date:
                if not isinstance(start_date, datetime):
                    self.log.warning("start_date for %s isn't datetime.datetime", self)
            if start_date:
                self.start_date = timezone.convert_to_utc(start_date)
            self.end_date = end_date
            if end_date:
                self.end_date = timezone.convert_to_utc(end_date)
            if not TriggerRule.is_valid(trigger_rule):
                raise AirflowException("The trigger_rule must be one of {all_triggers},'{d}.{t}'; received '{tr}'.".format(all_triggers=(TriggerRule.all_triggers()),
                  d=(dag.dag_id if dag else ''),
                  t=task_id,
                  tr=trigger_rule))
            self.trigger_rule = trigger_rule
            self.depends_on_past = depends_on_past
            self.wait_for_downstream = wait_for_downstream
            if wait_for_downstream:
                self.depends_on_past = True
            if schedule_interval:
                self.log.warning('schedule_interval is used for %s, though it has been deprecated as a task parameter, you need to specify it as a DAG parameter instead', self)
            self._schedule_interval = schedule_interval
            self.retries = retries
            self.queue = queue
            self.pool = pool
            self.sla = sla
            self.execution_timeout = execution_timeout
            self.on_failure_callback = on_failure_callback
            self.on_success_callback = on_success_callback
            self.on_retry_callback = on_retry_callback
            if isinstance(retry_delay, timedelta):
                self.retry_delay = retry_delay
            else:
                self.log.debug("Retry_delay isn't timedelta object, assuming secs")
                self.retry_delay = timedelta(seconds=retry_delay)
            self.retry_exponential_backoff = retry_exponential_backoff
            self.max_retry_delay = max_retry_delay
            self.params = params or {}
            self.priority_weight = priority_weight
            if not WeightRule.is_valid(weight_rule):
                raise AirflowException("The weight_rule must be one of {all_weight_rules},'{d}.{t}'; received '{tr}'.".format(all_weight_rules=(WeightRule.all_weight_rules),
                  d=(dag.dag_id if dag else ''),
                  t=task_id,
                  tr=weight_rule))
            self.weight_rule = weight_rule
            self.resources = Resources(*resources) if resources is not None else None
            self.run_as_user = run_as_user
            self.task_concurrency = task_concurrency
            self.executor_config = executor_config or {}
            self.do_xcom_push = do_xcom_push
            self._upstream_task_ids = set()
            self._downstream_task_ids = set()
            if not dag:
                if settings.CONTEXT_MANAGER_DAG:
                    dag = settings.CONTEXT_MANAGER_DAG
            if dag:
                self.dag = dag
            self._log = logging.getLogger('airflow.task.operators')
            self.inlets = []
            self.outlets = []
            self.lineage_data = None
            self._inlets = {'auto':False, 
             'task_ids':[],  'datasets':[]}
            self._outlets = {'datasets': []}
            if inlets:
                self._inlets.update(inlets)
            if outlets:
                self._outlets.update(outlets)

    def __eq__(self, other):
        if type(self) == type(other):
            if self.task_id == other.task_id:
                return all(self.__dict__.get(c, None) == other.__dict__.get(c, None) for c in self._comps)
        return False

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        return self.task_id < other.task_id

    def __hash__(self):
        hash_components = [
         type(self)]
        for c in self._comps:
            val = getattr(self, c, None)
            try:
                hash(val)
                hash_components.append(val)
            except TypeError:
                hash_components.append(repr(val))

        return hash(tuple(hash_components))

    def __rshift__(self, other):
        """
        Implements Self >> Other == self.set_downstream(other)

        If "Other" is a DAG, the DAG is assigned to the Operator.
        """
        if isinstance(other, DAG):
            if not (self.has_dag() and self.dag is other):
                self.dag = other
        else:
            self.set_downstream(other)
        return other

    def __lshift__(self, other):
        """
        Implements Self << Other == self.set_upstream(other)

        If "Other" is a DAG, the DAG is assigned to the Operator.
        """
        if isinstance(other, DAG):
            if not (self.has_dag() and self.dag is other):
                self.dag = other
        else:
            self.set_upstream(other)
        return other

    def __rrshift__(self, other):
        """
        Called for [DAG] >> [Operator] because DAGs don't have
        __rshift__ operators.
        """
        self.__lshift__(other)
        return self

    def __rlshift__(self, other):
        """
        Called for [DAG] << [Operator] because DAGs don't have
        __lshift__ operators.
        """
        self.__rshift__(other)
        return self

    @property
    def dag(self):
        """
        Returns the Operator's DAG if set, otherwise raises an error
        """
        if self.has_dag():
            return self._dag
        raise AirflowException('Operator {} has not been assigned to a DAG yet'.format(self))

    @dag.setter
    def dag(self, dag):
        """
        Operators can be assigned to one DAG, one time. Repeat assignments to
        that same DAG are ok.
        """
        if not isinstance(dag, DAG):
            raise TypeError('Expected DAG; received {}'.format(dag.__class__.__name__))
        else:
            if self.has_dag():
                if self.dag is not dag:
                    raise AirflowException('The DAG assigned to {} can not be changed.'.format(self))
        if self.task_id not in dag.task_dict:
            dag.add_task(self)
        self._dag = dag

    def has_dag(self):
        """
        Returns True if the Operator has been assigned to a DAG.
        """
        return getattr(self, '_dag', None) is not None

    @property
    def dag_id(self):
        if self.has_dag():
            return self.dag.dag_id
        else:
            return 'adhoc_' + self.owner

    @property
    def deps(self):
        """
        Returns the list of dependencies for the operator. These differ from execution
        context dependencies in that they are specific to tasks and can be
        extended/overridden by subclasses.
        """
        return {
         NotInRetryPeriodDep(),
         PrevDagrunDep(),
         TriggerRuleDep()}

    @property
    def schedule_interval(self):
        """
        The schedule interval of the DAG always wins over individual tasks so
        that tasks within a DAG always line up. The task still needs a
        schedule_interval as it may not be attached to a DAG.
        """
        if self.has_dag():
            return self.dag._schedule_interval
        else:
            return self._schedule_interval

    @property
    def priority_weight_total(self):
        if self.weight_rule == WeightRule.ABSOLUTE:
            return self.priority_weight
        else:
            if self.weight_rule == WeightRule.DOWNSTREAM:
                upstream = False
            else:
                if self.weight_rule == WeightRule.UPSTREAM:
                    upstream = True
                else:
                    upstream = False
            return self.priority_weight + sum(map(lambda task_id: self._dag.task_dict[task_id].priority_weight, self.get_flat_relative_ids(upstream=upstream)))

    @cached_property
    def operator_extra_link_dict(self):
        return {link.name:link for link in self.operator_extra_links}

    @cached_property
    def global_operator_extra_link_dict(self):
        from airflow.plugins_manager import global_operator_extra_links
        return {link.name:link for link in global_operator_extra_links}

    @prepare_lineage
    def pre_execute(self, context):
        """
        This hook is triggered right before self.execute() is called.
        """
        pass

    def execute(self, context):
        """
        This is the main method to derive when creating an operator.
        Context is the same dictionary used as when rendering jinja templates.

        Refer to get_template_context for more context.
        """
        raise NotImplementedError()

    @apply_lineage
    def post_execute(self, context, result=None):
        """
        This hook is triggered right after self.execute() is called.
        It is passed the execution context and any results returned by the
        operator.
        """
        pass

    def on_kill(self):
        """
        Override this method to cleanup subprocesses when a task instance
        gets killed. Any use of the threading, subprocess or multiprocessing
        module within an operator needs to be cleaned up or it will leave
        ghost processes behind.
        """
        pass

    def __deepcopy__(self, memo):
        """
        Hack sorting double chained task lists by task_id to avoid hitting
        max_depth on deepcopy operations.
        """
        sys.setrecursionlimit(5000)
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        shallow_copy = cls.shallow_copy_attrs + cls._base_operator_shallow_copy_attrs
        for k, v in list(self.__dict__.items()):
            if k not in shallow_copy:
                setattr(result, k, copy.deepcopy(v, memo))
            else:
                setattr(result, k, copy.copy(v))

        return result

    def __getstate__(self):
        state = dict(self.__dict__)
        del state['_log']
        return state

    def __setstate__(self, state):
        self.__dict__ = state
        self._log = logging.getLogger('airflow.task.operators')

    def render_template_from_field(self, attr, content, context, jinja_env):
        """
        Renders a template from a field. If the field is a string, it will
        simply render the string and return the result. If it is a collection or
        nested set of collections, it will traverse the structure and render
        all elements in it. If the field has another type, it will return it as it is.
        """
        rt = self.render_template
        if isinstance(content, six.string_types):
            result = (jinja_env.from_string(content).render)(**context)
        else:
            if isinstance(content, tuple):
                if type(content) is not tuple:
                    result = (content.__class__)(*(rt(attr, e, context) for e in content))
                else:
                    result = tuple(rt(attr, e, context) for e in content)
            else:
                if isinstance(content, list):
                    result = [rt(attr, e, context) for e in content]
                else:
                    if isinstance(content, dict):
                        result = {k:rt('{}[{}]'.format(attr, k), v, context) for k, v in list(content.items())}
                    else:
                        result = content
        return result

    def render_template(self, attr, content, context):
        """
        Renders a template either from a file or directly in a field, and returns
        the rendered result.
        """
        jinja_env = self.get_template_env()
        exts = self.__class__.template_ext
        if isinstance(content, six.string_types):
            if any([content.endswith(ext) for ext in exts]):
                return (jinja_env.get_template(content).render)(**context)
        return self.render_template_from_field(attr, content, context, jinja_env)

    def get_template_env(self):
        if hasattr(self, 'dag'):
            return self.dag.get_template_env()
        else:
            return jinja2.Environment(cache_size=0)

    def prepare_template(self):
        """
        Hook that is triggered after the templated fields get replaced
        by their content. If you need your operator to alter the
        content of the file before the template is rendered,
        it should override this method to do so.
        """
        pass

    def resolve_template_files(self):
        for attr in self.template_fields:
            content = getattr(self, attr)
            if content is None:
                continue
            elif isinstance(content, six.string_types) and any([content.endswith(ext) for ext in self.template_ext]):
                env = self.get_template_env()
                try:
                    setattr(self, attr, env.loader.get_source(env, content)[0])
                except Exception as e:
                    self.log.exception(e)

            else:
                if isinstance(content, list):
                    env = self.dag.get_template_env()
                    for i in range(len(content)):
                        if isinstance(content[i], six.string_types) and any([content[i].endswith(ext) for ext in self.template_ext]):
                            try:
                                content[i] = env.loader.get_source(env, content[i])[0]
                            except Exception as e:
                                self.log.exception(e)

        self.prepare_template()

    @property
    def upstream_list(self):
        """@property: list of tasks directly upstream"""
        return [self.dag.get_task(tid) for tid in self._upstream_task_ids]

    @property
    def upstream_task_ids(self):
        return self._upstream_task_ids

    @property
    def downstream_list(self):
        """@property: list of tasks directly downstream"""
        return [self.dag.get_task(tid) for tid in self._downstream_task_ids]

    @property
    def downstream_task_ids(self):
        return self._downstream_task_ids

    @provide_session
    def clear(self, start_date=None, end_date=None, upstream=False, downstream=False, session=None):
        """
        Clears the state of task instances associated with the task, following
        the parameters specified.
        """
        TI = TaskInstance
        qry = session.query(TI).filter(TI.dag_id == self.dag_id)
        if start_date:
            qry = qry.filter(TI.execution_date >= start_date)
        if end_date:
            qry = qry.filter(TI.execution_date <= end_date)
        tasks = [self.task_id]
        if upstream:
            tasks += [t.task_id for t in self.get_flat_relatives(upstream=True)]
        if downstream:
            tasks += [t.task_id for t in self.get_flat_relatives(upstream=False)]
        qry = qry.filter(TI.task_id.in_(tasks))
        count = qry.count()
        clear_task_instances((qry.all()), session, dag=(self.dag))
        session.commit()
        return count

    @provide_session
    def get_task_instances(self, start_date=None, end_date=None, session=None):
        """
        Get a set of task instance related to this task for a specific date
        range.
        """
        end_date = end_date or timezone.utcnow()
        return session.query(TaskInstance).filter(TaskInstance.dag_id == self.dag_id).filter(TaskInstance.task_id == self.task_id).filter(TaskInstance.execution_date >= start_date).filter(TaskInstance.execution_date <= end_date).order_by(TaskInstance.execution_date).all()

    def get_flat_relative_ids(self, upstream=False, found_descendants=None):
        """
        Get a flat list of relatives' ids, either upstream or downstream.
        """
        if not found_descendants:
            found_descendants = set()
        relative_ids = self.get_direct_relative_ids(upstream)
        for relative_id in relative_ids:
            if relative_id not in found_descendants:
                found_descendants.add(relative_id)
                relative_task = self._dag.task_dict[relative_id]
                relative_task.get_flat_relative_ids(upstream, found_descendants)

        return found_descendants

    def get_flat_relatives(self, upstream=False):
        """
        Get a flat list of relatives, either upstream or downstream.
        """
        return list(map(lambda task_id: self._dag.task_dict[task_id], self.get_flat_relative_ids(upstream)))

    def run(self, start_date=None, end_date=None, ignore_first_depends_on_past=False, ignore_ti_state=False, mark_success=False):
        """
        Run a set of task instances for a date range.
        """
        start_date = start_date or self.start_date
        end_date = end_date or self.end_date or timezone.utcnow()
        for dt in self.dag.date_range(start_date, end_date=end_date):
            TaskInstance(self, dt).run(mark_success=mark_success,
              ignore_depends_on_past=(dt == start_date and ignore_first_depends_on_past),
              ignore_ti_state=ignore_ti_state)

    def dry_run(self):
        self.log.info('Dry run')
        for attr in self.template_fields:
            content = getattr(self, attr)
            if content and isinstance(content, six.string_types):
                self.log.info('Rendering template for %s', attr)
                self.log.info(content)

    def get_direct_relative_ids(self, upstream=False):
        """
        Get the direct relative ids to the current task, upstream or
        downstream.
        """
        if upstream:
            return self._upstream_task_ids
        else:
            return self._downstream_task_ids

    def get_direct_relatives(self, upstream=False):
        """
        Get the direct relatives to the current task, upstream or
        downstream.
        """
        if upstream:
            return self.upstream_list
        else:
            return self.downstream_list

    def __repr__(self):
        return '<Task({self.__class__.__name__}): {self.task_id}>'.format(self=self)

    @property
    def task_type(self):
        return self.__class__.__name__

    def add_only_new(self, item_set, item):
        if item in item_set:
            self.log.warning('Dependency {self}, {item} already registered'.format(self=self,
              item=item))
        else:
            item_set.add(item)

    def _set_relatives(self, task_or_task_list, upstream=False):
        try:
            task_list = list(task_or_task_list)
        except TypeError:
            task_list = [
             task_or_task_list]

        for t in task_list:
            if not isinstance(t, BaseOperator):
                raise AirflowException('Relationships can only be set between Operators; received {}'.format(t.__class__.__name__))

        dags = {t._dag.dag_id:t._dag for t in [self] + task_list if t.has_dag() if t.has_dag()}
        if len(dags) > 1:
            raise AirflowException('Tried to set relationships between tasks in more than one DAG: {}'.format(dags.values()))
        else:
            if len(dags) == 1:
                dag = dags.popitem()[1]
            else:
                raise AirflowException("Tried to create relationships between tasks that don't have DAGs yet. Set the DAG for at least one task  and try again: {}".format([
                 self] + task_list))
        if dag:
            if not self.has_dag():
                self.dag = dag
        for task in task_list:
            if dag:
                if not task.has_dag():
                    task.dag = dag
            if upstream:
                task.add_only_new(task.get_direct_relative_ids(upstream=False), self.task_id)
                self.add_only_new(self._upstream_task_ids, task.task_id)
            else:
                self.add_only_new(self._downstream_task_ids, task.task_id)
                task.add_only_new(task.get_direct_relative_ids(upstream=True), self.task_id)

    def set_downstream(self, task_or_task_list):
        """
        Set a task or a task list to be directly downstream from the current
        task.
        """
        self._set_relatives(task_or_task_list, upstream=False)

    def set_upstream(self, task_or_task_list):
        """
        Set a task or a task list to be directly upstream from the current
        task.
        """
        self._set_relatives(task_or_task_list, upstream=True)

    def xcom_push(self, context, key, value, execution_date=None):
        """
        See TaskInstance.xcom_push()
        """
        context['ti'].xcom_push(key=key,
          value=value,
          execution_date=execution_date)

    def xcom_pull(self, context, task_ids=None, dag_id=None, key=XCOM_RETURN_KEY, include_prior_dates=None):
        """
        See TaskInstance.xcom_pull()
        """
        return context['ti'].xcom_pull(key=key,
          task_ids=task_ids,
          dag_id=dag_id,
          include_prior_dates=include_prior_dates)

    @cached_property
    def extra_links(self):
        return list(set(self.operator_extra_link_dict.keys()).union(self.global_operator_extra_link_dict.keys()))

    def get_extra_links(self, dttm, link_name):
        """
        For an operator, gets the URL that the external links specified in
        `extra_links` should point to.
        :raise ValueError: The error message of a ValueError will be passed on through to
        the fronted to show up as a tooltip on the disabled link
        :param dttm: The datetime parsed execution date for the URL being searched for
        :param link_name: The name of the link we're looking for the URL for. Should be
        one of the options specified in `extra_links`
        :return: A URL
        """
        if link_name in self.operator_extra_link_dict:
            return self.operator_extra_link_dict[link_name].get_link(self, dttm)
        if link_name in self.global_operator_extra_link_dict:
            return self.global_operator_extra_link_dict[link_name].get_link(self, dttm)


class BaseOperatorLink:
    __doc__ = '\n    Abstract base class that defines how we get an operator link.\n    '
    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def name(self):
        """
        Name of the link. This will be the button name on the task UI.

        :return: link name
        """
        pass

    @abstractmethod
    def get_link(self, operator, dttm):
        """
        Link to external system.

        :param operator: airflow operator
        :param dttm: datetime
        :return: link to external system
        """
        pass