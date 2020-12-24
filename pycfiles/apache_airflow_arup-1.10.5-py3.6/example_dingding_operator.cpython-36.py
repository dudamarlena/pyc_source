# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/example_dags/example_dingding_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 7035 bytes
from datetime import timedelta
import airflow
from airflow.contrib.operators.dingding_operator import DingdingOperator
from airflow.models import DAG
args = {'owner':'airflow', 
 'retries':3, 
 'start_date':airflow.utils.dates.days_ago(2)}

def failure_callback(context):
    message = 'AIRFLOW TASK FAILURE TIPS:\nDAG:    {}\nTASKS:  {}\nReason: {}\n'.format(context['task_instance'].dag_id, context['task_instance'].task_id, context['exception'])
    return DingdingOperator(task_id='dingding_success_callback',
      dingding_conn_id='dingding_default',
      message_type='text',
      message=message,
      at_all=True).execute(context)


args['on_failure_callback'] = failure_callback
dag = DAG(dag_id='example_dingding_operator',
  default_args=args,
  schedule_interval='@once',
  dagrun_timeout=timedelta(minutes=60))
text_msg_remind_none = DingdingOperator(task_id='text_msg_remind_none',
  dingding_conn_id='dingding_default',
  message_type='text',
  message='Airflow dingding text message remind none',
  at_mobiles=None,
  at_all=False,
  dag=dag)
text_msg_remind_specific = DingdingOperator(task_id='text_msg_remind_specific',
  dingding_conn_id='dingding_default',
  message_type='text',
  message='Airflow dingding text message remind specific users',
  at_mobiles=[
 '156XXXXXXXX', '130XXXXXXXX'],
  at_all=False,
  dag=dag)
text_msg_remind_include_invalid = DingdingOperator(task_id='text_msg_remind_include_invalid',
  dingding_conn_id='dingding_default',
  message_type='text',
  message='Airflow dingding text message remind users including invalid',
  at_mobiles=[
 '156XXXXXXXX', '123'],
  at_all=False,
  dag=dag)
text_msg_remind_all = DingdingOperator(task_id='text_msg_remind_all',
  dingding_conn_id='dingding_default',
  message_type='text',
  message='Airflow dingding text message remind all users in group',
  at_mobiles=[
 '156XXXXXXXX', '130XXXXXXXX'],
  at_all=True,
  dag=dag)
link_msg = DingdingOperator(task_id='link_msg',
  dingding_conn_id='dingding_default',
  message_type='link',
  message={'title':'Airflow dingding link message', 
 'text':'Airflow official documentation link', 
 'messageUrl':'http://airflow.apache.org', 
 'picURL':'http://airflow.apache.org/_images/pin_large.png'},
  dag=dag)
markdown_msg = DingdingOperator(task_id='markdown_msg',
  dingding_conn_id='dingding_default',
  message_type='markdown',
  message={'title':'Airflow dingding markdown message', 
 'text':'# Markdown message title\ncontent content .. \n### sub-title\n![logo](http://airflow.apache.org/_images/pin_large.png)'},
  at_mobiles=[
 '156XXXXXXXX'],
  at_all=False,
  dag=dag)
single_action_card_msg = DingdingOperator(task_id='single_action_card_msg',
  dingding_conn_id='dingding_default',
  message_type='actionCard',
  message={'title':'Airflow dingding single actionCard message', 
 'text':'Airflow dingding single actionCard message\n![logo](http://airflow.apache.org/_images/pin_large.png)\nThis is a official logo in Airflow website.', 
 'hideAvatar':'0', 
 'btnOrientation':'0', 
 'singleTitle':'read more', 
 'singleURL':'http://airflow.apache.org'},
  dag=dag)
multi_action_card_msg = DingdingOperator(task_id='multi_action_card_msg',
  dingding_conn_id='dingding_default',
  message_type='actionCard',
  message={'title':'Airflow dingding multi actionCard message', 
 'text':'Airflow dingding multi actionCard message\n![logo](http://airflow.apache.org/_images/pin_large.png)\nAirflow documentation and github', 
 'hideAvatar':'0', 
 'btnOrientation':'0', 
 'btns':[
  {'title':'Airflow Documentation', 
   'actionURL':'http://airflow.apache.org'},
  {'title':'Airflow Github', 
   'actionURL':'https://github.com/apache/airflow'}]},
  dag=dag)
feed_card_msg = DingdingOperator(task_id='feed_card_msg',
  dingding_conn_id='dingding_default',
  message_type='feedCard',
  message={'links': [
           {'title':'Airflow DAG feed card', 
            'messageURL':'https://airflow.readthedocs.io/en/latest/ui.html', 
            'picURL':'http://airflow.apache.org/_images/dags.png'},
           {'title':'Airflow tree feed card', 
            'messageURL':'https://airflow.readthedocs.io/en/latest/ui.html', 
            'picURL':'http://airflow.apache.org/_images/tree.png'},
           {'title':'Airflow graph feed card', 
            'messageURL':'https://airflow.readthedocs.io/en/latest/ui.html', 
            'picURL':'http://airflow.apache.org/_images/graph.png'}]},
  dag=dag)
msg_failure_callback = DingdingOperator(task_id='msg_failure_callback',
  dingding_conn_id='dingding_default',
  message_type='not_support_msg_type',
  message='',
  dag=dag)
[
 text_msg_remind_none, text_msg_remind_specific, text_msg_remind_include_invalid, text_msg_remind_all] >> link_msg >> markdown_msg >> [single_action_card_msg, multi_action_card_msg] >> feed_card_msg >> msg_failure_callback