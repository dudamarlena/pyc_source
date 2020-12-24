# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_migration_customer_syndication_migration.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1MigrationCustomerSyndicationMigration(Model):
    """Status of customer migration from syndication to CSP.

    :param mosi_customer_id: Gets or sets the Mosi customer ID
    :type mosi_customer_id: str
    :param customer_name: Gets or sets the customer name.
    :type customer_name: str
    :param tenant_id: Gets or sets the Mosi tenant Id.
    :type tenant_id: str
    :param csp_customer_id: Gets or sets the CSP customer Id.
    :type csp_customer_id: str
    :param status: Gets or sets the status of migration
    :type status: str
    :param error_details: Gets or sets the error details if the migration
     fails
    :type error_details: str
    :param error_code: Gets or sets the error code if the migration fails
    :type error_code: str
    :param migrated_subscriptions: Gets or sets the migrated CSP
     subscriptions.
    :type migrated_subscriptions:
     list[~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1MigrationSubscriptionSyndicationMigrationStatus]
    """
    _attribute_map = {'mosi_customer_id': {'key': 'mosiCustomerId', 'type': 'str'}, 'customer_name': {'key': 'customerName', 'type': 'str'}, 'tenant_id': {'key': 'tenantId', 'type': 'str'}, 'csp_customer_id': {'key': 'cspCustomerId', 'type': 'str'}, 'status': {'key': 'status', 'type': 'str'}, 'error_details': {'key': 'errorDetails', 'type': 'str'}, 'error_code': {'key': 'errorCode', 'type': 'str'}, 'migrated_subscriptions': {'key': 'migratedSubscriptions', 'type': '[MicrosoftPartnerSdkContractsV1MigrationSubscriptionSyndicationMigrationStatus]'}}

    def __init__(self, mosi_customer_id=None, customer_name=None, tenant_id=None, csp_customer_id=None, status=None, error_details=None, error_code=None, migrated_subscriptions=None):
        super(MicrosoftPartnerSdkContractsV1MigrationCustomerSyndicationMigration, self).__init__()
        self.mosi_customer_id = mosi_customer_id
        self.customer_name = customer_name
        self.tenant_id = tenant_id
        self.csp_customer_id = csp_customer_id
        self.status = status
        self.error_details = error_details
        self.error_code = error_code
        self.migrated_subscriptions = migrated_subscriptions