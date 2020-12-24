# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/example_dags/example_azure_cosmosdb_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2201 bytes
__doc__ = '\nThis is only an example DAG to highlight usage of AzureCosmosDocumentSensor to detect\nif a document now exists.\n\nYou can trigger this manually with `airflow trigger_dag example_cosmosdb_sensor`.\n\n*Note: Make sure that connection `azure_cosmos_default` is properly set before running\nthis example.*\n'
from airflow import DAG
from airflow.contrib.sensors.azure_cosmos_sensor import AzureCosmosDocumentSensor
from airflow.contrib.operators.azure_cosmos_operator import AzureCosmosInsertDocumentOperator
from airflow.utils import dates
default_args = {'owner':'airflow', 
 'depends_on_past':False, 
 'start_date':dates.days_ago(2), 
 'email':[
  'airflow@example.com'], 
 'email_on_failure':False, 
 'email_on_retry':False}
dag = DAG('example_azure_cosmosdb_sensor', default_args=default_args)
dag.doc_md = __doc__
t1 = AzureCosmosDocumentSensor(task_id='check_cosmos_file',
  database_name='airflow_example_db',
  collection_name='airflow_example_coll',
  document_id='airflow_checkid',
  azure_cosmos_conn_id='azure_cosmos_default',
  dag=dag)
t2 = AzureCosmosInsertDocumentOperator(task_id='insert_cosmos_file',
  dag=dag,
  database_name='airflow_example_db',
  collection_name='new-collection',
  document={'id':'someuniqueid', 
 'param1':'value1',  'param2':'value2'},
  azure_cosmos_conn_id='azure_cosmos_default')
t1 >> t2