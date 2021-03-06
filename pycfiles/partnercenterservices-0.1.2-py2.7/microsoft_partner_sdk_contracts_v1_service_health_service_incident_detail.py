# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_service_health_service_incident_detail.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1ServiceHealthServiceIncidentDetail(Model):
    """Represents an office service health incident message.

    :param id: Gets or sets the Incident ID
    :type id: str
    :param message_type: Gets or sets the message type. Possible values
     include: 'none', 'incident', 'message_center', 'all'
    :type message_type: str or
     ~microsoft.store.partnercenterservices.models.enum
    :param start_time: Gets or sets the Incident start time
    :type start_time: datetime
    :param end_time: Gets or sets the Incident End time
    :type end_time: datetime
    :param status: Gets or sets the status. Possible values include: 'normal',
     'information', 'warning', 'critical'
    :type status: str or ~microsoft.store.partnercenterservices.models.enum
    :param messages: Gets or sets the Service Health messages
    :type messages:
     list[~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1ServiceHealthServiceIncidentHistory]
    :param workload: Gets or sets the workload name
    :type workload: str
    :param affected_workload_names: Gets or sets the affected workload names
    :type affected_workload_names: list[str]
    :param resolved: Gets or sets the incident Resolved state
    :type resolved: bool
    :param impacted_area: Gets or sets the feature name
    :type impacted_area: str
    :param impacted_customers: Gets or sets the affected tenant count
    :type impacted_customers: int
    :param service_health_links: Gets or sets the link to redirect the user
     for action - set only for message center type messages.
    :type service_health_links:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1ContractsLinksServiceHealthLinks
    :param required_by: Gets or sets the date by which partner is expected to
     complete an action - set only for message center type messages.
    :type required_by: datetime
    :param category: Gets or sets the category of message center - set only
     for message center type messages.
    :type category: str
    :param action_type: Gets or sets the type of action to be followed up with
     - set only for message center type messages.
    :type action_type: str
    :param severity: Gets or sets the severity of the message - set only for
     message center type messages. Possible values include: 'normal',
     'information', 'warning', 'critical'
    :type severity: str or ~microsoft.store.partnercenterservices.models.enum
    """
    _attribute_map = {'id': {'key': 'id', 'type': 'str'}, 'message_type': {'key': 'messageType', 'type': 'str'}, 'start_time': {'key': 'startTime', 'type': 'iso-8601'}, 'end_time': {'key': 'endTime', 'type': 'iso-8601'}, 'status': {'key': 'status', 'type': 'str'}, 'messages': {'key': 'messages', 'type': '[MicrosoftPartnerSdkContractsV1ServiceHealthServiceIncidentHistory]'}, 'workload': {'key': 'workload', 'type': 'str'}, 'affected_workload_names': {'key': 'affectedWorkloadNames', 'type': '[str]'}, 'resolved': {'key': 'resolved', 'type': 'bool'}, 'impacted_area': {'key': 'impactedArea', 'type': 'str'}, 'impacted_customers': {'key': 'impactedCustomers', 'type': 'int'}, 'service_health_links': {'key': 'serviceHealthLinks', 'type': 'MicrosoftPartnerSdkContractsV1ContractsLinksServiceHealthLinks'}, 'required_by': {'key': 'requiredBy', 'type': 'iso-8601'}, 'category': {'key': 'category', 'type': 'str'}, 'action_type': {'key': 'actionType', 'type': 'str'}, 'severity': {'key': 'severity', 'type': 'str'}}

    def __init__(self, id=None, message_type=None, start_time=None, end_time=None, status=None, messages=None, workload=None, affected_workload_names=None, resolved=None, impacted_area=None, impacted_customers=None, service_health_links=None, required_by=None, category=None, action_type=None, severity=None):
        super(MicrosoftPartnerSdkContractsV1ServiceHealthServiceIncidentDetail, self).__init__()
        self.id = id
        self.message_type = message_type
        self.start_time = start_time
        self.end_time = end_time
        self.status = status
        self.messages = messages
        self.workload = workload
        self.affected_workload_names = affected_workload_names
        self.resolved = resolved
        self.impacted_area = impacted_area
        self.impacted_customers = impacted_customers
        self.service_health_links = service_health_links
        self.required_by = required_by
        self.category = category
        self.action_type = action_type
        self.severity = severity