# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aws/facade/ses.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 2173 bytes
from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.utils import map_concurrently
from ScoutSuite.providers.utils import run_concurrently

class SESFacade(AWSBaseFacade):

    async def get_identities(self, region: str):
        try:
            identity_names = await AWSFacadeUtils.get_all_pages('ses', region, self.session, 'list_identities', 'Identities')
            return await map_concurrently((self._get_identity_dkim_attributes), identity_names, region=region)
        except Exception as e:
            try:
                print_exception('Failed to get SES identities: {}'.format(e))
                return []
            finally:
                e = None
                del e

    async def _get_identity_dkim_attributes(self, identity_name: str, region: str):
        ses_client = AWSFacadeUtils.get_client('ses', self.session, region)
        try:
            dkim_attributes = await run_concurrently(lambda : ses_client.get_identity_dkim_attributes(Identities=[identity_name])['DkimAttributes'][identity_name])
        except Exception as e:
            try:
                print_exception('Failed to get SES DKIM attributes: {}'.format(e))
                raise
            finally:
                e = None
                del e

        return (
         identity_name, dkim_attributes)

    async def get_identity_policies(self, region: str, identity_name: str):
        ses_client = AWSFacadeUtils.get_client('ses', self.session, region)
        try:
            policy_names = await run_concurrently(lambda : ses_client.list_identity_policies(Identity=identity_name)['PolicyNames'])
        except Exception as e:
            try:
                print_exception('Failed to list SES policies: {}'.format(e))
                policy_names = []
            finally:
                e = None
                del e

        if len(policy_names) == 0:
            return {}
        try:
            return await run_concurrently(lambda : ses_client.get_identity_policies(Identity=identity_name, PolicyNames=policy_names)['Policies'])
        except Exception as e:
            try:
                print_exception('Failed to get SES policies: {}'.format(e))
                return
            finally:
                e = None
                del e