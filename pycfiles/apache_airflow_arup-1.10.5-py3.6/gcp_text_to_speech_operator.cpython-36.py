# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
    __doc__ = "\n    Synthesizes text to speech and stores it in Google Cloud Storage\n\n    .. seealso::\n        For more information on how to use this operator, take a look at the guide:\n        :ref:`howto/operator:GcpTextToSpeechSynthesizeOperator`\n\n    :param input_data: text input to be synthesized. See more:\n        https://googleapis.github.io/google-cloud-python/latest/texttospeech/gapic/v1/types.html#google.cloud.texttospeech_v1.types.SynthesisInput\n    :type input_data: dict or google.cloud.texttospeech_v1.types.SynthesisInput\n    :param voice: configuration of voice to be used in synthesis. See more:\n        https://googleapis.github.io/google-cloud-python/latest/texttospeech/gapic/v1/types.html#google.cloud.texttospeech_v1.types.VoiceSelectionParams\n    :type voice: dict or google.cloud.texttospeech_v1.types.VoiceSelectionParams\n    :param audio_config: configuration of the synthesized audio. See more:\n        https://googleapis.github.io/google-cloud-python/latest/texttospeech/gapic/v1/types.html#google.cloud.texttospeech_v1.types.AudioConfig\n    :type audio_config: dict or google.cloud.texttospeech_v1.types.AudioConfig\n    :param target_bucket_name: name of the GCS bucket in which output file should be stored\n    :type target_bucket_name: str\n    :param target_filename: filename of the output file.\n    :type target_filename: str\n    :param project_id: Optional, Google Cloud Platform Project ID where the Compute\n        Engine Instance exists.  If set to None or missing, the default project_id from the GCP connection is\n        used.\n    :type project_id: str\n    :param gcp_conn_id: Optional, The connection ID used to connect to Google Cloud\n        Platform. Defaults to 'google_cloud_default'.\n    :type gcp_conn_id: str\n    :param retry: (Optional) A retry object used to retry requests. If None is specified,\n            requests will not be retried.\n    :type retry: google.api_core.retry.Retry\n    :param timeout: (Optional) The amount of time, in seconds, to wait for the request to complete.\n        Note that if retry is specified, the timeout applies to each individual attempt.\n    :type timeout: float\n    "
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