# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_migration_syndication_migration_status.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1MigrationSyndicationMigrationStatus(Model):
    """Status of migration from syndication to CSP.

    :param id: Gets or sets the migration batch ID
    :type id: str
    :param partner_id: Gets or sets the CSP Partner ID
    :type partner_id: str
    :param customers_data: Gets or sets the migration data of customers
    :type customers_data:
     list[~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1MigrationCustomerSyndicationMigration]
    """
    _attribute_map = {'id': {'key': 'id', 'type': 'str'}, 'partner_id': {'key': 'partnerId', 'type': 'str'}, 'customers_data': {'key': 'customersData', 'type': '[MicrosoftPartnerSdkContractsV1MigrationCustomerSyndicationMigration]'}}

    def __init__(self, id=None, partner_id=None, customers_data=None):
        super(MicrosoftPartnerSdkContractsV1MigrationSyndicationMigrationStatus, self).__init__()
        self.id = id
        self.partner_id = partner_id
        self.customers_data = customers_data