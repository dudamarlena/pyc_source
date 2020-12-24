# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/ti_deps/deps/prev_dagrun_dep.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 3587 bytes
from airflow.ti_deps.deps.base_ti_dep import BaseTIDep
from airflow.utils.db import provide_session
from airflow.utils.state import State

class PrevDagrunDep(BaseTIDep):
    __doc__ = "\n    Is the past dagrun in a state that allows this task instance to run, e.g. did this\n    task instance's task in the previous dagrun complete if we are depending on past.\n    "
    NAME = 'Previous Dagrun State'
    IGNOREABLE = True
    IS_TASK_DEP = True

    @provide_session
    def _get_dep_statuses(self, ti, session, dep_context):
        if dep_context.ignore_depends_on_past:
            yield self._passing_status(reason='The context specified that the state of past DAGs could be ignored.')
            return
        elif not ti.task.depends_on_past:
            yield self._passing_status(reason='The task did not have depends_on_past set.')
            return
        else:
            dag = ti.task.dag
            if dag.catchup:
                if dag.previous_schedule(ti.execution_date) is None:
                    yield self._passing_status(reason='This task does not have a schedule or is @once')
                    return
                if dag.previous_schedule(ti.execution_date) < ti.task.start_date:
                    yield self._passing_status(reason='This task instance was the first task instance for its task.')
                    return
            else:
                dr = ti.get_dagrun()
            last_dagrun = dr.get_previous_dagrun() if dr else None
            if not last_dagrun:
                yield self._passing_status(reason='This task instance was the first task instance for its task.')
                return
            previous_ti = ti.previous_ti
            if not previous_ti:
                yield self._failing_status(reason="depends_on_past is true for this task's DAG, but the previous task instance has not run yet.")
                return
            if previous_ti.state not in {State.SKIPPED, State.SUCCESS}:
                yield self._failing_status(reason=("depends_on_past is true for this task, but the previous task instance {0} is in the state '{1}' which is not a successful state.".format(previous_ti, previous_ti.state)))
            previous_ti.task = ti.task
            if ti.task.wait_for_downstream:
                if not previous_ti.are_dependents_done(session=session):
                    yield self._failing_status(reason=("The tasks downstream of the previous task instance {0} haven't completed.".format(previous_ti)))