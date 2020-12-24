# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_reseller_program_profile.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1ResellerProgramProfile(Model):
    """The reseller program profile.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param partner_tier: Gets or sets the partner tier. Possible values
     include: 'none', 'first_tier', 'second_tier'
    :type partner_tier: str or
     ~microsoft.store.partnercenterservices.models.enum
    :param is_tip_reseller: Gets or sets a value indicating whether or not the
     reseller is a test in production reseller.
    :type is_tip_reseller: bool
    :param qualifications: Gets or sets Qualifications
    :type qualifications:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1Qualifications
    :param supported_countries: Gets or sets the supported countries.
    :type supported_countries: list[str]
    :param csl_tenant_id: Gets or sets the shared services tenant id.
    :type csl_tenant_id: str
    :ivar attributes: Gets the attributes.
    :vartype attributes:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceAttributes
    """
    _validation = {'attributes': {'readonly': True}}
    _attribute_map = {'partner_tier': {'key': 'partnerTier', 'type': 'str'}, 'is_tip_reseller': {'key': 'isTipReseller', 'type': 'bool'}, 'qualifications': {'key': 'qualifications', 'type': 'MicrosoftPartnerSdkContractsV1Qualifications'}, 'supported_countries': {'key': 'supportedCountries', 'type': '[str]'}, 'csl_tenant_id': {'key': 'cslTenantId', 'type': 'str'}, 'attributes': {'key': 'attributes', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceAttributes'}}

    def __init__(self, partner_tier=None, is_tip_reseller=None, qualifications=None, supported_countries=None, csl_tenant_id=None):
        super(MicrosoftPartnerSdkContractsV1ResellerProgramProfile, self).__init__()
        self.partner_tier = partner_tier
        self.is_tip_reseller = is_tip_reseller
        self.qualifications = qualifications
        self.supported_countries = supported_countries
        self.csl_tenant_id = csl_tenant_id
        self.attributes = None
        return