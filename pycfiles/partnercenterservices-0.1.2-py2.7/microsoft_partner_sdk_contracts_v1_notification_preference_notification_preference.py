# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_notification_preference_notification_preference.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1NotificationPreferenceNotificationPreference(Model):
    """Represents the notification preference model.

    :param notification_area: Gets or sets the NotificationArea. Possible
     values include: 'none', 'rated_usage', 'service_health'
    :type notification_area: str or
     ~microsoft.store.partnercenterservices.models.enum
    :param locale: Gets or sets the Locale
    :type locale: str
    :param communication_preferences: Gets or sets the communication
     preferences for a profile
    :type communication_preferences:
     list[~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1NotificationPreferenceCommunicationPreference]
    """
    _attribute_map = {'notification_area': {'key': 'notificationArea', 'type': 'str'}, 'locale': {'key': 'locale', 'type': 'str'}, 'communication_preferences': {'key': 'communicationPreferences', 'type': '[MicrosoftPartnerSdkContractsV1NotificationPreferenceCommunicationPreference]'}}

    def __init__(self, notification_area=None, locale=None, communication_preferences=None):
        super(MicrosoftPartnerSdkContractsV1NotificationPreferenceNotificationPreference, self).__init__()
        self.notification_area = notification_area
        self.locale = locale
        self.communication_preferences = communication_preferences