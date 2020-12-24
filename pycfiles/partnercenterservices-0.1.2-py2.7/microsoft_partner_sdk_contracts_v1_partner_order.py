# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_partner_order.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1PartnerOrder(Model):
    """Defines an order placed by a partner for a partner offering.

    :param id: The order Id.
    :type id: str
    :param creation_date: The date the order was created.
    :type creation_date: datetime
    :param currency_code: The currency code.
    :type currency_code: str
    :param currency_symbol: The currency symbol.
    :type currency_symbol: str
    :param status: The status of the order. Possible values include: 'none',
     'purchased', 'refunded'
    :type status: str or ~microsoft.store.partnercenterservices.models.enum
    :param subtotal: The amount of the order before taxes are applied.
    :type subtotal: float
    :param tax_amount: The tax amount applied to the order.
    :type tax_amount: float
    :param total_amount: The total amount of the order after taxes are
     applied.
    :type total_amount: float
    :param line_items: The line items included in the order.
    :type line_items:
     list[~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1PartnerOrderLineItem]
    """
    _attribute_map = {'id': {'key': 'id', 'type': 'str'}, 'creation_date': {'key': 'creationDate', 'type': 'iso-8601'}, 'currency_code': {'key': 'currencyCode', 'type': 'str'}, 'currency_symbol': {'key': 'currencySymbol', 'type': 'str'}, 'status': {'key': 'status', 'type': 'str'}, 'subtotal': {'key': 'subtotal', 'type': 'float'}, 'tax_amount': {'key': 'taxAmount', 'type': 'float'}, 'total_amount': {'key': 'totalAmount', 'type': 'float'}, 'line_items': {'key': 'lineItems', 'type': '[MicrosoftPartnerSdkContractsV1PartnerOrderLineItem]'}}

    def __init__(self, id=None, creation_date=None, currency_code=None, currency_symbol=None, status=None, subtotal=None, tax_amount=None, total_amount=None, line_items=None):
        super(MicrosoftPartnerSdkContractsV1PartnerOrder, self).__init__()
        self.id = id
        self.creation_date = creation_date
        self.currency_code = currency_code
        self.currency_symbol = currency_symbol
        self.status = status
        self.subtotal = subtotal
        self.tax_amount = tax_amount
        self.total_amount = total_amount
        self.line_items = line_items