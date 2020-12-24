# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/example_dags/example_branch_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1808 bytes
import random, airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import BranchPythonOperator
args = {'owner':'airflow', 
 'start_date':airflow.utils.dates.days_ago(2)}
dag = DAG(dag_id='example_branch_operator',
  default_args=args,
  schedule_interval='@daily')
run_this_first = DummyOperator(task_id='run_this_first',
  dag=dag)
options = [
 'branch_a', 'branch_b', 'branch_c', 'branch_d']
branching = BranchPythonOperator(task_id='branching',
  python_callable=(lambda : random.choice(options)),
  dag=dag)
run_this_first >> branching
join = DummyOperator(task_id='join',
  trigger_rule='one_success',
  dag=dag)
for option in options:
    t = DummyOperator(task_id=option,
      dag=dag)
    dummy_follow = DummyOperator(task_id=('follow_' + option),
      dag=dag)
    branching >> t >> dummy_follow >> join