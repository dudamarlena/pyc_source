# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/opensearchsdk/v2/index.py
# Compiled at: 2015-12-03 09:15:02
from opensearchsdk.apiclient import api_base

class IndexManager(api_base.Manager):
    """Index resource manage class"""

    def refactor(self, name, operate=None, table_name=None):
        """
        refactor index
        :param name: application name
        :param operate: weather import data for refactor
        :param table_name: import data tables name, separated by ','
        :return:
        """
        body = dict(action='createtask')
        if operate and table_name:
            body['operate'] = 'import'
            body['table_name'] = table_name
        spec_url = '/' + name
        return self.send_get(body, spec_url)