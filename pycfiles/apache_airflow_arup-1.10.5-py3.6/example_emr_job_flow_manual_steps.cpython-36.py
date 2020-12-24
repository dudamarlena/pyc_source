# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/example_dags/example_emr_job_flow_manual_steps.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3008 bytes
from datetime import timedelta
import airflow
from airflow import DAG
from airflow.contrib.operators.emr_create_job_flow_operator import EmrCreateJobFlowOperator
from airflow.contrib.operators.emr_add_steps_operator import EmrAddStepsOperator
from airflow.contrib.sensors.emr_step_sensor import EmrStepSensor
from airflow.contrib.operators.emr_terminate_job_flow_operator import EmrTerminateJobFlowOperator
DEFAULT_ARGS = {'owner':'airflow', 
 'depends_on_past':False, 
 'start_date':airflow.utils.dates.days_ago(2), 
 'email':[
  'airflow@example.com'], 
 'email_on_failure':False, 
 'email_on_retry':False}
SPARK_TEST_STEPS = [
 {'Name':'calculate_pi', 
  'ActionOnFailure':'CONTINUE', 
  'HadoopJarStep':{'Jar':'command-runner.jar', 
   'Args':[
    '/usr/lib/spark/bin/run-example',
    'SparkPi',
    '10']}}]
JOB_FLOW_OVERRIDES = {'Name': 'PiCalc'}
dag = DAG('emr_job_flow_manual_steps_dag',
  default_args=DEFAULT_ARGS,
  dagrun_timeout=timedelta(hours=2),
  schedule_interval='0 3 * * *')
cluster_creator = EmrCreateJobFlowOperator(task_id='create_job_flow',
  job_flow_overrides=JOB_FLOW_OVERRIDES,
  aws_conn_id='aws_default',
  emr_conn_id='emr_default',
  dag=dag)
step_adder = EmrAddStepsOperator(task_id='add_steps',
  job_flow_id="{{ task_instance.xcom_pull('create_job_flow', key='return_value') }}",
  aws_conn_id='aws_default',
  steps=SPARK_TEST_STEPS,
  dag=dag)
step_checker = EmrStepSensor(task_id='watch_step',
  job_flow_id="{{ task_instance.xcom_pull('create_job_flow', key='return_value') }}",
  step_id="{{ task_instance.xcom_pull('add_steps', key='return_value')[0] }}",
  aws_conn_id='aws_default',
  dag=dag)
cluster_remover = EmrTerminateJobFlowOperator(task_id='remove_cluster',
  job_flow_id="{{ task_instance.xcom_pull('create_job_flow', key='return_value') }}",
  aws_conn_id='aws_default',
  dag=dag)
cluster_creator.set_downstream(step_adder)
step_adder.set_downstream(step_checker)
step_checker.set_downstream(cluster_remover)