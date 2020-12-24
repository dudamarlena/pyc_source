# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aws/resources/kms/aliases.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 859 bytes
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources

class Aliases(AWSResources):

    def __init__(self, facade, region):
        super(Aliases, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_aliases = await self.facade.kms.get_aliases(self.region)
        for raw_alias in raw_aliases:
            id, alias = self._parse_alias(raw_alias)
            self[id] = alias

    def _parse_alias(self, raw_alias):
        alias_dict = {'name':raw_alias.get('AliasName').lstrip('alias/'), 
         'arn':raw_alias.get('AliasArn'), 
         'key_id':raw_alias.get('TargetKeyId')}
        return (alias_dict['name'], alias_dict)