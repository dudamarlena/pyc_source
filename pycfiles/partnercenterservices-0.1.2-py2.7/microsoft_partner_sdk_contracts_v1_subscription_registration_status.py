# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_subscription_registration_status.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1SubscriptionRegistrationStatus(Model):
    """Provides information about the provisioning status of a subscription.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param subscription_id: Gets or sets a GUID formatted string that
     identifies the subscription.
    :type subscription_id: str
    :param status:
    :type status: str
    :ivar attributes: Gets the attributes.
    :vartype attributes:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceAttributes
    """
    _validation = {'attributes': {'readonly': True}}
    _attribute_map = {'subscription_id': {'key': 'subscriptionId', 'type': 'str'}, 'status': {'key': 'status', 'type': 'str'}, 'attributes': {'key': 'attributes', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceAttributes'}}

    def __init__(self, subscription_id=None, status=None):
        super(MicrosoftPartnerSdkContractsV1SubscriptionRegistrationStatus, self).__init__()
        self.subscription_id = subscription_id
        self.status = status
        self.attributes = None
        return