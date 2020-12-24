# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aws/facade/directconnect.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 666 bytes
from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.utils import run_concurrently

class DirectConnectFacade(AWSBaseFacade):

    async def get_connections(self, region):
        client = AWSFacadeUtils.get_client('directconnect', self.session, region)
        try:
            return await run_concurrently(lambda : client.describe_connections()['connections'])
        except Exception as e:
            try:
                print_exception('Failed to describe Direct Connect connections: {}'.format(e))
                return []
            finally:
                e = None
                del e