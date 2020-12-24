# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/example_dags/example_gcp_translate.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1928 bytes
__doc__ = '\nExample Airflow DAG that translates text in Google Cloud Translate\nservice in the Google Cloud Platform.\n\n'
import airflow
from airflow import models
from airflow.contrib.operators.gcp_translate_operator import CloudTranslateTextOperator
from airflow.operators.bash_operator import BashOperator
default_args = {'start_date': airflow.utils.dates.days_ago(1)}
with models.DAG('example_gcp_translate',
  default_args=default_args, schedule_interval=None) as (dag):
    product_set_create = CloudTranslateTextOperator(task_id='translate',
      values=[
     'zażółć gęślą jaźń'],
      target_language='en',
      format_='text',
      source_language=None,
      model='base')
    translation_access = BashOperator(task_id='access',
      bash_command='echo \'{{ task_instance.xcom_pull("translate")[0] }}\'')
    product_set_create >> translation_access