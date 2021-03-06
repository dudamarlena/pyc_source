# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_contracts_service_costs_summary.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1ContractsServiceCostsSummary(Model):
    """Contains a summary that aggregates all services purchased by the specified
    customer during the billing period.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param billing_start_date: Gets or sets the start of the billing period.
    :type billing_start_date: datetime
    :param billing_end_date: Gets or sets the end of the billing period.
    :type billing_end_date: datetime
    :param pretax_total: Gets or sets the pre-tax total of all costs for the
     customer.
    :type pretax_total: float
    :param tax: Gets or sets the total tax incurred over all items purchased
     by the customer.
    :type tax: float
    :param after_tax_total: Gets or sets the net total cost (pretax + tax) for
     all items purchased by the customer.
    :type after_tax_total: float
    :param currency_code: Gets or sets the currency used for the costs.
    :type currency_code: str
    :param currency_symbol: Gets or sets the currency symbol used for the
     costs.
    :type currency_symbol: str
    :param customer_id: Gets or sets the ID of the customer making the
     purchase.
    :type customer_id: str
    :param links: Gets or sets the links.
    :type links:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceLinks
    :ivar attributes: Gets the attributes.
    :vartype attributes:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceAttributes
    """
    _validation = {'attributes': {'readonly': True}}
    _attribute_map = {'billing_start_date': {'key': 'billingStartDate', 'type': 'iso-8601'}, 'billing_end_date': {'key': 'billingEndDate', 'type': 'iso-8601'}, 'pretax_total': {'key': 'pretaxTotal', 'type': 'float'}, 'tax': {'key': 'tax', 'type': 'float'}, 'after_tax_total': {'key': 'afterTaxTotal', 'type': 'float'}, 'currency_code': {'key': 'currencyCode', 'type': 'str'}, 'currency_symbol': {'key': 'currencySymbol', 'type': 'str'}, 'customer_id': {'key': 'customerId', 'type': 'str'}, 'links': {'key': 'links', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceLinks'}, 'attributes': {'key': 'attributes', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceAttributes'}}

    def __init__(self, billing_start_date=None, billing_end_date=None, pretax_total=None, tax=None, after_tax_total=None, currency_code=None, currency_symbol=None, customer_id=None, links=None):
        super(MicrosoftPartnerSdkContractsV1ContractsServiceCostsSummary, self).__init__()
        self.billing_start_date = billing_start_date
        self.billing_end_date = billing_end_date
        self.pretax_total = pretax_total
        self.tax = tax
        self.after_tax_total = after_tax_total
        self.currency_code = currency_code
        self.currency_symbol = currency_symbol
        self.customer_id = customer_id
        self.links = links
        self.attributes = None
        return