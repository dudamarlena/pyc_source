# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/example_dags/example_trigger_target_dag.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2614 bytes
import pprint, airflow
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
pp = pprint.PrettyPrinter(indent=4)
args = {'start_date':airflow.utils.dates.days_ago(2), 
 'owner':'airflow'}
dag = DAG(dag_id='example_trigger_target_dag',
  default_args=args,
  schedule_interval=None)

def run_this_func(ds, **kwargs):
    print('Remotely received value of {} for key=message'.format(kwargs['dag_run'].conf['message']))


run_this = PythonOperator(task_id='run_this',
  provide_context=True,
  python_callable=run_this_func,
  dag=dag)
bash_task = BashOperator(task_id='bash_task',
  bash_command='echo "Here is the message: {{ dag_run.conf["message"] if dag_run else "" }}" ',
  dag=dag)