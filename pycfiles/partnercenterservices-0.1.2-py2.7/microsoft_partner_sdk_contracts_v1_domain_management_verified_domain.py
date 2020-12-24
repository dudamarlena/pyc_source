# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_domain_management_verified_domain.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1DomainManagementVerifiedDomain(Model):
    """Represents VerifiedDomain request and response.

    :param verified_domain_name: Verified Domain Name
    :type verified_domain_name: str
    :param domain: Domain
    :type domain:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1DomainManagementDomain
    :param domain_federation_settings: Domain federation settings
    :type domain_federation_settings:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1DomainManagementDomainFederationSettings
    """
    _attribute_map = {'verified_domain_name': {'key': 'verifiedDomainName', 'type': 'str'}, 'domain': {'key': 'domain', 'type': 'MicrosoftPartnerSdkContractsV1DomainManagementDomain'}, 'domain_federation_settings': {'key': 'domainFederationSettings', 'type': 'MicrosoftPartnerSdkContractsV1DomainManagementDomainFederationSettings'}}

    def __init__(self, verified_domain_name=None, domain=None, domain_federation_settings=None):
        super(MicrosoftPartnerSdkContractsV1DomainManagementVerifiedDomain, self).__init__()
        self.verified_domain_name = verified_domain_name
        self.domain = domain
        self.domain_federation_settings = domain_federation_settings