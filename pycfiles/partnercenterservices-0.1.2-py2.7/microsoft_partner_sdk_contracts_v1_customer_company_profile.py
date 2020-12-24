# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_customer_company_profile.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1CustomerCompanyProfile(Model):
    """Additional information about the company or organization.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param tenant_id: Gets or sets the customer's tenant identifier for Azure
     AD.
     This is also called a Microsoft ID.
    :type tenant_id: str
    :param domain: Gets or sets the customer's domain. (Example :
     contoso.onmicrosoft.com)
    :type domain: str
    :param company_name: The name of the company or organization.
    :type company_name: str
    :param address: The default address for the customer's company.
    :type address:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1Address
    :param email: The email address for the customer's company.
    :type email: str
    :param links: Gets or sets the links.
    :type links:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceLinks
    :ivar attributes: Gets the attributes.
    :vartype attributes:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceAttributes
    """
    _validation = {'attributes': {'readonly': True}}
    _attribute_map = {'tenant_id': {'key': 'tenantId', 'type': 'str'}, 'domain': {'key': 'domain', 'type': 'str'}, 'company_name': {'key': 'companyName', 'type': 'str'}, 'address': {'key': 'address', 'type': 'MicrosoftPartnerSdkContractsV1Address'}, 'email': {'key': 'email', 'type': 'str'}, 'links': {'key': 'links', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceLinks'}, 'attributes': {'key': 'attributes', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceAttributes'}}

    def __init__(self, tenant_id=None, domain=None, company_name=None, address=None, email=None, links=None):
        super(MicrosoftPartnerSdkContractsV1CustomerCompanyProfile, self).__init__()
        self.tenant_id = tenant_id
        self.domain = domain
        self.company_name = company_name
        self.address = address
        self.email = email
        self.links = links
        self.attributes = None
        return