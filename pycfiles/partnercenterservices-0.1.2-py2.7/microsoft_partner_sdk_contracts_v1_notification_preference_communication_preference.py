# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_notification_preference_communication_preference.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1NotificationPreferenceCommunicationPreference(Model):
    """Represents the communication preference model.

    :param channel: Gets or sets the Channel for communication. Possible
     values include: 'none', 'email', 'web'
    :type channel: str or ~microsoft.store.partnercenterservices.models.enum
    :param endpoint: Gets or sets the email address used for communication
    :type endpoint: str
    :param status: Gets or sets the status for a Channel. Possible values
     include: 'not_supported', 'on', 'off'
    :type status: str or ~microsoft.store.partnercenterservices.models.enum
    :param feature_preferences: Gets or sets the feature preferences for a
     particular notification area.
    :type feature_preferences: str
    """
    _attribute_map = {'channel': {'key': 'channel', 'type': 'str'}, 'endpoint': {'key': 'endpoint', 'type': 'str'}, 'status': {'key': 'status', 'type': 'str'}, 'feature_preferences': {'key': 'featurePreferences', 'type': 'str'}}

    def __init__(self, channel=None, endpoint=None, status=None, feature_preferences=None):
        super(MicrosoftPartnerSdkContractsV1NotificationPreferenceCommunicationPreference, self).__init__()
        self.channel = channel
        self.endpoint = endpoint
        self.status = status
        self.feature_preferences = feature_preferences