# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
    """DepContext"""

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