# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gmsdk/log.py
# Compiled at: 2015-04-04 04:52:46
import json
from gmsdk.connection import BaseConnection
from gmsdk.app_settings import API_VERSION as VERSION

class LogAPIService(BaseConnection):
    """
    Product service to serve various api endpoints
    """
    AVAILABLE_VERSIONS = [
     '2013.07']

    def __init__(self, **kwargs):
        self.config.resp_format = 'json'
        super(LogAPIService, self).__init__(**kwargs)
        self.config['headers'] = kwargs.pop('headers', {})

    def logs(self, request_id, version=VERSION):
        """
        Description:
        Log API integration endpoint

        Args:
        request id: RequestID to fetch request logs
        version: Version of the API being used
        Example:
        """
        self.method = 'GET'
        self.config.uri = ('/datasync/log/api/{request_id}/').format(request_id=request_id)
        self.query_params = {'version': version}
        response = self.execute()
        return response