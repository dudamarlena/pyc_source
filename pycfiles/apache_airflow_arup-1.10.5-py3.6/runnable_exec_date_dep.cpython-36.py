# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/ti_deps/deps/runnable_exec_date_dep.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 2194 bytes
from airflow.ti_deps.deps.base_ti_dep import BaseTIDep
from airflow.utils import timezone
from airflow.utils.db import provide_session

class RunnableExecDateDep(BaseTIDep):
    NAME = 'Execution Date'
    IGNOREABLE = True

    @provide_session
    def _get_dep_statuses(self, ti, session, dep_context):
        cur_date = timezone.utcnow()
        if ti.execution_date > cur_date:
            yield self._failing_status(reason=('Execution date {0} is in the future (the current date is {1}).'.format(ti.execution_date.isoformat(), cur_date.isoformat())))
        if ti.task.end_date:
            if ti.execution_date > ti.task.end_date:
                yield self._failing_status(reason=("The execution date is {0} but this is after the task's end date {1}.".format(ti.execution_date.isoformat(), ti.task.end_date.isoformat())))
        if ti.task.dag:
            if ti.task.dag.end_date:
                if ti.execution_date > ti.task.dag.end_date:
                    yield self._failing_status(reason=("The execution date is {0} but this is after the task's DAG's end date {1}.".format(ti.execution_date.isoformat(), ti.task.dag.end_date.isoformat())))