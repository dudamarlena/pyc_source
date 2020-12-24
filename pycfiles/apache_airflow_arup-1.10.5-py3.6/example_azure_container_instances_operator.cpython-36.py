# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/example_dags/example_azure_container_instances_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1711 bytes
from airflow import DAG
from airflow.contrib.operators.azure_container_instances_operator import AzureContainerInstancesOperator
from datetime import datetime, timedelta
default_args = {'owner':'airflow', 
 'depends_on_past':False, 
 'start_date':datetime(2018, 11, 1), 
 'email':[
  'airflow@example.com'], 
 'email_on_failure':False, 
 'email_on_retry':False, 
 'retries':1, 
 'retry_delay':timedelta(minutes=5)}
dag = DAG('aci_example',
  default_args=default_args,
  schedule_interval=(timedelta(1)))
t1 = AzureContainerInstancesOperator(ci_conn_id='azure_container_instances_default',
  registry_conn_id=None,
  resource_group='resource-group',
  name='aci-test-{{ ds }}',
  image='hello-world',
  region='WestUS2',
  environment_variables={},
  volumes=[],
  memory_in_gb=4.0,
  cpu=1.0,
  task_id='start_container',
  dag=dag)