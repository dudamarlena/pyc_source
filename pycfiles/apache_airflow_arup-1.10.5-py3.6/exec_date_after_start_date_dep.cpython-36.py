# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/ti_deps/deps/exec_date_after_start_date_dep.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1826 bytes
from airflow.ti_deps.deps.base_ti_dep import BaseTIDep
from airflow.utils.db import provide_session

class ExecDateAfterStartDateDep(BaseTIDep):
    NAME = 'Execution Date'
    IGNOREABLE = True

    @provide_session
    def _get_dep_statuses(self, ti, session, dep_context):
        if ti.task.start_date:
            if ti.execution_date < ti.task.start_date:
                yield self._failing_status(reason=("The execution date is {0} but this is before the task's start date {1}.".format(ti.execution_date.isoformat(), ti.task.start_date.isoformat())))
        if ti.task.dag:
            if ti.task.dag.start_date:
                if ti.execution_date < ti.task.dag.start_date:
                    yield self._failing_status(reason=("The execution date is {0} but this is before the task's DAG's start date {1}.".format(ti.execution_date.isoformat(), ti.task.dag.start_date.isoformat())))