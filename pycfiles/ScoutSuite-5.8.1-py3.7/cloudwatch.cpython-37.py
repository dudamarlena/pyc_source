# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aws/facade/cloudwatch.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 583 bytes
from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils

class CloudWatch(AWSBaseFacade):

    async def get_alarms(self, region):
        try:
            return await AWSFacadeUtils.get_all_pages('cloudwatch', region, self.session, 'describe_alarms', 'MetricAlarms')
        except Exception as e:
            try:
                print_exception('Failed to get CloudWatch alarms: {}'.format(e))
                return []
            finally:
                e = None
                del e