# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_links_order_links.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1LinksOrderLinks(Model):
    """Represents navigation links for an order, including
    a link to order provisioning status.

    :param provisioning_status: Gets or sets the link to the provisioning
     status.
    :type provisioning_status:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonLink
    :param self: The self uri.
    :type self:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonLink
    :param next: The next page of items.
    :type next:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonLink
    :param previous: The previous page of items.
    :type previous:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonLink
    """
    _attribute_map = {'provisioning_status': {'key': 'provisioningStatus', 'type': 'MicrosoftPartnerSdkContractsV1CommonLink'}, 'itself': {'key': 'self', 'type': 'MicrosoftPartnerSdkContractsV1CommonLink'}, 'next': {'key': 'next', 'type': 'MicrosoftPartnerSdkContractsV1CommonLink'}, 'previous': {'key': 'previous', 'type': 'MicrosoftPartnerSdkContractsV1CommonLink'}}

    def __init__(self, provisioning_status=None, itself=None, next=None, previous=None):
        super(MicrosoftPartnerSdkContractsV1LinksOrderLinks, self).__init__()
        self.provisioning_status = provisioning_status
        self.itself = itself
        self.next = next
        self.previous = previous