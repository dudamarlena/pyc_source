# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/example_dags/example_latest_only.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1320 bytes
__doc__ = '\nExample of the LatestOnlyOperator\n'
import datetime as dt, airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.latest_only_operator import LatestOnlyOperator
dag = DAG(dag_id='latest_only',
  schedule_interval=dt.timedelta(hours=4),
  start_date=(airflow.utils.dates.days_ago(2)))
latest_only = LatestOnlyOperator(task_id='latest_only', dag=dag)
task1 = DummyOperator(task_id='task1', dag=dag)
latest_only >> task1