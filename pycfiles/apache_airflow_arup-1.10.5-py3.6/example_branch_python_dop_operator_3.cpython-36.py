# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/example_dags/example_branch_python_dop_operator_3.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1899 bytes
import airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import BranchPythonOperator
args = {'owner':'airflow', 
 'start_date':airflow.utils.dates.days_ago(2), 
 'depends_on_past':True}
dag = DAG(dag_id='example_branch_dop_operator_v3',
  schedule_interval='*/1 * * * *',
  default_args=args)

def should_run(**kwargs):
    print('------------- exec dttm = {} and minute = {}'.format(kwargs['execution_date'], kwargs['execution_date'].minute))
    if kwargs['execution_date'].minute % 2 == 0:
        return 'dummy_task_1'
    else:
        return 'dummy_task_2'


cond = BranchPythonOperator(task_id='condition',
  provide_context=True,
  python_callable=should_run,
  dag=dag)
dummy_task_1 = DummyOperator(task_id='dummy_task_1', dag=dag)
dummy_task_2 = DummyOperator(task_id='dummy_task_2', dag=dag)
cond >> [dummy_task_1, dummy_task_2]