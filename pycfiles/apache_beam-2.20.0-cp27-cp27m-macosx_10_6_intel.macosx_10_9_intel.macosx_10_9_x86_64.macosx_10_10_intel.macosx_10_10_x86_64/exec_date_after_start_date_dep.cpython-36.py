# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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