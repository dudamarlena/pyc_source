# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_subscriptions_upgrade_result.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1SubscriptionsUpgradeResult(Model):
    """Describes the result of the subscription upgrade process.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param source_subscription_id: The identifier of the source subscription.
    :type source_subscription_id: str
    :param target_subscription_id: The identifier of the target subscription.
    :type target_subscription_id: str
    :param upgrade_type: The type of upgrade. Possible values include: 'none',
     'upgrade_only', 'upgrade_with_license_transfer'
    :type upgrade_type: str or
     ~microsoft.store.partnercenterservices.models.enum
    :param upgrade_errors: Errors encountered while attempting to perform the
     upgrade, if applicable.
    :type upgrade_errors:
     list[~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1SubscriptionsUpgradeError]
    :param license_errors: Errors encountered while attempting to migrate user
     licenses, if applicable.
    :type license_errors:
     list[~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1SubscriptionsUserLicenseError]
    :ivar attributes: Gets the attributes.
    :vartype attributes:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceAttributes
    """
    _validation = {'attributes': {'readonly': True}}
    _attribute_map = {'source_subscription_id': {'key': 'sourceSubscriptionId', 'type': 'str'}, 'target_subscription_id': {'key': 'targetSubscriptionId', 'type': 'str'}, 'upgrade_type': {'key': 'upgradeType', 'type': 'str'}, 'upgrade_errors': {'key': 'upgradeErrors', 'type': '[MicrosoftPartnerSdkContractsV1SubscriptionsUpgradeError]'}, 'license_errors': {'key': 'licenseErrors', 'type': '[MicrosoftPartnerSdkContractsV1SubscriptionsUserLicenseError]'}, 'attributes': {'key': 'attributes', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceAttributes'}}

    def __init__(self, source_subscription_id=None, target_subscription_id=None, upgrade_type=None, upgrade_errors=None, license_errors=None):
        super(MicrosoftPartnerSdkContractsV1SubscriptionsUpgradeResult, self).__init__()
        self.source_subscription_id = source_subscription_id
        self.target_subscription_id = target_subscription_id
        self.upgrade_type = upgrade_type
        self.upgrade_errors = upgrade_errors
        self.license_errors = license_errors
        self.attributes = None
        return