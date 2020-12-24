# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_subscriptions_support_contact.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1SubscriptionsSupportContact(Model):
    """Represents a support contact for a customer's subscription.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param support_tenant_id: Gets or sets a GUID formatted string that
     indicates the support contact's tenant identifier.
    :type support_tenant_id: str
    :param support_mpn_id: Gets or sets the support contact's Microsoft
     Partner Network (MPN) identifier.
    :type support_mpn_id: str
    :param name: Gets or sets the name of the support contact.
    :type name: str
    :param links: Gets or sets the links.
    :type links:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceLinks
    :ivar attributes: Gets the attributes.
    :vartype attributes:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceAttributes
    """
    _validation = {'attributes': {'readonly': True}}
    _attribute_map = {'support_tenant_id': {'key': 'supportTenantId', 'type': 'str'}, 'support_mpn_id': {'key': 'supportMpnId', 'type': 'str'}, 'name': {'key': 'name', 'type': 'str'}, 'links': {'key': 'links', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceLinks'}, 'attributes': {'key': 'attributes', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceAttributes'}}

    def __init__(self, support_tenant_id=None, support_mpn_id=None, name=None, links=None):
        super(MicrosoftPartnerSdkContractsV1SubscriptionsSupportContact, self).__init__()
        self.support_tenant_id = support_tenant_id
        self.support_mpn_id = support_mpn_id
        self.name = name
        self.links = links
        self.attributes = None
        return