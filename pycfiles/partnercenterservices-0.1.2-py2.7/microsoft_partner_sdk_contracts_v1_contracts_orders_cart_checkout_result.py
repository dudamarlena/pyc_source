# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_contracts_orders_cart_checkout_result.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1ContractsOrdersCartCheckoutResult(Model):
    """Represents the result of placing an order using a cart.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param orders: Gets or sets the orders created.
    :type orders:
     list[~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1Order]
    :param order_errors: Gets or sets a collection of order failure
     information.
    :type order_errors:
     list[~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1ContractsOrdersOrderError]
    :ivar attributes: Gets the attributes.
    :vartype attributes:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceAttributes
    """
    _validation = {'attributes': {'readonly': True}}
    _attribute_map = {'orders': {'key': 'orders', 'type': '[MicrosoftPartnerSdkContractsV1Order]'}, 'order_errors': {'key': 'orderErrors', 'type': '[MicrosoftPartnerSdkContractsV1ContractsOrdersOrderError]'}, 'attributes': {'key': 'attributes', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceAttributes'}}

    def __init__(self, orders=None, order_errors=None):
        super(MicrosoftPartnerSdkContractsV1ContractsOrdersCartCheckoutResult, self).__init__()
        self.orders = orders
        self.order_errors = order_errors
        self.attributes = None
        return