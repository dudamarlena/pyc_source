# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/api/common/experimental/get_task_instance.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1682 bytes
"""Task Instance APIs."""
from datetime import datetime
from airflow.api.common.experimental import check_and_get_dag, check_and_get_dagrun
from airflow.exceptions import TaskInstanceNotFound
from airflow.models import TaskInstance

def get_task_instance(dag_id, task_id, execution_date):
    """Return the task object identified by the given dag_id and task_id."""
    dag = check_and_get_dag(dag_id, task_id)
    dagrun = check_and_get_dagrun(dag=dag, execution_date=execution_date)
    task_instance = dagrun.get_task_instance(task_id)
    if not task_instance:
        error_message = 'Task {} instance for date {} not found'.format(task_id, execution_date)
        raise TaskInstanceNotFound(error_message)
    return task_instance