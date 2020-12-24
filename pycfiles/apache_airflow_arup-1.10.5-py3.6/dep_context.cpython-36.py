# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/ti_deps/dep_context.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 5654 bytes
from airflow.ti_deps.deps.dag_ti_slots_available_dep import DagTISlotsAvailableDep
from airflow.ti_deps.deps.dag_unpaused_dep import DagUnpausedDep
from airflow.ti_deps.deps.dagrun_exists_dep import DagrunRunningDep
from airflow.ti_deps.deps.exec_date_after_start_date_dep import ExecDateAfterStartDateDep
from airflow.ti_deps.deps.not_running_dep import NotRunningDep
from airflow.ti_deps.deps.not_skipped_dep import NotSkippedDep
from airflow.ti_deps.deps.runnable_exec_date_dep import RunnableExecDateDep
from airflow.ti_deps.deps.valid_state_dep import ValidStateDep
from airflow.ti_deps.deps.task_concurrency_dep import TaskConcurrencyDep
from airflow.utils.state import State

class DepContext(object):
    __doc__ = "\n    A base class for contexts that specifies which dependencies should be evaluated in\n    the context for a task instance to satisfy the requirements of the context. Also\n    stores state related to the context that can be used by dependency classes.\n\n    For example there could be a SomeRunContext that subclasses this class which has\n    dependencies for:\n\n    - Making sure there are slots available on the infrastructure to run the task instance\n    - A task-instance's task-specific dependencies are met (e.g. the previous task\n      instance completed successfully)\n    - ...\n\n    :param deps: The context-specific dependencies that need to be evaluated for a\n        task instance to run in this execution context.\n    :type deps: set(airflow.ti_deps.deps.base_ti_dep.BaseTIDep)\n    :param flag_upstream_failed: This is a hack to generate the upstream_failed state\n        creation while checking to see whether the task instance is runnable. It was the\n        shortest path to add the feature. This is bad since this class should be pure (no\n        side effects).\n    :type flag_upstream_failed: bool\n    :param ignore_all_deps: Whether or not the context should ignore all ignoreable\n        dependencies. Overrides the other ignore_* parameters\n    :type ignore_all_deps: bool\n    :param ignore_depends_on_past: Ignore depends_on_past parameter of DAGs (e.g. for\n        Backfills)\n    :type ignore_depends_on_past: bool\n    :param ignore_in_retry_period: Ignore the retry period for task instances\n    :type ignore_in_retry_period: bool\n    :param ignore_in_reschedule_period: Ignore the reschedule period for task instances\n    :type ignore_in_reschedule_period: bool\n    :param ignore_task_deps: Ignore task-specific dependencies such as depends_on_past and\n        trigger rule\n    :type ignore_task_deps: bool\n    :param ignore_ti_state: Ignore the task instance's previous failure/success\n    :type ignore_ti_state: bool\n    "

    def __init__(self, deps=None, flag_upstream_failed=False, ignore_all_deps=False, ignore_depends_on_past=False, ignore_in_retry_period=False, ignore_in_reschedule_period=False, ignore_task_deps=False, ignore_ti_state=False):
        self.deps = deps or set()
        self.flag_upstream_failed = flag_upstream_failed
        self.ignore_all_deps = ignore_all_deps
        self.ignore_depends_on_past = ignore_depends_on_past
        self.ignore_in_retry_period = ignore_in_retry_period
        self.ignore_in_reschedule_period = ignore_in_reschedule_period
        self.ignore_task_deps = ignore_task_deps
        self.ignore_ti_state = ignore_ti_state


QUEUEABLE_STATES = {
 State.FAILED,
 State.NONE,
 State.QUEUED,
 State.SCHEDULED,
 State.SKIPPED,
 State.UPSTREAM_FAILED,
 State.UP_FOR_RETRY,
 State.UP_FOR_RESCHEDULE}
QUEUE_DEPS = {
 NotRunningDep(),
 NotSkippedDep(),
 RunnableExecDateDep(),
 ValidStateDep(QUEUEABLE_STATES)}
RUN_DEPS = QUEUE_DEPS | {
 DagTISlotsAvailableDep(),
 TaskConcurrencyDep()}
SCHEDULER_DEPS = RUN_DEPS | {
 DagrunRunningDep(),
 DagUnpausedDep(),
 ExecDateAfterStartDateDep()}