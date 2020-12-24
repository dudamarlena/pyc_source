# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/example_dags/example_gcp_speech.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4035 bytes
"""
Example Airflow DAG that runs speech synthesizing and stores output in Google Cloud Storage

This DAG relies on the following OS environment variables
* GCP_PROJECT_ID - Google Cloud Platform project for the Cloud SQL instance.
* GCP_SPEECH_TEST_BUCKET - Name of the bucket in which the output file should be stored.
"""
import os
from airflow.utils import dates
from airflow import models
from airflow.contrib.operators.gcp_text_to_speech_operator import GcpTextToSpeechSynthesizeOperator
from airflow.contrib.operators.gcp_speech_to_text_operator import GcpSpeechToTextRecognizeSpeechOperator
from airflow.contrib.operators.gcp_translate_speech_operator import GcpTranslateSpeechOperator
GCP_PROJECT_ID = os.environ.get('GCP_PROJECT_ID', 'example-project')
BUCKET_NAME = os.environ.get('GCP_SPEECH_TEST_BUCKET', 'gcp-speech-test-bucket')
FILENAME = 'gcp-speech-test-file'
INPUT = {'text': 'Sample text for demo purposes'}
VOICE = {'language_code':'en-US',  'ssml_gender':'FEMALE'}
AUDIO_CONFIG = {'audio_encoding': 'LINEAR16'}
CONFIG = {'encoding':'LINEAR16', 
 'language_code':'en_US'}
AUDIO = {'uri': 'gs://{bucket}/{object}'.format(bucket=BUCKET_NAME, object=FILENAME)}
TARGET_LANGUAGE = 'pl'
FORMAT = 'text'
MODEL = 'base'
SOURCE_LANGUAGE = None
default_args = {'start_date': dates.days_ago(1)}
with models.DAG('example_gcp_speech',
  default_args=default_args, schedule_interval=None) as (dag):
    text_to_speech_synthesize_task = GcpTextToSpeechSynthesizeOperator(project_id=GCP_PROJECT_ID,
      input_data=INPUT,
      voice=VOICE,
      audio_config=AUDIO_CONFIG,
      target_bucket_name=BUCKET_NAME,
      target_filename=FILENAME,
      task_id='text_to_speech_synthesize_task')
    speech_to_text_recognize_task = GcpSpeechToTextRecognizeSpeechOperator(project_id=GCP_PROJECT_ID,
      config=CONFIG,
      audio=AUDIO,
      task_id='speech_to_text_recognize_task')
    text_to_speech_synthesize_task >> speech_to_text_recognize_task
    translate_speech_task = GcpTranslateSpeechOperator(project_id=GCP_PROJECT_ID,
      audio=AUDIO,
      config=CONFIG,
      target_language=TARGET_LANGUAGE,
      format_=FORMAT,
      source_language=SOURCE_LANGUAGE,
      model=MODEL,
      task_id='translate_speech_task')
    text_to_speech_synthesize_task >> translate_speech_task