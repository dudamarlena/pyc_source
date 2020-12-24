# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_transfers_last_known_billing_details.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1TransfersLastKnownBillingDetails(Model):
    """LastKnownBillingDetails represents billing information required to transfer
    the customer subscription.

    :param billing_type: Gets or sets a value indicating how the subscription
     is billed. For example, "usage" or "license". Possible values include:
     'none', 'usage', 'license'
    :type billing_type: str or
     ~microsoft.store.partnercenterservices.models.enum
    :param billing_cycle: Gets or sets a value indicating the frequency with
     which the partner is billed for this subscription.
     The default value is monthly. Possible values include: 'unknown',
     'monthly', 'annual', 'none', 'one_time'
    :type billing_cycle: str or
     ~microsoft.store.partnercenterservices.models.enum
    :param billing_period: Gets or sets a value indicating the billing period
     details for the subscription.
    :type billing_period:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1TransfersLastKnownBillingPeriod
    :param billing_amount: Gets or sets the billing amount".
    :type billing_amount: float
    :param currency: Gets or sets the billing currency".
    :type currency: str
    """
    _attribute_map = {'billing_type': {'key': 'billingType', 'type': 'str'}, 'billing_cycle': {'key': 'billingCycle', 'type': 'str'}, 'billing_period': {'key': 'billingPeriod', 'type': 'MicrosoftPartnerSdkContractsV1TransfersLastKnownBillingPeriod'}, 'billing_amount': {'key': 'billingAmount', 'type': 'float'}, 'currency': {'key': 'currency', 'type': 'str'}}

    def __init__(self, billing_type=None, billing_cycle=None, billing_period=None, billing_amount=None, currency=None):
        super(MicrosoftPartnerSdkContractsV1TransfersLastKnownBillingDetails, self).__init__()
        self.billing_type = billing_type
        self.billing_cycle = billing_cycle
        self.billing_period = billing_period
        self.billing_amount = billing_amount
        self.currency = currency