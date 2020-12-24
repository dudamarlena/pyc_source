# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/example_dags/example_gcp_function.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 5058 bytes
__doc__ = '\nExample Airflow DAG that displays interactions with Google Cloud Functions.\nIt creates a function and then deletes it.\n\nThis DAG relies on the following OS environment variables\nhttps://airflow.apache.org/concepts.html#variables\n\n* GCP_PROJECT_ID - Google Cloud Project to use for the Cloud Function.\n* GCP_LOCATION - Google Cloud Functions region where the function should be\n  created.\n* GCF_ENTRYPOINT - Name of the executable function in the source code.\n* and one of the below:\n\n    * GCF_SOURCE_ARCHIVE_URL - Path to the zipped source in Google Cloud Storage\n\n    * GCF_SOURCE_UPLOAD_URL - Generated upload URL for the zipped source and GCF_ZIP_PATH - Local path to\n      the zipped source archive\n\n    * GCF_SOURCE_REPOSITORY - The URL pointing to the hosted repository where the function\n      is defined in a supported Cloud Source Repository URL format\n      https://cloud.google.com/functions/docs/reference/rest/v1/projects.locations.functions#SourceRepository\n\n'
import os
from airflow import models
from airflow.contrib.operators.gcp_function_operator import GcfFunctionDeployOperator, GcfFunctionDeleteOperator
from airflow.utils import dates
GCP_PROJECT_ID = os.environ.get('GCP_PROJECT_ID', 'example-project')
GCP_LOCATION = os.environ.get('GCP_LOCATION', 'europe-west1')
GCF_SHORT_FUNCTION_NAME = os.environ.get('GCF_SHORT_FUNCTION_NAME', 'hello').replace('-', '_')
FUNCTION_NAME = 'projects/{}/locations/{}/functions/{}'.format(GCP_PROJECT_ID, GCP_LOCATION, GCF_SHORT_FUNCTION_NAME)
GCF_SOURCE_ARCHIVE_URL = os.environ.get('GCF_SOURCE_ARCHIVE_URL', '')
GCF_SOURCE_UPLOAD_URL = os.environ.get('GCF_SOURCE_UPLOAD_URL', '')
GCF_SOURCE_REPOSITORY = os.environ.get('GCF_SOURCE_REPOSITORY', 'https://source.developers.google.com/projects/{}/repos/hello-world/moveable-aliases/master'.format(GCP_PROJECT_ID))
GCF_ZIP_PATH = os.environ.get('GCF_ZIP_PATH', '')
GCF_ENTRYPOINT = os.environ.get('GCF_ENTRYPOINT', 'helloWorld')
GCF_RUNTIME = 'nodejs6'
GCP_VALIDATE_BODY = os.environ.get('GCP_VALIDATE_BODY', True)
body = {'name':FUNCTION_NAME, 
 'entryPoint':GCF_ENTRYPOINT, 
 'runtime':GCF_RUNTIME, 
 'httpsTrigger':{}}
default_args = {'start_date': dates.days_ago(1)}
if GCF_SOURCE_ARCHIVE_URL:
    body['sourceArchiveUrl'] = GCF_SOURCE_ARCHIVE_URL
else:
    if GCF_SOURCE_REPOSITORY:
        body['sourceRepository'] = {'url': GCF_SOURCE_REPOSITORY}
    else:
        if GCF_ZIP_PATH:
            body['sourceUploadUrl'] = ''
            default_args['zip_path'] = GCF_ZIP_PATH
        else:
            if GCF_SOURCE_UPLOAD_URL:
                body['sourceUploadUrl'] = GCF_SOURCE_UPLOAD_URL
            else:
                raise Exception('Please provide one of the source_code parameters')
with models.DAG('example_gcp_function',
  default_args=default_args,
  schedule_interval=None) as (dag):
    deploy_task = GcfFunctionDeployOperator(task_id='gcf_deploy_task',
      project_id=GCP_PROJECT_ID,
      location=GCP_LOCATION,
      body=body,
      validate_body=GCP_VALIDATE_BODY)
    deploy2_task = GcfFunctionDeployOperator(task_id='gcf_deploy2_task',
      location=GCP_LOCATION,
      body=body,
      validate_body=GCP_VALIDATE_BODY)
    delete_task = GcfFunctionDeleteOperator(task_id='gcf_delete_task',
      name=FUNCTION_NAME)
    deploy_task >> deploy2_task >> delete_task