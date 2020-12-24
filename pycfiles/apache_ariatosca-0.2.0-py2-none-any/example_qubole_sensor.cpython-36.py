# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/example_dags/example_qubole_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2673 bytes
__doc__ = '\nThis is only an example DAG to highlight usage of QuboleSensor in various scenarios,\nsome of these tasks may or may not work based on your QDS account setup.\n\nRun a shell command from Qubole Analyze against your Airflow cluster with following to\ntrigger it manually `airflow trigger_dag example_qubole_sensor`.\n\n*Note: Make sure that connection `qubole_default` is properly set before running\nthis example.*\n'
from airflow import DAG
from airflow.contrib.sensors.qubole_sensor import QuboleFileSensor, QubolePartitionSensor
from airflow.utils import dates
default_args = {'owner':'airflow', 
 'depends_on_past':False, 
 'start_date':dates.days_ago(2), 
 'email':[
  'airflow@example.com'], 
 'email_on_failure':False, 
 'email_on_retry':False}
dag = DAG('example_qubole_sensor', default_args=default_args, schedule_interval=None)
dag.doc_md = __doc__
t1 = QuboleFileSensor(task_id='check_s3_file',
  qubole_conn_id='qubole_default',
  poke_interval=60,
  timeout=600,
  data={'files': [
           's3://paid-qubole/HadoopAPIExamples/jars/hadoop-0.20.1-dev-streaming.jar',
           "s3://paid-qubole/HadoopAPITests/data/{{ ds.split('-')[2] }}.tsv"]},
  dag=dag)
t2 = QubolePartitionSensor(task_id='check_hive_partition',
  poke_interval=10,
  timeout=60,
  data={'schema':'default', 
 'table':'my_partitioned_table', 
 'columns':[
  {'column':'month', 
   'values':[
    "{{ ds.split('-')[1] }}"]},
  {'column':'day', 
   'values':[
    "{{ ds.split('-')[2] }}", "{{ yesterday_ds.split('-')[2] }}"]}]},
  dag=dag)
t1.set_downstream(t2)