# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/opensearchsdk/v2/log.py
# Compiled at: 2015-12-06 00:16:53
from opensearchsdk.apiclient import api_base

class LogManager(api_base.Manager):
    """Error Log resource manage class"""

    def get(self, name, page, page_size, sort_mode):
        """
        get error log of application
        :param name: application name
        :param page: (str)page number
        :param page_size: (int)page size
        :param sort_mode: 'ASC' or 'DESC'
        :return: (json)log content
        """
        body = dict(page=page, page_size=str(page_size), sort_mode=sort_mode)
        spec_url = '/' + name
        return self.send_get(body, spec_url)