# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aliyun/facade/oss.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 620 bytes
from ScoutSuite.providers.aliyun.authentication_strategy import AliyunCredentials
from ScoutSuite.providers.aliyun.utils import get_oss_client

class OSSFacade:

    def __init__(self, credentials: AliyunCredentials):
        self._credentials = credentials

    async def get_buckets(self):
        """
        Get all instances

        :return: a list of all instances
        """
        client = get_oss_client(credentials=(self._credentials))
        response = client.list_buckets()
        if response:
            return response.buckets
        return []