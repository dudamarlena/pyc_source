# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/example_dags/test_utils.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1170 bytes
"""Used for unit tests"""
import airflow
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
dag = DAG(dag_id='test_utils', schedule_interval=None)
task = BashOperator(task_id='sleeps_forever',
  dag=dag,
  bash_command='sleep 10000000000',
  start_date=(airflow.utils.dates.days_ago(2)),
  owner='airflow')