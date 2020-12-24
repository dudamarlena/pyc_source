# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/opensearchsdk/v2/data.py
# Compiled at: 2016-09-02 10:11:10
from opensearchsdk.apiclient import api_base

class DataManager(api_base.Manager):
    """Data Process resource manage class"""

    def create(self, app_name, table_name, items):
        """
        create data process to application
        :param app_name: app name
        :param table_name: table name of upload items
        :param items: items in json format
        :return:{"status":"OK","request_id":"10373587"}
        """
        body = dict(table_name=table_name, items=items)
        spec_url = '/' + app_name
        return self.send_post(body, spec_url)