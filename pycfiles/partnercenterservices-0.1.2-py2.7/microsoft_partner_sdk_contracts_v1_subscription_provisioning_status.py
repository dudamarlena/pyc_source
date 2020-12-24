# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_subscription_provisioning_status.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1SubscriptionProvisioningStatus(Model):
    """Provides information about the provisioning status of a subscription.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param sku_id: Gets or sets a GUID formatted string that identifies the
     product SKU.
    :type sku_id: str
    :param status: Gets or sets a value indicating whether this subscription
     is provisioned.
    :type status: str
    :param quantity: Gets or sets the subscription quantity after
     provisioning.
    :type quantity: int
    :param end_date: Gets or sets the end date of the subscription.
    :type end_date: datetime
    :ivar attributes: Gets the attributes.
    :vartype attributes:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceAttributes
    """
    _validation = {'attributes': {'readonly': True}}
    _attribute_map = {'sku_id': {'key': 'skuId', 'type': 'str'}, 'status': {'key': 'status', 'type': 'str'}, 'quantity': {'key': 'quantity', 'type': 'int'}, 'end_date': {'key': 'endDate', 'type': 'iso-8601'}, 'attributes': {'key': 'attributes', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceAttributes'}}

    def __init__(self, sku_id=None, status=None, quantity=None, end_date=None):
        super(MicrosoftPartnerSdkContractsV1SubscriptionProvisioningStatus, self).__init__()
        self.sku_id = sku_id
        self.status = status
        self.quantity = quantity
        self.end_date = end_date
        self.attributes = None
        return