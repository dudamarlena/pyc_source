# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/md_translate/translator.py
# Compiled at: 2019-05-16 02:18:44
# Size of source mod 2**32: 2295 bytes
from typing import Type
import requests
from requests.exceptions import ConnectionError

class AbstractTranslator:
    BASE_API_URL = None

    def __init__(self, settings):
        self.settings = settings

    def request_translation(self, string_to_translate: str):
        response = self.request_for_translation(string_to_translate)
        if response.ok:
            translated_data = self.process_response(response)
            return translated_data
        raise ConnectionError('Something web wrong with translation requesting.')

    def request_for_translation(self, string_to_translate: str):
        raise NotImplementedError()

    def process_response(self, response: requests.Response):
        raise NotImplementedError()


def get_translator_by_name(name) -> Type[AbstractTranslator]:
    if name == 'Yandex':
        return YandexTranslator
    if name == 'Google':
        return GoogleTranslator


class YandexTranslator(AbstractTranslator):
    BASE_API_URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'

    def request_for_translation(self, string_to_translate: str) -> requests.Response:
        params = {'key':self.settings.api_key,  'lang':'-'.join([self.settings.source_lang, self.settings.target_lang])}
        data = {'text': string_to_translate}
        return requests.post((self.BASE_API_URL), params=params, data=data)

    def process_response(self, response: requests.Response) -> str:
        return response.json()['text'][0]


class GoogleTranslator(AbstractTranslator):
    BASE_API_URL = 'https://translation.googleapis.com/language/translate/v2'

    def request_for_translation(self, string_to_translate: str) -> requests.Response:
        headers = {'Authorization': 'Bearer "{}"'.format(self.settings.api_key)}
        data = {'q':string_to_translate,  'source':self.settings.source_lang, 
         'target':self.settings.target_lang, 
         'format':'text'}
        return requests.post((self.BASE_API_URL), headers=headers, data=data)

    def process_response(self, response: requests.Response) -> str:
        return response.json()['data']['translations'][0]['translatedText']