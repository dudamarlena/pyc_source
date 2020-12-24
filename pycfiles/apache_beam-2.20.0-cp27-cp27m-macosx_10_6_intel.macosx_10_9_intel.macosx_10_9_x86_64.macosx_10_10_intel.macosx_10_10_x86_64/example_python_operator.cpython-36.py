# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/example_dags/example_python_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2056 bytes
from __future__ import print_function
import time
from builtins import range
from pprint import pprint
import airflow
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
args = {'owner':'airflow', 
 'start_date':airflow.utils.dates.days_ago(2)}
dag = DAG(dag_id='example_python_operator',
  default_args=args,
  schedule_interval=None)

def print_context(ds, **kwargs):
    pprint(kwargs)
    print(ds)
    return 'Whatever you return gets printed in the logs'


run_this = PythonOperator(task_id='print_the_context',
  provide_context=True,
  python_callable=print_context,
  dag=dag)

def my_sleeping_function(random_base):
    """This is a function that will run within the DAG execution"""
    time.sleep(random_base)


for i in range(5):
    task = PythonOperator(task_id=('sleep_for_' + str(i)),
      python_callable=my_sleeping_function,
      op_kwargs={'random_base': float(i) / 10},
      dag=dag)
    run_this >> task