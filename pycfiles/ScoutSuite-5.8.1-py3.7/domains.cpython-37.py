# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aws/resources/route53/domains.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 1016 bytes
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.utils import get_non_provider_id

class Domains(AWSResources):

    def __init__(self, facade, region):
        super(Domains, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_domains = await self.facade.route53.get_domains(self.region)
        for raw_domain in raw_domains:
            id, domain = self._parse_domain(raw_domain)
            self[id] = domain

    def _parse_domain(self, raw_domain):
        domain_dict = {}
        domain_dict['id'] = get_non_provider_id(raw_domain.get('DomainName'))
        domain_dict['name'] = raw_domain.get('DomainName')
        domain_dict['auto_renew'] = raw_domain.get('AutoRenew')
        domain_dict['transfer_lock'] = raw_domain.get('TransferLock')
        domain_dict['expiry'] = raw_domain.get('Expiry')
        return (domain_dict['id'], domain_dict)