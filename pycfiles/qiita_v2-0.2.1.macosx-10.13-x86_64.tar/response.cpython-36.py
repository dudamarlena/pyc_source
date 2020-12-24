# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/komurasaki/.anyenv/envs/pyenv/versions/3.6.3/lib/python3.6/site-packages/qiita_v2/response.py
# Compiled at: 2018-11-06 19:47:21
# Size of source mod 2**32: 1903 bytes
""" qiita.QiitaResponse
Handling QiitaClient response

created by @petitviolet
"""
import re

class QiitaResponse:
    __doc__ = ' Wrap requests.Response\n    '

    def __init__(self, response):
        """ initialize with requests.Response
        :params response: instance of requests.Response
        """
        self.response = response
        self.headers = response.headers
        self.table = {}

    def to_json(self):
        """ Returns jsonified contents of response
        """
        return self.response.json()

    @property
    def status(self):
        """ Returns status code
        """
        return self.response.status_code

    def _get_from_header(self, key):
        """ extrace value from header if key exists
        """
        if key in self.headers:
            return self.headers[key]

    @property
    def result_count(self):
        """ Returns count of result
        """
        return self._get_from_header('Total-Count')

    @property
    def remain_request_count(self):
        """ Returns how many api counts remaining
        """
        return self._get_from_header('Rate-Remaining')

    @property
    def links(self):
        """ split 'Link' header for pagenation
        """
        if self.table:
            return self.table
        else:
            links = self._get_from_header('Link').split(',')
            pattern = re.compile('<(.+?)>; rel="(.+?)"')
            for link in links:
                url, rel = pattern.findall(link.strip())[0]
                self.table[rel] = url

            return self.table

    @property
    def link_first(self):
        """ Returns link to first page
        """
        return self.links['first']

    @property
    def link_next(self):
        """ Returns link to next page
        """
        return self.links['next']

    @property
    def link_last(self):
        """ Returns link to last page
        """
        return self.links['last']