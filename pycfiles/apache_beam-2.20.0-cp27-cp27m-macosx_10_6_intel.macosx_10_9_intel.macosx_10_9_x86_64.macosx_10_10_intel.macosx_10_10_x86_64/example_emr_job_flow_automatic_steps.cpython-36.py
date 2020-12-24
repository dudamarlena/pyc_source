# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/example_dags/example_emr_job_flow_automatic_steps.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2266 bytes
from datetime import timedelta
import airflow
from airflow import DAG
from airflow.contrib.operators.emr_create_job_flow_operator import EmrCreateJobFlowOperator
from airflow.contrib.sensors.emr_job_flow_sensor import EmrJobFlowSensor
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
JOB_FLOW_OVERRIDES = {'Name':'PiCalc', 
 'Steps':SPARK_TEST_STEPS}
dag = DAG('emr_job_flow_automatic_steps_dag',
  default_args=DEFAULT_ARGS,
  dagrun_timeout=timedelta(hours=2),
  schedule_interval='0 3 * * *')
job_flow_creator = EmrCreateJobFlowOperator(task_id='create_job_flow',
  job_flow_overrides=JOB_FLOW_OVERRIDES,
  aws_conn_id='aws_default',
  emr_conn_id='emr_default',
  dag=dag)
job_sensor = EmrJobFlowSensor(task_id='check_job_flow',
  job_flow_id="{{ task_instance.xcom_pull('create_job_flow', key='return_value') }}",
  aws_conn_id='aws_default',
  dag=dag)
job_flow_creator.set_downstream(job_sensor)