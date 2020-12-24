# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_invoice_detail.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1InvoiceDetail(Model):
    """Represents the detailed information of an invoice.
    An invoice contains a collection of billed items, and each item is
    represented by an InvoiceDetail resource.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param invoice_line_item_type: Gets or sets the type of invoice detail.
     Possible values include: 'none', 'usage_line_items', 'billing_line_items'
    :type invoice_line_item_type: str or
     ~microsoft.store.partnercenterservices.models.enum
    :param billing_provider: Gets or sets the billing provider. Possible
     values include: 'none', 'office', 'azure', 'azure_data_market'
    :type billing_provider: str or
     ~microsoft.store.partnercenterservices.models.enum
    :param links: Gets or sets the links.
    :type links:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceLinks
    :ivar attributes: Gets the attributes.
    :vartype attributes:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceAttributes
    """
    _validation = {'attributes': {'readonly': True}}
    _attribute_map = {'invoice_line_item_type': {'key': 'invoiceLineItemType', 'type': 'str'}, 'billing_provider': {'key': 'billingProvider', 'type': 'str'}, 'links': {'key': 'links', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceLinks'}, 'attributes': {'key': 'attributes', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceAttributes'}}

    def __init__(self, invoice_line_item_type=None, billing_provider=None, links=None):
        super(MicrosoftPartnerSdkContractsV1InvoiceDetail, self).__init__()
        self.invoice_line_item_type = invoice_line_item_type
        self.billing_provider = billing_provider
        self.links = links
        self.attributes = None
        return