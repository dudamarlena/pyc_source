# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/narendra/.pyenv/versions/aws/lib/python3.6/site-packages/tvarit_api/resources/datasource.py
# Compiled at: 2019-07-17 09:31:51
# Size of source mod 2**32: 2439 bytes
from .base import Base

class Datasource(Base):

    def __init__(self, api):
        super(Datasource, self).__init__(api)
        self.api = api

    def find_datasource(self, datasource_name):
        """

        :param datasource_name:
        :return:
        """
        get_datasource_path = '/datasources/name/%s' % datasource_name
        r = self.api.GET(get_datasource_path)
        return r

    def get_datasource_by_id(self, datasource_id):
        """

        :param datasource_id:
        :return:
        """
        get_datasource_path = '/datasources/%s' % datasource_id
        r = self.api.GET(get_datasource_path)
        return r

    def get_datasource_by_name(self, datasource_name):
        """

        :param datasource_name:
        :return:
        """
        get_datasource_path = '/datasources/name/%s' % datasource_name
        r = self.api.GET(get_datasource_path)
        return r

    def get_datasource_id_by_name(self, datasource_name):
        """

        :param datasource_name:
        :return:
        """
        get_datasource_path = '/datasources/id/%s' % datasource_name
        r = self.api.GET(get_datasource_path)
        return r

    def create_datasource(self, datasource):
        """

        :param datasource:
        :return:
        """
        create_datasources_path = '/datasources'
        r = self.api.POST(create_datasources_path, json=datasource)
        return r

    def update_datasource(self, datasource_id, datasource):
        """

        :param datasource_id:
        :param datasource:
        :return:
        """
        update_datasource = '/datasources/%s' % datasource_id
        r = self.api.PUT(update_datasource, json=datasource)
        return r

    def list_datasources(self):
        """

        :return:
        """
        list_datasources_path = '/datasources'
        r = self.api.GET(list_datasources_path)
        return r

    def delete_datasource_by_id(self, datasource_id):
        """

        :param datasource_id:
        :return:
        """
        delete_datasource = '/datasources/%s' % datasource_id
        r = self.api.DELETE(delete_datasource)
        return r

    def delete_datasource_by_name(self, datasource_name):
        """

        :param datasource_name:
        :return:
        """
        delete_datasource = '/datasources/name/%s' % datasource_name
        r = self.api.DELETE(delete_datasource)
        return r