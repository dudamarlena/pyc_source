# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/gcp_speech_to_text_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3928 bytes
from airflow import AirflowException
from airflow.contrib.hooks.gcp_speech_to_text_hook import GCPSpeechToTextHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class GcpSpeechToTextRecognizeSpeechOperator(BaseOperator):
    """GcpSpeechToTextRecognizeSpeechOperator"""
    template_fields = ('audio', 'config', 'project_id', 'gcp_conn_id', 'timeout')

    @apply_defaults
    def __init__(self, audio, config, project_id=None, gcp_conn_id='google_cloud_default', retry=None, timeout=None, *args, **kwargs):
        self.audio = audio
        self.config = config
        self.project_id = project_id
        self.gcp_conn_id = gcp_conn_id
        self.retry = retry
        self.timeout = timeout
        self._validate_inputs()
        (super(GcpSpeechToTextRecognizeSpeechOperator, self).__init__)(*args, **kwargs)

    def _validate_inputs(self):
        if self.audio == '':
            raise AirflowException("The required parameter 'audio' is empty")
        if self.config == '':
            raise AirflowException("The required parameter 'config' is empty")

    def execute(self, context):
        _hook = GCPSpeechToTextHook(gcp_conn_id=(self.gcp_conn_id))
        return _hook.recognize_speech(config=(self.config),
          audio=(self.audio),
          retry=(self.retry),
          timeout=(self.timeout))