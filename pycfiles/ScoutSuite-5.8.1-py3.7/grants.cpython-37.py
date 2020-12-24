# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aws/resources/kms/grants.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 1190 bytes
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources

class Grants(AWSResources):

    def __init__(self, facade, region, key_id):
        super(Grants, self).__init__(facade)
        self.region = region
        self.key_id = key_id

    async def fetch_all(self):
        raw_grants = await self.facade.kms.get_grants(self.region, self.key_id)
        for raw_grant in raw_grants:
            id, grant = self._parse_grant(raw_grant)
            self[id] = grant

    def _parse_grant(self, raw_grant):
        grant_dict = {'key_id':raw_grant.get('KeyId'), 
         'grant_id':raw_grant.get('GrantId'), 
         'name':raw_grant.get('Name'), 
         'create_date':raw_grant.get('CreationDate'), 
         'grantee_principal':raw_grant.get('GranteePrincipal'), 
         'retiring_principal':raw_grant.get('ReitirngPrincipal'), 
         'issuing_account':raw_grant.get('IssuingAccount'), 
         'operations':raw_grant.get('Operations'), 
         'constraints':raw_grant.get('Constraints')}
        return (
         grant_dict['grant_id'], grant_dict)