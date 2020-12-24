# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/narendra/.pyenv/versions/aws/lib/python3.6/site-packages/tvarit_api/resources/search.py
# Compiled at: 2019-07-17 09:31:51
# Size of source mod 2**32: 1249 bytes
from .base import Base

class Search(Base):

    def __init__(self, api):
        super(Search, self).__init__(api)
        self.api = api

    def search_dashboards(self, query=None, tag=None, type_=None, dashboard_ids=None, folder_ids=None, starred=None, limit=None):
        """

        :param query:
        :param tag:
        :param type_:
        :param dashboard_ids:
        :param folder_ids:
        :param starred:
        :param limit:
        :return:
        """
        list_dashboard_path = '/search'
        params = []
        if query:
            params.append('query=%s' % query)
        if tag:
            params.append('tag=%s' % tag)
        if type_:
            params.append('type=%s' % type_)
        if dashboard_ids:
            params.append('dashboardIds=%s' % dashboard_ids)
        if folder_ids:
            params.append('folderIds=%s' % folder_ids)
        if starred:
            params.append('starred=%s' % starred)
        if limit:
            params.append('limit=%s' % limit)
        list_dashboard_path += '?'
        list_dashboard_path += '&'.join(params)
        r = self.api.GET(list_dashboard_path)
        return r