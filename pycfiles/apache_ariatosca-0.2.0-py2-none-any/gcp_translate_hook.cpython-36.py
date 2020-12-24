# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/gcp_translate_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3662 bytes
from google.cloud.translate_v2 import Client
from airflow.contrib.hooks.gcp_api_base_hook import GoogleCloudBaseHook

class CloudTranslateHook(GoogleCloudBaseHook):
    """CloudTranslateHook"""
    _client = None

    def __init__(self, gcp_conn_id='google_cloud_default'):
        super(CloudTranslateHook, self).__init__(gcp_conn_id)

    def get_conn(self):
        """
        Retrieves connection to Cloud Translate

        :return: Google Cloud Translate client object.
        :rtype: Client
        """
        if not self._client:
            self._client = Client(credentials=(self._get_credentials()))
        return self._client

    def translate(self, values, target_language, format_=None, source_language=None, model=None):
        """Translate a string or list of strings.

        See https://cloud.google.com/translate/docs/translating-text

        :type values: str or list
        :param values: String or list of strings to translate.

        :type target_language: str
        :param target_language: The language to translate results into. This
                                is required by the API and defaults to
                                the target language of the current instance.

        :type format_: str
        :param format_: (Optional) One of ``text`` or ``html``, to specify
                        if the input text is plain text or HTML.

        :type source_language: str or None
        :param source_language: (Optional) The language of the text to
                                be translated.

        :type model: str or None
        :param model: (Optional) The model used to translate the text, such
                      as ``'base'`` or ``'nmt'``.

        :rtype: str or list
        :returns: A list of dictionaries for each queried value. Each
                  dictionary typically contains three keys (though not
                  all will be present in all cases)

                  * ``detectedSourceLanguage``: The detected language (as an
                    ISO 639-1 language code) of the text.
                  * ``translatedText``: The translation of the text into the
                    target language.
                  * ``input``: The corresponding input value.
                  * ``model``: The model used to translate the text.

                  If only a single value is passed, then only a single
                  dictionary will be returned.
        :raises: :class:`~exceptions.ValueError` if the number of
                 values and translations differ.
        """
        client = self.get_conn()
        return client.translate(values=values,
          target_language=target_language,
          format_=format_,
          source_language=source_language,
          model=model)