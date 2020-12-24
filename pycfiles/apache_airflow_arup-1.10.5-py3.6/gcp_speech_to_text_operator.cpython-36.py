# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/gcp_speech_to_text_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3928 bytes
from airflow import AirflowException
from airflow.contrib.hooks.gcp_speech_to_text_hook import GCPSpeechToTextHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class GcpSpeechToTextRecognizeSpeechOperator(BaseOperator):
    __doc__ = "\n    Recognizes speech from audio file and returns it as text.\n\n    .. seealso::\n        For more information on how to use this operator, take a look at the guide:\n        :ref:`howto/operator:GcpSpeechToTextRecognizeSpeechOperator`\n\n    :param config: information to the recognizer that specifies how to process the request. See more:\n        https://googleapis.github.io/google-cloud-python/latest/speech/gapic/v1/types.html#google.cloud.speech_v1.types.RecognitionConfig\n    :type config: dict or google.cloud.speech_v1.types.RecognitionConfig\n    :param audio: audio data to be recognized. See more:\n        https://googleapis.github.io/google-cloud-python/latest/speech/gapic/v1/types.html#google.cloud.speech_v1.types.RecognitionAudio\n    :type audio: dict or google.cloud.speech_v1.types.RecognitionAudio\n    :param project_id: Optional, Google Cloud Platform Project ID where the Compute\n        Engine Instance exists.  If set to None or missing, the default project_id from the GCP connection is\n        used.\n    :type project_id: str\n    :param gcp_conn_id: Optional, The connection ID used to connect to Google Cloud\n        Platform. Defaults to 'google_cloud_default'.\n    :type gcp_conn_id: str\n    :param retry: (Optional) A retry object used to retry requests. If None is specified,\n            requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: (Optional) The amount of time, in seconds, to wait for the request to complete.\n        Note that if retry is specified, the timeout applies to each individual attempt.\n    :type timeout: float\n    "
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