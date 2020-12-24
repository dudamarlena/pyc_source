# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/ti_deps/deps/dagrun_exists_dep.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 2287 bytes
from airflow.ti_deps.deps.base_ti_dep import BaseTIDep
from airflow.utils.db import provide_session
from airflow.utils.state import State

class DagrunRunningDep(BaseTIDep):
    NAME = 'Dagrun Running'
    IGNOREABLE = True

    @provide_session
    def _get_dep_statuses(self, ti, session, dep_context):
        dag = ti.task.dag
        dagrun = ti.get_dagrun(session)
        if not dagrun:
            from airflow.models import DagRun
            running_dagruns = DagRun.find(dag_id=(dag.dag_id),
              state=(State.RUNNING),
              external_trigger=False,
              session=session)
            if len(running_dagruns) >= dag.max_active_runs:
                reason = "The maximum number of active dag runs ({0}) for this task instance's DAG '{1}' has been reached.".format(dag.max_active_runs, ti.dag_id)
            else:
                reason = 'Unknown reason'
            yield self._failing_status(reason=("Task instance's dagrun did not exist: {0}.".format(reason)))
        elif dagrun.state != State.RUNNING:
            yield self._failing_status(reason=("Task instance's dagrun was not in the 'running' state but in the state '{}'.".format(dagrun.state)))