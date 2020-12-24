# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_migration_syndication_migration.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1MigrationSyndicationMigration(Model):
    """Batch for migration from syndication to CSP.

    :param id: Gets or sets the migration batch ID
    :type id: str
    :param partner_id: Gets or sets the CSP Partner ID
    :type partner_id: str
    :param created_date: Gets or sets the batch created date
    :type created_date: datetime
    :param mosi_customer_ids: Gets or sets the list of customers to be
     migrated
    :type mosi_customer_ids: list[str]
    """
    _attribute_map = {'id': {'key': 'id', 'type': 'str'}, 'partner_id': {'key': 'partnerId', 'type': 'str'}, 'created_date': {'key': 'createdDate', 'type': 'iso-8601'}, 'mosi_customer_ids': {'key': 'mosiCustomerIds', 'type': '[str]'}}

    def __init__(self, id=None, partner_id=None, created_date=None, mosi_customer_ids=None):
        super(MicrosoftPartnerSdkContractsV1MigrationSyndicationMigration, self).__init__()
        self.id = id
        self.partner_id = partner_id
        self.created_date = created_date
        self.mosi_customer_ids = mosi_customer_ids