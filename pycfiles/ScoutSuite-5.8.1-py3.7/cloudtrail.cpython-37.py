# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aws/facade/cloudtrail.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 1794 bytes
from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.utils import get_and_set_concurrently
from ScoutSuite.providers.utils import run_concurrently

class CloudTrailFacade(AWSBaseFacade):

    async def get_trails(self, region):
        client = AWSFacadeUtils.get_client('cloudtrail', self.session, region)
        try:
            try:
                trails = await run_concurrently(lambda : client.describe_trails()['trailList'])
            except Exception as e:
                try:
                    print_exception('Failed to describe CloudTrail trail: {}'.format(e))
                    trails = []
                finally:
                    e = None
                    del e

            else:
                await get_and_set_concurrently([
                 self._get_and_set_status, self._get_and_set_selectors],
                  trails, region=region)
        finally:
            return

        return trails

    async def _get_and_set_status(self, trail: {}, region: str):
        client = AWSFacadeUtils.get_client('cloudtrail', self.session, region)
        try:
            trail_status = await run_concurrently(lambda : client.get_trail_status(Name=(trail['TrailARN'])))
            trail.update(trail_status)
        except Exception as e:
            try:
                print_exception('Failed to get CloudTrail trail status: {}'.format(e))
            finally:
                e = None
                del e

    async def _get_and_set_selectors(self, trail: {}, region: str):
        client = AWSFacadeUtils.get_client('cloudtrail', self.session, region)
        try:
            trail['EventSelectors'] = await run_concurrently(lambda : client.get_event_selectors(TrailName=(trail['TrailARN']))['EventSelectors'])
        except Exception as e:
            try:
                print_exception('Failed to get CloudTrail event selectors: {}'.format(e))
            finally:
                e = None
                del e