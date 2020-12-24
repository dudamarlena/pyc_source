# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/example_dags/example_gcp_compute_igm.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 5763 bytes
__doc__ = '\nExample Airflow DAG that uses IGM-type compute operations:\n* copy of Instance Template\n* update template in Instance Group Manager\n\nThis DAG relies on the following OS environment variables\n\n* GCP_PROJECT_ID - the Google Cloud Platform project where the Compute Engine instance exists\n* GCE_ZONE - the zone where the Compute Engine instance exists\n\nVariables for copy template operator:\n* GCE_TEMPLATE_NAME - name of the template to copy\n* GCE_NEW_TEMPLATE_NAME - name of the new template\n* GCE_NEW_DESCRIPTION - description added to the template\n\nVariables for update template in Group Manager:\n\n* GCE_INSTANCE_GROUP_MANAGER_NAME - name of the Instance Group Manager\n* SOURCE_TEMPLATE_URL - url of the template to replace in the Instance Group Manager\n* DESTINATION_TEMPLATE_URL - url of the new template to set in the Instance Group Manager\n'
import os, airflow
from airflow import models
from airflow.contrib.operators.gcp_compute_operator import GceInstanceTemplateCopyOperator, GceInstanceGroupManagerUpdateTemplateOperator
GCP_PROJECT_ID = os.environ.get('GCP_PROJECT_ID', 'example-project')
GCE_ZONE = os.environ.get('GCE_ZONE', 'europe-west1-b')
default_args = {'start_date': airflow.utils.dates.days_ago(1)}
GCE_TEMPLATE_NAME = os.environ.get('GCE_TEMPLATE_NAME', 'instance-template-test')
GCE_NEW_TEMPLATE_NAME = os.environ.get('GCE_NEW_TEMPLATE_NAME', 'instance-template-test-new')
GCE_NEW_DESCRIPTION = os.environ.get('GCE_NEW_DESCRIPTION', 'Test new description')
GCE_INSTANCE_TEMPLATE_BODY_UPDATE = {'name':GCE_NEW_TEMPLATE_NAME, 
 'description':GCE_NEW_DESCRIPTION, 
 'properties':{'machineType': 'n1-standard-2'}}
GCE_INSTANCE_GROUP_MANAGER_NAME = os.environ.get('GCE_INSTANCE_GROUP_MANAGER_NAME', 'instance-group-test')
SOURCE_TEMPLATE_URL = os.environ.get('SOURCE_TEMPLATE_URL', 'https://www.googleapis.com/compute/beta/projects/' + GCP_PROJECT_ID + '/global/instanceTemplates/instance-template-test')
DESTINATION_TEMPLATE_URL = os.environ.get('DESTINATION_TEMPLATE_URL', 'https://www.googleapis.com/compute/beta/projects/' + GCP_PROJECT_ID + '/global/instanceTemplates/' + GCE_NEW_TEMPLATE_NAME)
UPDATE_POLICY = {'type':'OPPORTUNISTIC', 
 'minimalAction':'RESTART', 
 'maxSurge':{'fixed': 1}, 
 'minReadySec':1800}
with models.DAG('example_gcp_compute_igm',
  default_args=default_args,
  schedule_interval=None) as (dag):
    gce_instance_template_copy = GceInstanceTemplateCopyOperator(project_id=GCP_PROJECT_ID,
      resource_id=GCE_TEMPLATE_NAME,
      body_patch=GCE_INSTANCE_TEMPLATE_BODY_UPDATE,
      task_id='gcp_compute_igm_copy_template_task')
    gce_instance_template_copy2 = GceInstanceTemplateCopyOperator(resource_id=GCE_TEMPLATE_NAME,
      body_patch=GCE_INSTANCE_TEMPLATE_BODY_UPDATE,
      task_id='gcp_compute_igm_copy_template_task_2')
    gce_instance_group_manager_update_template = GceInstanceGroupManagerUpdateTemplateOperator(project_id=GCP_PROJECT_ID,
      resource_id=GCE_INSTANCE_GROUP_MANAGER_NAME,
      zone=GCE_ZONE,
      source_template=SOURCE_TEMPLATE_URL,
      destination_template=DESTINATION_TEMPLATE_URL,
      update_policy=UPDATE_POLICY,
      task_id='gcp_compute_igm_group_manager_update_template')
    gce_instance_group_manager_update_template2 = GceInstanceGroupManagerUpdateTemplateOperator(resource_id=GCE_INSTANCE_GROUP_MANAGER_NAME,
      zone=GCE_ZONE,
      source_template=SOURCE_TEMPLATE_URL,
      destination_template=DESTINATION_TEMPLATE_URL,
      task_id='gcp_compute_igm_group_manager_update_template_2')
    gce_instance_template_copy >> gce_instance_template_copy2 >> gce_instance_group_manager_update_template >> gce_instance_group_manager_update_template2