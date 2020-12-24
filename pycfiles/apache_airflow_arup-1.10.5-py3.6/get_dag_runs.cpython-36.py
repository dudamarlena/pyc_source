# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/api/common/experimental/get_dag_runs.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2057 bytes
"""DAG runs APIs."""
from typing import Optional, List, Dict, Any
from flask import url_for
from airflow.api.common.experimental import check_and_get_dag
from airflow.models import DagRun

def get_dag_runs(dag_id, state=None, run_url_route='Airflow.graph'):
    """
    Returns a list of Dag Runs for a specific DAG ID.
    :param dag_id: String identifier of a DAG
    :param state: queued|running|success...
    :return: List of DAG runs of a DAG with requested state,
    or all runs if the state is not specified
    """
    check_and_get_dag(dag_id=dag_id)
    dag_runs = list()
    state = state.lower() if state else None
    for run in DagRun.find(dag_id=dag_id, state=state):
        dag_runs.append({'id':run.id, 
         'run_id':run.run_id, 
         'state':run.state, 
         'dag_id':run.dag_id, 
         'execution_date':run.execution_date.isoformat(), 
         'start_date':run.start_date or '' and run.start_date.isoformat(), 
         'dag_run_url':url_for(run_url_route, dag_id=run.dag_id, execution_date=run.execution_date)})

    return dag_runs