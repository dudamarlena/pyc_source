# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/example_dags/example_latest_only_with_trigger.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1627 bytes
__doc__ = '\nExample LatestOnlyOperator and TriggerRule interactions\n'
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