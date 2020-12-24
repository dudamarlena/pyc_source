# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/example_dags/example_gcp_video_intelligence.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4725 bytes
__doc__ = '\nExample Airflow DAG that demonstrates operators for the Google Cloud Video Intelligence service in the Google\nCloud Platform.\n\nThis DAG relies on the following OS environment variables:\n\n* GCP_BUCKET_NAME - Google Cloud Storage bucket where the file exists.\n'
import os
from google.api_core.retry import Retry
import airflow
from airflow import models
from airflow.contrib.operators.gcp_video_intelligence_operator import CloudVideoIntelligenceDetectVideoLabelsOperator, CloudVideoIntelligenceDetectVideoExplicitContentOperator, CloudVideoIntelligenceDetectVideoShotsOperator
from airflow.operators.bash_operator import BashOperator
default_args = {'start_date': airflow.utils.dates.days_ago(1)}
GCP_BUCKET_NAME = os.environ.get('GCP_VIDEO_INTELLIGENCE_BUCKET_NAME', 'test-bucket-name')
INPUT_URI = 'gs://{}/video.mp4'.format(GCP_BUCKET_NAME)
with models.DAG('example_gcp_video_intelligence',
  default_args=default_args,
  schedule_interval=None) as (dag):
    detect_video_label = CloudVideoIntelligenceDetectVideoLabelsOperator(input_uri=INPUT_URI,
      output_uri=None,
      video_context=None,
      timeout=5,
      task_id='detect_video_label')
    detect_video_label_result = BashOperator(bash_command="echo {{ task_instance.xcom_pull('detect_video_label')['annotationResults'][0]['shotLabelAnnotations'][0]['entity']}}",
      task_id='detect_video_label_result')
    detect_video_explicit_content = CloudVideoIntelligenceDetectVideoExplicitContentOperator(input_uri=INPUT_URI,
      output_uri=None,
      video_context=None,
      retry=Retry(maximum=10.0),
      timeout=5,
      task_id='detect_video_explicit_content')
    detect_video_explicit_content_result = BashOperator(bash_command="echo {{ task_instance.xcom_pull('detect_video_explicit_content')['annotationResults'][0]['explicitAnnotation']['frames'][0]}}",
      task_id='detect_video_explicit_content_result')
    detect_video_shots = CloudVideoIntelligenceDetectVideoShotsOperator(input_uri=INPUT_URI,
      output_uri=None,
      video_context=None,
      retry=Retry(maximum=10.0),
      timeout=5,
      task_id='detect_video_shots')
    detect_video_shots_result = BashOperator(bash_command="echo {{ task_instance.xcom_pull('detect_video_shots')['annotationResults'][0]['shotAnnotations'][0]}}",
      task_id='detect_video_shots_result')
    detect_video_label >> detect_video_label_result
    detect_video_explicit_content >> detect_video_explicit_content_result
    detect_video_shots >> detect_video_shots_result