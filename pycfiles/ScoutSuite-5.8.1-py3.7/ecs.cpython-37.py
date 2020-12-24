# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aliyun/facade/ecs.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 861 bytes
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
from ScoutSuite.providers.aliyun.utils import get_client
from ScoutSuite.providers.aliyun.authentication_strategy import AliyunCredentials
from ScoutSuite.providers.aliyun.facade.utils import get_response

class ECSFacade:

    def __init__(self, credentials: AliyunCredentials):
        self._credentials = credentials

    async def get_instances(self, region):
        """
        Get all instances

        :return: a list of all instances
        """
        client = get_client(credentials=(self._credentials), region=region)
        response = await get_response(client=client, request=(DescribeInstancesRequest.DescribeInstancesRequest()))
        if response:
            return response['Instances']['Instance']
        return []