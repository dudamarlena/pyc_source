# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aws/resources/acm/certificates.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 872 bytes
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.utils import get_non_provider_id

class Certificates(AWSResources):

    def __init__(self, facade, region):
        super(Certificates, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_certificates = await self.facade.acm.get_certificates(self.region)
        for raw_certificate in raw_certificates:
            name, resource = self._parse_certificate(raw_certificate)
            self[name] = resource

    def _parse_certificate(self, raw_certificate):
        raw_certificate['name'] = raw_certificate.get('DomainName')
        raw_certificate['id'] = get_non_provider_id(raw_certificate['name'])
        return (
         raw_certificate['id'], raw_certificate)