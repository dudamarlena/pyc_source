# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/projects/cpmd/server/api/django-google-address/google_address/api.py
# Compiled at: 2017-04-21 21:25:02
# Size of source mod 2**32: 692 bytes
from google_address import helpers
import requests

class GoogleAddressApi:
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address={address}'
    key = None

    def __init__(self):
        self.key = helpers.get_settings().get('API_KEY', None)
        self.language = helpers.get_settings().get('API_LANGUAGE', 'en_US')

    def _get_url(self):
        url = self.url
        if self.key:
            url = '{}&key={}'.format(url, self.key)
        if self.language:
            url = '{}&language={}'.format(url, self.language)
        return url

    def query(self, raw):
        url = self._get_url().format(address=raw)
        r = requests.get(url)
        data = r.json()
        return data