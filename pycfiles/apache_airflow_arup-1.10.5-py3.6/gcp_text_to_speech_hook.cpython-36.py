# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/gcp_text_to_speech_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3889 bytes
from google.cloud.texttospeech_v1 import TextToSpeechClient
from airflow.contrib.hooks.gcp_api_base_hook import GoogleCloudBaseHook

class GCPTextToSpeechHook(GoogleCloudBaseHook):
    __doc__ = '\n    Hook for Google Cloud Text to Speech API.\n\n    :param gcp_conn_id: The connection ID to use when fetching connection info.\n    :type gcp_conn_id: str\n    :param delegate_to: The account to impersonate, if any.\n        For this to work, the service account making the request must have\n        domain-wide delegation enabled.\n    :type delegate_to: str\n    '
    _client = None

    def __init__(self, gcp_conn_id='google_cloud_default', delegate_to=None):
        super(GCPTextToSpeechHook, self).__init__(gcp_conn_id, delegate_to)

    def get_conn(self):
        """
        Retrieves connection to Cloud Text to Speech.

        :return: Google Cloud Text to Speech client object.
        :rtype: google.cloud.texttospeech_v1.TextToSpeechClient
        """
        if not self._client:
            self._client = TextToSpeechClient(credentials=(self._get_credentials()))
        return self._client

    def synthesize_speech(self, input_data, voice, audio_config, retry=None, timeout=None):
        """
        Synthesizes text input

        :param input_data: text input to be synthesized. See more:
            https://googleapis.github.io/google-cloud-python/latest/texttospeech/gapic/v1/types.html#google.cloud.texttospeech_v1.types.SynthesisInput
        :type input_data: dict or google.cloud.texttospeech_v1.types.SynthesisInput
        :param voice: configuration of voice to be used in synthesis. See more:
            https://googleapis.github.io/google-cloud-python/latest/texttospeech/gapic/v1/types.html#google.cloud.texttospeech_v1.types.VoiceSelectionParams
        :type voice: dict or google.cloud.texttospeech_v1.types.VoiceSelectionParams
        :param audio_config: configuration of the synthesized audio. See more:
            https://googleapis.github.io/google-cloud-python/latest/texttospeech/gapic/v1/types.html#google.cloud.texttospeech_v1.types.AudioConfig
        :type audio_config: dict or google.cloud.texttospeech_v1.types.AudioConfig
        :return: SynthesizeSpeechResponse See more:
            https://googleapis.github.io/google-cloud-python/latest/texttospeech/gapic/v1/types.html#google.cloud.texttospeech_v1.types.SynthesizeSpeechResponse
        :rtype: object
        :param retry: (Optional) A retry object used to retry requests. If None is specified,
                requests will not be retried.
        :type retry: google.api_core.retry.Retry
        :param timeout: (Optional) The amount of time, in seconds, to wait for the request to complete.
            Note that if retry is specified, the timeout applies to each individual attempt.
        :type timeout: float
        """
        client = self.get_conn()
        self.log.info('Synthesizing input: %s' % input_data)
        return client.synthesize_speech(input_=input_data,
          voice=voice,
          audio_config=audio_config,
          retry=retry,
          timeout=timeout)