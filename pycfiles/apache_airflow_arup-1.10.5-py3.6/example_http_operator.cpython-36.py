# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/example_dags/example_http_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2811 bytes
"""
### Example HTTP operator and sensor
"""
import json
from datetime import timedelta
import airflow
from airflow import DAG
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.sensors.http_sensor import HttpSensor
default_args = {'owner':'airflow', 
 'depends_on_past':False, 
 'start_date':airflow.utils.dates.days_ago(2), 
 'email':[
  'airflow@example.com'], 
 'email_on_failure':False, 
 'email_on_retry':False, 
 'retries':1, 
 'retry_delay':timedelta(minutes=5)}
dag = DAG('example_http_operator', default_args=default_args)
dag.doc_md = __doc__
t1 = SimpleHttpOperator(task_id='post_op',
  endpoint='api/v1.0/nodes',
  data=(json.dumps({'priority': 5})),
  headers={'Content-Type': 'application/json'},
  response_check=(lambda response: True if len(response.json()) == 0 else False),
  dag=dag)
t5 = SimpleHttpOperator(task_id='post_op_formenc',
  endpoint='nodes/url',
  data='name=Joe',
  headers={'Content-Type': 'application/x-www-form-urlencoded'},
  dag=dag)
t2 = SimpleHttpOperator(task_id='get_op',
  method='GET',
  endpoint='api/v1.0/nodes',
  data={'param1':'value1', 
 'param2':'value2'},
  headers={},
  dag=dag)
t3 = SimpleHttpOperator(task_id='put_op',
  method='PUT',
  endpoint='api/v1.0/nodes',
  data=(json.dumps({'priority': 5})),
  headers={'Content-Type': 'application/json'},
  dag=dag)
t4 = SimpleHttpOperator(task_id='del_op',
  method='DELETE',
  endpoint='api/v1.0/nodes',
  data='some=data',
  headers={'Content-Type': 'application/x-www-form-urlencoded'},
  dag=dag)
sensor = HttpSensor(task_id='http_sensor_check',
  http_conn_id='http_default',
  endpoint='',
  request_params={},
  response_check=(lambda response: True if 'Google' in response.text else False),
  poke_interval=5,
  dag=dag)
sensor >> t1 >> t2 >> t3 >> t4 >> t5