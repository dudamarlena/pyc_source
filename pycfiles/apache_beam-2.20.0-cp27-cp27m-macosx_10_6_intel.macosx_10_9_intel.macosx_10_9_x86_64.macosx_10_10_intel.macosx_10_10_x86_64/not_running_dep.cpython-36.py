# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/ti_deps/deps/not_running_dep.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1578 bytes
from airflow.ti_deps.deps.base_ti_dep import BaseTIDep
from airflow.utils.db import provide_session
from airflow.utils.state import State

class NotRunningDep(BaseTIDep):
    NAME = 'Task Instance Not Already Running'
    IGNOREABLE = False

    @provide_session
    def _get_dep_statuses(self, ti, session, dep_context):
        if ti.state == State.RUNNING:
            yield self._failing_status(reason=('Task is already running, it started on {0}.'.format(ti.start_date)))