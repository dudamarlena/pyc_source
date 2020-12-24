# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/example_dags/example_xcom.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2151 bytes
from __future__ import print_function
import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
args = {'owner':'airflow', 
 'start_date':airflow.utils.dates.days_ago(2), 
 'provide_context':True}
dag = DAG('example_xcom', schedule_interval='@once', default_args=args)
value_1 = [
 1, 2, 3]
value_2 = {'a': 'b'}

def push(**kwargs):
    """Pushes an XCom without a specific target"""
    kwargs['ti'].xcom_push(key='value from pusher 1', value=value_1)


def push_by_returning(**kwargs):
    """Pushes an XCom without a specific target, just by returning it"""
    return value_2


def puller(**kwargs):
    ti = kwargs['ti']
    v1 = ti.xcom_pull(key=None, task_ids='push')
    if not v1 == value_1:
        raise AssertionError
    else:
        v2 = ti.xcom_pull(task_ids='push_by_returning')
        assert v2 == value_2
        v1, v2 = ti.xcom_pull(key=None, task_ids=['push', 'push_by_returning'])
        assert (v1, v2) == (value_1, value_2)


push1 = PythonOperator(task_id='push',
  dag=dag,
  python_callable=push)
push2 = PythonOperator(task_id='push_by_returning',
  dag=dag,
  python_callable=push_by_returning)
pull = PythonOperator(task_id='puller',
  dag=dag,
  python_callable=puller)
pull << [push1, push2]