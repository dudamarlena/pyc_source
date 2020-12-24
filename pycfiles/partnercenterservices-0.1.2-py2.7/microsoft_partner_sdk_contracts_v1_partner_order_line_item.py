# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_partner_order_line_item.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1PartnerOrderLineItem(Model):
    """Defines a line item in a  partner order.

    :param id: The line item unique identifier.
    :type id: str
    :param offer: The offer information.
    :type offer:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1PartnerOffer
    :param quantity: Quantity of item sold.
    :type quantity: int
    :param subtotal: The amount of the order before taxes are applied.
    :type subtotal: float
    :param tax_amount: The tax amount applied to the order.
    :type tax_amount: float
    :param total_amount: The total amount of the order after taxes are
     applied.
    :type total_amount: float
    :param auto_renews: Defines whether auto-renew is enabled.
    :type auto_renews: bool
    :param expiration_date: The expiration date and time.
    :type expiration_date: datetime
    """
    _attribute_map = {'id': {'key': 'id', 'type': 'str'}, 'offer': {'key': 'offer', 'type': 'MicrosoftPartnerSdkContractsV1PartnerOffer'}, 'quantity': {'key': 'quantity', 'type': 'int'}, 'subtotal': {'key': 'subtotal', 'type': 'float'}, 'tax_amount': {'key': 'taxAmount', 'type': 'float'}, 'total_amount': {'key': 'totalAmount', 'type': 'float'}, 'auto_renews': {'key': 'autoRenews', 'type': 'bool'}, 'expiration_date': {'key': 'expirationDate', 'type': 'iso-8601'}}

    def __init__(self, id=None, offer=None, quantity=None, subtotal=None, tax_amount=None, total_amount=None, auto_renews=None, expiration_date=None):
        super(MicrosoftPartnerSdkContractsV1PartnerOrderLineItem, self).__init__()
        self.id = id
        self.offer = offer
        self.quantity = quantity
        self.subtotal = subtotal
        self.tax_amount = tax_amount
        self.total_amount = total_amount
        self.auto_renews = auto_renews
        self.expiration_date = expiration_date