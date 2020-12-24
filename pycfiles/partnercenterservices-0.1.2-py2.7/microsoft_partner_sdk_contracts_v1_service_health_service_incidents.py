# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_service_health_service_incidents.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1ServiceHealthServiceIncidents(Model):
    """Represents an office service health incident message.

    :param workload: Workload display name
    :type workload: str
    :param incidents: Gets or sets the Incident list
    :type incidents:
     list[~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1ServiceHealthServiceIncidentDetail]
    :param status: Gets or sets the cumulative status of the service. Possible
     values include: 'normal', 'information', 'warning', 'critical'
    :type status: str or ~microsoft.store.partnercenterservices.models.enum
    :param message_center_messages: Gets or sets the message center messages
    :type message_center_messages:
     list[~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1ServiceHealthServiceIncidentDetail]
    """
    _attribute_map = {'workload': {'key': 'workload', 'type': 'str'}, 'incidents': {'key': 'incidents', 'type': '[MicrosoftPartnerSdkContractsV1ServiceHealthServiceIncidentDetail]'}, 'status': {'key': 'status', 'type': 'str'}, 'message_center_messages': {'key': 'messageCenterMessages', 'type': '[MicrosoftPartnerSdkContractsV1ServiceHealthServiceIncidentDetail]'}}

    def __init__(self, workload=None, incidents=None, status=None, message_center_messages=None):
        super(MicrosoftPartnerSdkContractsV1ServiceHealthServiceIncidents, self).__init__()
        self.workload = workload
        self.incidents = incidents
        self.status = status
        self.message_center_messages = message_center_messages