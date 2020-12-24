# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_links_order_line_item_links.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1LinksOrderLineItemLinks(Model):
    """Represents navigation links for an order line item, including
    a link to the full subscription associated with the order.

    :param subscription: Gets or sets the link to the full subscription
     information.
    :type subscription:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonLink
    :param sku: Gets or sets the SKU URI.
    :type sku:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonLink
    :param provisioning_status: Gets or sets the Provisioning Status URI.
    :type provisioning_status:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonLink
    """
    _attribute_map = {'subscription': {'key': 'subscription', 'type': 'MicrosoftPartnerSdkContractsV1CommonLink'}, 'sku': {'key': 'sku', 'type': 'MicrosoftPartnerSdkContractsV1CommonLink'}, 'provisioning_status': {'key': 'provisioningStatus', 'type': 'MicrosoftPartnerSdkContractsV1CommonLink'}}

    def __init__(self, subscription=None, sku=None, provisioning_status=None):
        super(MicrosoftPartnerSdkContractsV1LinksOrderLineItemLinks, self).__init__()
        self.subscription = subscription
        self.sku = sku
        self.provisioning_status = provisioning_status