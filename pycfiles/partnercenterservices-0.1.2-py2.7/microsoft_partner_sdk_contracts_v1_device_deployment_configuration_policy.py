# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_device_deployment_configuration_policy.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1DeviceDeploymentConfigurationPolicy(Model):
    """Provides information about a configuration policy associated with a
    customer.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param id: Gets or sets A GUID-formatted string that identifies the
     policy.
    :type id: str
    :param name: Gets or sets the friendly name for the policy.
    :type name: str
    :param category: Gets or sets the category of the policy. Possible values
     include: 'none', 'o_o_b_e'
    :type category: str or ~microsoft.store.partnercenterservices.models.enum
    :param description: Gets or sets the policy description.
    :type description: str
    :param devices_assigned_count: Gets or sets the number of devices assigned
     to this policy.
    :type devices_assigned_count: int
    :param policy_settings: Gets or sets the policy settings.
    :type policy_settings: list[str]
    :param created_date: Gets or sets the date and time the policy was
     created.
    :type created_date: datetime
    :param last_modified_date: Gets or sets the date and time the policy was
     last modified.
    :type last_modified_date: datetime
    :param links: Gets or sets the links.
    :type links:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceLinks
    :ivar attributes: Gets the attributes.
    :vartype attributes:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceAttributes
    """
    _validation = {'attributes': {'readonly': True}}
    _attribute_map = {'id': {'key': 'id', 'type': 'str'}, 'name': {'key': 'name', 'type': 'str'}, 'category': {'key': 'category', 'type': 'str'}, 'description': {'key': 'description', 'type': 'str'}, 'devices_assigned_count': {'key': 'devicesAssignedCount', 'type': 'int'}, 'policy_settings': {'key': 'policySettings', 'type': '[str]'}, 'created_date': {'key': 'createdDate', 'type': 'iso-8601'}, 'last_modified_date': {'key': 'lastModifiedDate', 'type': 'iso-8601'}, 'links': {'key': 'links', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceLinks'}, 'attributes': {'key': 'attributes', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceAttributes'}}

    def __init__(self, id=None, name=None, category=None, description=None, devices_assigned_count=None, policy_settings=None, created_date=None, last_modified_date=None, links=None):
        super(MicrosoftPartnerSdkContractsV1DeviceDeploymentConfigurationPolicy, self).__init__()
        self.id = id
        self.name = name
        self.category = category
        self.description = description
        self.devices_assigned_count = devices_assigned_count
        self.policy_settings = policy_settings
        self.created_date = created_date
        self.last_modified_date = last_modified_date
        self.links = links
        self.attributes = None
        return