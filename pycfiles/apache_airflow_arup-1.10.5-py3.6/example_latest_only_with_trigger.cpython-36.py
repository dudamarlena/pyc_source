# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/example_dags/example_latest_only_with_trigger.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1627 bytes
"""
Example LatestOnlyOperator and TriggerRule interactions
"""
import datetime as dt, airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.latest_only_operator import LatestOnlyOperator
from airflow.utils.trigger_rule import TriggerRule
dag = DAG(dag_id='latest_only_with_trigger',
  schedule_interval=dt.timedelta(hours=4),
  start_date=(airflow.utils.dates.days_ago(2)))
latest_only = LatestOnlyOperator(task_id='latest_only', dag=dag)
task1 = DummyOperator(task_id='task1', dag=dag)
task2 = DummyOperator(task_id='task2', dag=dag)
task3 = DummyOperator(task_id='task3', dag=dag)
task4 = DummyOperator(task_id='task4', dag=dag, trigger_rule=(TriggerRule.ALL_DONE))
latest_only >> task1 >> [task3, task4]
task2 >> [task3, task4]