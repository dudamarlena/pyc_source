# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_migration_subscription_syndication_migration_status.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1MigrationSubscriptionSyndicationMigrationStatus(Model):
    """Status of subscription migration from syndication to CSP.

    :param mosi_subscription_id: Gets or sets the Mosi customer ID
    :type mosi_subscription_id: str
    :param csp_subscription_id: Gets or sets the CSP subscription ID
    :type csp_subscription_id: str
    :param csp_subscription_offer_id: Gets or sets the CSP subscription offer
     ID
    :type csp_subscription_offer_id: str
    :param csp_subscription_start_date: Gets or sets the subscription start
     date
    :type csp_subscription_start_date: datetime
    :param csp_subscription_end_date: Gets or sets the subscription end date
    :type csp_subscription_end_date: datetime
    """
    _attribute_map = {'mosi_subscription_id': {'key': 'mosiSubscriptionId', 'type': 'str'}, 'csp_subscription_id': {'key': 'cspSubscriptionId', 'type': 'str'}, 'csp_subscription_offer_id': {'key': 'cspSubscriptionOfferId', 'type': 'str'}, 'csp_subscription_start_date': {'key': 'cspSubscriptionStartDate', 'type': 'iso-8601'}, 'csp_subscription_end_date': {'key': 'cspSubscriptionEndDate', 'type': 'iso-8601'}}

    def __init__(self, mosi_subscription_id=None, csp_subscription_id=None, csp_subscription_offer_id=None, csp_subscription_start_date=None, csp_subscription_end_date=None):
        super(MicrosoftPartnerSdkContractsV1MigrationSubscriptionSyndicationMigrationStatus, self).__init__()
        self.mosi_subscription_id = mosi_subscription_id
        self.csp_subscription_id = csp_subscription_id
        self.csp_subscription_offer_id = csp_subscription_offer_id
        self.csp_subscription_start_date = csp_subscription_start_date
        self.csp_subscription_end_date = csp_subscription_end_date