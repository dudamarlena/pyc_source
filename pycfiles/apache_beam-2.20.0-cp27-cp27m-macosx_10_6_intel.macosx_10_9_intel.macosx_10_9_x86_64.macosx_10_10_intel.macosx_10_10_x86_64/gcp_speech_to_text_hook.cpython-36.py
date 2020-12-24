# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/gcp_speech_to_text_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3187 bytes
from google.cloud.speech_v1 import SpeechClient
from airflow.contrib.hooks.gcp_api_base_hook import GoogleCloudBaseHook

class GCPSpeechToTextHook(GoogleCloudBaseHook):
    """GCPSpeechToTextHook"""
    _client = None

    def __init__(self, gcp_conn_id='google_cloud_default', delegate_to=None):
        super(GCPSpeechToTextHook, self).__init__(gcp_conn_id, delegate_to)

    def get_conn(self):
        """
        Retrieves connection to Cloud Speech.

        :return: Google Cloud Speech client object.
        :rtype: google.cloud.speech_v1.SpeechClient
        """
        if not self._client:
            self._client = SpeechClient(credentials=(self._get_credentials()))
        return self._client

    def recognize_speech(self, config, audio, retry=None, timeout=None):
        """
        Recognizes audio input

        :param config: information to the recognizer that specifies how to process the request.
            https://googleapis.github.io/google-cloud-python/latest/speech/gapic/v1/types.html#google.cloud.speech_v1.types.RecognitionConfig
        :type config: dict or google.cloud.speech_v1.types.RecognitionConfig
        :param audio: audio data to be recognized
            https://googleapis.github.io/google-cloud-python/latest/speech/gapic/v1/types.html#google.cloud.speech_v1.types.RecognitionAudio
        :type audio: dict or google.cloud.speech_v1.types.RecognitionAudio
        :param retry: (Optional) A retry object used to retry requests. If None is specified,
            requests will not be retried.
        :type retry: google.api_core.retry.Retry
        :param timeout: (Optional) The amount of time, in seconds, to wait for the request to complete.
            Note that if retry is specified, the timeout applies to each individual attempt.
        :type timeout: float
        """
        client = self.get_conn()
        response = client.recognize(config=config, audio=audio, retry=retry, timeout=timeout)
        self.log.info('Recognised speech: %s' % response)
        return response