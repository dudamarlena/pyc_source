# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aliyun/facade/actiontrail.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 835 bytes
from ScoutSuite.providers.aliyun.authentication_strategy import AliyunCredentials
from ScoutSuite.providers.aliyun.facade.utils import get_response
from aliyunsdkactiontrail.request.v20171204 import DescribeTrailsRequest
from ScoutSuite.providers.aliyun.utils import get_client

class ActiontrailFacade:

    def __init__(self, credentials: AliyunCredentials):
        self._credentials = credentials
        self._client = get_client(credentials=(self._credentials))

    async def get_trails(self):
        """
        Get all users

        :return: a list of all users
        """
        response = await get_response(client=(self._client), request=(DescribeTrailsRequest.DescribeTrailsRequest()))
        if response:
            return response['TrailList']
        return []