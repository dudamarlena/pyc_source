# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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