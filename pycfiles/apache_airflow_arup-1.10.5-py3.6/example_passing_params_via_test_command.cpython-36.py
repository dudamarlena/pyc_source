# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/example_dags/example_passing_params_via_test_command.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2321 bytes
from datetime import timedelta
import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
dag = DAG('example_passing_params_via_test_command',
  default_args={'owner':'airflow', 
 'start_date':airflow.utils.dates.days_ago(1)},
  schedule_interval='*/1 * * * *',
  dagrun_timeout=timedelta(minutes=4))

def my_py_command(ds, **kwargs):
    if kwargs['test_mode']:
        print(" 'foo' was passed in via test={} command : kwargs[params][foo]                = {}".format(kwargs['test_mode'], kwargs['params']['foo']))
    print(" 'miff' was passed in via task params = {}".format(kwargs['params']['miff']))
    return 1


my_templated_command = '\n    echo " \'foo was passed in via Airflow CLI Test command with value {{ params.foo }} "\n    echo " \'miff was passed in via BashOperator with value {{ params.miff }} "\n'
run_this = PythonOperator(task_id='run_this',
  provide_context=True,
  python_callable=my_py_command,
  params={'miff': 'agg'},
  dag=dag)
also_run_this = BashOperator(task_id='also_run_this',
  bash_command=my_templated_command,
  params={'miff': 'agg'},
  dag=dag)
run_this >> also_run_this