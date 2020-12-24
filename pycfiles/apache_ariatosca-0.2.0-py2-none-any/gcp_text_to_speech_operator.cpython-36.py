# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/gcp_text_to_speech_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 5491 bytes
from tempfile import NamedTemporaryFile
from airflow import AirflowException
from airflow.contrib.hooks.gcp_text_to_speech_hook import GCPTextToSpeechHook
from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class GcpTextToSpeechSynthesizeOperator(BaseOperator):
    """GcpTextToSpeechSynthesizeOperator"""
    template_fields = ('input_data', 'voice', 'audio_config', 'project_id', 'gcp_conn_id',
                       'target_bucket_name', 'target_filename')

    @apply_defaults
    def __init__(self, input_data, voice, audio_config, target_bucket_name, target_filename, project_id=None, gcp_conn_id='google_cloud_default', retry=None, timeout=None, *args, **kwargs):
        self.input_data = input_data
        self.voice = voice
        self.audio_config = audio_config
        self.target_bucket_name = target_bucket_name
        self.target_filename = target_filename
        self.project_id = project_id
        self.gcp_conn_id = gcp_conn_id
        self.retry = retry
        self.timeout = timeout
        self._validate_inputs()
        (super(GcpTextToSpeechSynthesizeOperator, self).__init__)(*args, **kwargs)

    def _validate_inputs(self):
        for parameter in ('input_data', 'voice', 'audio_config', 'target_bucket_name',
                          'target_filename'):
            if getattr(self, parameter) == '':
                raise AirflowException("The required parameter '{}' is empty".format(parameter))

    def execute(self, context):
        gcp_text_to_speech_hook = GCPTextToSpeechHook(gcp_conn_id=(self.gcp_conn_id))
        result = gcp_text_to_speech_hook.synthesize_speech(input_data=(self.input_data),
          voice=(self.voice),
          audio_config=(self.audio_config),
          retry=(self.retry),
          timeout=(self.timeout))
        with NamedTemporaryFile() as (temp_file):
            temp_file.write(result.audio_content)
            cloud_storage_hook = GoogleCloudStorageHook(google_cloud_storage_conn_id=(self.gcp_conn_id))
            cloud_storage_hook.upload(bucket=(self.target_bucket_name),
              object=(self.target_filename),
              filename=(temp_file.name))