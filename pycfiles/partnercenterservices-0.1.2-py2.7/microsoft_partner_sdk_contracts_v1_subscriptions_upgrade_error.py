# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_subscriptions_upgrade_error.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1SubscriptionsUpgradeError(Model):
    """Represents an error for subscription upgrade eligibility.
    Provides a reason why an upgrade cannot be performed.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param code: The error code associated with the issue. Possible values
     include: 'other', 'delegated_admin_permissions_disabled',
     'subscription_status_not_active', 'conflicting_service_types',
     'concurrency_conflicts', 'user_context_required',
     'subscription_add_ons_present',
     'subscription_does_not_have_any_upgrade_paths',
     'subscription_target_offer_not_found', 'subscription_not_provisioned',
     'offer_does_not_support_billing_cycle'
    :type code: str or ~microsoft.store.partnercenterservices.models.enum
    :param description: Friendly text describing the error.
    :type description: str
    :param additional_details: Additional details regarding the error.
    :type additional_details: str
    :ivar attributes: Gets the attributes.
    :vartype attributes:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceAttributes
    """
    _validation = {'attributes': {'readonly': True}}
    _attribute_map = {'code': {'key': 'code', 'type': 'str'}, 'description': {'key': 'description', 'type': 'str'}, 'additional_details': {'key': 'additionalDetails', 'type': 'str'}, 'attributes': {'key': 'attributes', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceAttributes'}}

    def __init__(self, code=None, description=None, additional_details=None):
        super(MicrosoftPartnerSdkContractsV1SubscriptionsUpgradeError, self).__init__()
        self.code = code
        self.description = description
        self.additional_details = additional_details
        self.attributes = None
        return