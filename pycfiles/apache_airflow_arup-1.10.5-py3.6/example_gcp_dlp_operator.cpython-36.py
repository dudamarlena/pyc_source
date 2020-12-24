# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/example_dags/example_gcp_dlp_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2751 bytes
"""
Example Airflow DAG that execute the following tasks using
Cloud DLP service in the Google Cloud Platform:
1) Creating a content inspect template;
2) Using the created template to inspect content;
3) Deleting the template from GCP .
"""
import os
from google.cloud.dlp_v2.types import ContentItem, InspectConfig, InspectTemplate
import airflow
from airflow.models import DAG
from airflow.contrib.operators.gcp_dlp_operator import CloudDLPCreateInspectTemplateOperator, CloudDLPDeleteInspectTemplateOperator, CloudDLPInspectContentOperator
default_args = {'start_date': airflow.utils.dates.days_ago(1)}
GCP_PROJECT = os.environ.get('GCP_PROJECT_ID', 'example-project')
TEMPLATE_ID = 'dlp-inspect-8034856'
ITEM = ContentItem(table={'headers':[
  {'name': 'column1'}], 
 'rows':[
  {'values': [{'string_value': 'My phone number is (206) 555-0123'}]}]})
INSPECT_CONFIG = InspectConfig(info_types=[
 {'name': 'PHONE_NUMBER'}, {'name': 'US_TOLLFREE_PHONE_NUMBER'}])
INSPECT_TEMPLATE = InspectTemplate(inspect_config=INSPECT_CONFIG)
with DAG('example_gcp_dlp', default_args=default_args, schedule_interval=None) as (dag):
    create_template = CloudDLPCreateInspectTemplateOperator(project_id=GCP_PROJECT,
      inspect_template=INSPECT_TEMPLATE,
      template_id=TEMPLATE_ID,
      task_id='create_template',
      do_xcom_push=True,
      dag=dag)
    inspect_content = CloudDLPInspectContentOperator(task_id='inpsect_content',
      project_id=GCP_PROJECT,
      item=ITEM,
      inspect_template_name="{{ task_instance.xcom_pull('create_template', key='return_value')['name'] }}",
      dag=dag)
    delete_template = CloudDLPDeleteInspectTemplateOperator(task_id='delete_template',
      template_id=TEMPLATE_ID,
      project_id=GCP_PROJECT,
      dag=dag)
    create_template > inspect_content > delete_template