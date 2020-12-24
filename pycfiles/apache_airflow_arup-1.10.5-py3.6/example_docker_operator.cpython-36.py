# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/example_dags/example_docker_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1956 bytes
"""
import airflow
from airflow import DAG
from airflow.operators import BashOperator
from datetime import timedelta
from airflow.operators.docker_operator import DockerOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(2),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'docker_sample', default_args=default_args, schedule_interval=timedelta(minutes=10))

t1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag)

t2 = BashOperator(
    task_id='sleep',
    bash_command='sleep 5',
    retries=3,
    dag=dag)

t3 = DockerOperator(api_version='1.19',
    docker_url='tcp://localhost:2375', #Set your docker URL
    command='/bin/sleep 30',
    image='centos:latest',
    network_mode='bridge',
    task_id='docker_op_tester',
    dag=dag)

t4 = BashOperator(
    task_id='print_hello',
    bash_command='echo "hello world!!!"',
    dag=dag)

t1.set_downstream(t2)
t1.set_downstream(t3)
t3.set_downstream(t4)
"""