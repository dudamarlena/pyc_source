# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\Pymoe\Kitsu\manga.py
# Compiled at: 2017-08-03 07:38:56
# Size of source mod 2**32: 1327 bytes
import requests
from ..errors import *
from .helpers import SearchWrapper

class KitsuManga:

    def __init__(self, api, header):
        self.apiurl = api
        self.header = header

    def get(self, aid):
        """
        Get manga information by id.

        :param int aid: ID of the manga.
        :return: Dictionary or None (for not found)
        :rtype: Dictionary or None
        :raises: :class:`Pymoe.errors.ServerError`
        """
        r = requests.get((self.apiurl + '/manga/{}'.format(aid)), headers=(self.header))
        if r.status_code != 200:
            if r.status_code == 404:
                return
            raise ServerError
        return r.json()

    def search(self, term):
        """
        Search for manga by term.

        :param str term: What to search for.
        :return: The results as a SearchWrapper iterator.
        :rtype: SearchWrapper
        """
        r = requests.get((self.apiurl + '/manga'), params={'filter[text]': term}, headers=(self.header))
        if r.status_code != 200:
            raise ServerError
        jsd = r.json()
        if jsd['meta']['count']:
            return SearchWrapper(jsd['data'], jsd['links']['next'] if 'next' in jsd['links'] else None, self.header)
        else:
            return