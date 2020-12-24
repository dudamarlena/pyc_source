# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/api/common/experimental/get_task.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1179 bytes
"""Task APIs.."""
from airflow.api.common.experimental import check_and_get_dag
from airflow.models import TaskInstance

def get_task(dag_id, task_id):
    """Return the task object identified by the given dag_id and task_id."""
    dag = check_and_get_dag(dag_id, task_id)
    return dag.get_task(task_id)