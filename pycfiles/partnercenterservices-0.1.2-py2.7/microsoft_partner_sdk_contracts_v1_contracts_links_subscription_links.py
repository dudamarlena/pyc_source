# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_contracts_links_subscription_links.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1ContractsLinksSubscriptionLinks(Model):
    """Describes the collection of links attached to a subscription resource.

    :param offer: Gets or sets the offer.
    :type offer:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonLink
    :param entitlement: Gets or sets the entitlement.
    :type entitlement:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonLink
    :param parent_subscription: Gets or sets the parent subscription.
    :type parent_subscription:
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
    _attribute_map = {'offer': {'key': 'offer', 'type': 'MicrosoftPartnerSdkContractsV1CommonLink'}, 'entitlement': {'key': 'entitlement', 'type': 'MicrosoftPartnerSdkContractsV1CommonLink'}, 'parent_subscription': {'key': 'parentSubscription', 'type': 'MicrosoftPartnerSdkContractsV1CommonLink'}, 'itself': {'key': 'self', 'type': 'MicrosoftPartnerSdkContractsV1CommonLink'}, 'next': {'key': 'next', 'type': 'MicrosoftPartnerSdkContractsV1CommonLink'}, 'previous': {'key': 'previous', 'type': 'MicrosoftPartnerSdkContractsV1CommonLink'}}

    def __init__(self, offer=None, entitlement=None, parent_subscription=None, itself=None, next=None, previous=None):
        super(MicrosoftPartnerSdkContractsV1ContractsLinksSubscriptionLinks, self).__init__()
        self.offer = offer
        self.entitlement = entitlement
        self.parent_subscription = parent_subscription
        self.itself = itself
        self.next = next
        self.previous = previous