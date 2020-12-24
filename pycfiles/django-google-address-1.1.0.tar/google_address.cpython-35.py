# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/projects/cpmd/server/api/django-google-address/google_address/google_address.py
# Compiled at: 2017-04-17 22:12:20
# Size of source mod 2**32: 843 bytes
from google_address import helpers
import requests

class GoogleAddressApi:
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address={address}'
    key = None

    def __init__(self, key=None, language=None):
        if key == None:
            self.key = helpers.get_settings().get('API_KEY', None)
        else:
            self.key = key
        if language == None:
            self.language = helpers.get_settings().get('API_LANGUAGE', 'en_US')
        else:
            self.language = language

    def _get_url(self):
        url = self.url
        if self.key:
            url = '{}&key={}'.format(url, self.key)
        if self.language:
            url = '{}&language={}'.format(url, self.language)
        return self.url

    def query(self, raw):
        url = self._get_url().format(address=raw)
        r = requests.get(url)
        data = r.json()
        return data