# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_links_transfer_entity_links.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1LinksTransferEntityLinks(Model):
    """Colleciton of links attached to a transfer entity.

    :param order: Gets or sets the order.
    :type order:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonLink
    :param subscription: Gets or sets the subscription.
    :type subscription:
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
    _attribute_map = {'order': {'key': 'order', 'type': 'MicrosoftPartnerSdkContractsV1CommonLink'}, 'subscription': {'key': 'subscription', 'type': 'MicrosoftPartnerSdkContractsV1CommonLink'}, 'itself': {'key': 'self', 'type': 'MicrosoftPartnerSdkContractsV1CommonLink'}, 'next': {'key': 'next', 'type': 'MicrosoftPartnerSdkContractsV1CommonLink'}, 'previous': {'key': 'previous', 'type': 'MicrosoftPartnerSdkContractsV1CommonLink'}}

    def __init__(self, order=None, subscription=None, itself=None, next=None, previous=None):
        super(MicrosoftPartnerSdkContractsV1LinksTransferEntityLinks, self).__init__()
        self.order = order
        self.subscription = subscription
        self.itself = itself
        self.next = next
        self.previous = previous