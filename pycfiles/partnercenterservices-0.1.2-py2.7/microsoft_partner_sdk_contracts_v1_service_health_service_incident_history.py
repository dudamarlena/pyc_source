# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_service_health_service_incident_history.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1ServiceHealthServiceIncidentHistory(Model):
    """Represents the message history for an office incident.

    :param published_time: Gets or sets the published time
    :type published_time: datetime
    :param message_text: Gets or sets the Message text
    :type message_text: str
    """
    _attribute_map = {'published_time': {'key': 'publishedTime', 'type': 'iso-8601'}, 'message_text': {'key': 'messageText', 'type': 'str'}}

    def __init__(self, published_time=None, message_text=None):
        super(MicrosoftPartnerSdkContractsV1ServiceHealthServiceIncidentHistory, self).__init__()
        self.published_time = published_time
        self.message_text = message_text