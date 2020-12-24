# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_contracts_rate_cards_azure_offer_term.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1ContractsRateCardsAzureOfferTerm(Model):
    """Represents an offer term tied to an Azure rate card.

    :param name: Gets or sets the offer name.
    :type name: str
    :param discount: Gets or sets the applied discount if any.
    :type discount: float
    :param excluded_meter_ids: Gets or sets the excluded meter IDs from the
     offer term, if any.
    :type excluded_meter_ids: list[str]
    :param effective_date: Gets or sets the effective start date of the offer
     term.
    :type effective_date: datetime
    """
    _attribute_map = {'name': {'key': 'name', 'type': 'str'}, 'discount': {'key': 'discount', 'type': 'float'}, 'excluded_meter_ids': {'key': 'excludedMeterIds', 'type': '[str]'}, 'effective_date': {'key': 'effectiveDate', 'type': 'iso-8601'}}

    def __init__(self, name=None, discount=None, excluded_meter_ids=None, effective_date=None):
        super(MicrosoftPartnerSdkContractsV1ContractsRateCardsAzureOfferTerm, self).__init__()
        self.name = name
        self.discount = discount
        self.excluded_meter_ids = excluded_meter_ids
        self.effective_date = effective_date