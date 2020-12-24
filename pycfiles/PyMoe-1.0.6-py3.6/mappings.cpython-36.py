# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\Pymoe\Kitsu\mappings.py
# Compiled at: 2018-03-03 22:42:40
# Size of source mod 2**32: 1141 bytes
import requests
from ..errors import *
from .helpers import SearchWrapper

class KitsuMappings:

    def __init__(self, api, header):
        self.apiurl = api
        self.header = header

    def get(self, external_site: str, external_id: int):
        """
        Get a kitsu mapping by external site ID

        :param str external_site: string representing the external site
        :param int external_id: ID of the entry in the external site.
        :return: Dictionary or None (for not found)
        :rtype: Dictionary or None
        :raises: :class:`Pymoe.errors.ServerError`
        """
        r = requests.get((self.apiurl + '/mappings'), params={'filter[externalSite]':external_site,  'filter[externalId]':external_id}, headers=(self.header))
        if r.status_code != 200:
            raise ServerError
        jsd = r.json()
        if len(jsd['data']) < 1:
            return
        else:
            r = requests.get((jsd['data'][0]['relationships']['item']['links']['related']), headers=(self.header))
            if r.status_code != 200:
                return jsd
            return r.json()