# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/api/common/experimental/get_dag_run_state.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1407 bytes
__doc__ = 'DAG run APIs.'
from datetime import datetime
from typing import Dict
from airflow.api.common.experimental import check_and_get_dag, check_and_get_dagrun

def get_dag_run_state(dag_id, execution_date):
    """Return the task object identified by the given dag_id and task_id.

    :param dag_id: DAG id
    :param execution_date: execution date
    :return: Dictionary storing state of the object
    """
    dag = check_and_get_dag(dag_id=dag_id)
    dagrun = check_and_get_dagrun(dag, execution_date)
    return {'state': dagrun.get_state()}