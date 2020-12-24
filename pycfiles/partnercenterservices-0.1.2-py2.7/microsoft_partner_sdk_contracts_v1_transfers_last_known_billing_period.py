# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_transfers_last_known_billing_period.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1TransfersLastKnownBillingPeriod(Model):
    """LastKnownBillingPeriod represents billing period(start date, end date)
    information required to transfer the customer subscription.

    :param start_date: Gets or sets a value indicating the start date.
    :type start_date: datetime
    :param end_date: Gets or sets a value indicating the end date.
    :type end_date: datetime
    """
    _attribute_map = {'start_date': {'key': 'startDate', 'type': 'iso-8601'}, 'end_date': {'key': 'endDate', 'type': 'iso-8601'}}

    def __init__(self, start_date=None, end_date=None):
        super(MicrosoftPartnerSdkContractsV1TransfersLastKnownBillingPeriod, self).__init__()
        self.start_date = start_date
        self.end_date = end_date