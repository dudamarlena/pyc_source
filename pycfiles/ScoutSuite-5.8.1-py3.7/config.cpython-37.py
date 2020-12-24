# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aws/facade/config.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 1779 bytes
from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.utils import run_concurrently

class ConfigFacade(AWSBaseFacade):

    async def get_rules(self, region):
        try:
            return await AWSFacadeUtils.get_all_pages('config', region, self.session, 'describe_config_rules', 'ConfigRules')
        except Exception as e:
            try:
                print_exception('Failed to get Config ruless: {}'.format(e))
                return []
            finally:
                e = None
                del e

    async def get_recorders(self, region: str):
        client = AWSFacadeUtils.get_client('config', self.session, region)
        try:
            recorders = (await run_concurrently(client.describe_configuration_recorders))['ConfigurationRecorders']
        except Exception as e:
            try:
                print_exception('Failed to get Config recorders: {}'.format(e))
                recorders = []
            finally:
                e = None
                del e

        try:
            recorder_statuses_list = (await run_concurrently(client.describe_configuration_recorder_status))['ConfigurationRecordersStatus']
        except Exception as e:
            try:
                print_exception('Failed to get Config recorder statuses: {}'.format(e))
            finally:
                e = None
                del e

        else:
            recorder_statuses_map = {recorder['name']:recorder for recorder in recorder_statuses_list}
            for recorder in recorders:
                recorder['ConfigurationRecordersStatus'] = recorder_statuses_map[recorder['name']]

        return recorders