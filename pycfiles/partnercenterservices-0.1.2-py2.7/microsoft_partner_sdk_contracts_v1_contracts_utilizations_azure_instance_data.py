# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_contracts_utilizations_azure_instance_data.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1ContractsUtilizationsAzureInstanceData(Model):
    """Describes the properties of an Azure Instance Data resource.

    :param resource_uri: Gets or sets the fully qualified Azure resource ID,
     which includes the resource groups and the instance name.
    :type resource_uri: str
    :param location: Gets or sets the region in which the service was run.
    :type location: str
    :param part_number: Gets or sets the unique namespace used to identify the
     resource for Azure Marketplace 3rd party usage. This may be an empty
     string.
    :type part_number: str
    :param order_number: Gets or sets the unique namespace used to identify
     the 3rd party order for Azure Marketplace. This may be an empty string.
    :type order_number: str
    :param tags: Gets or sets the the resource tags specified by the user.
    :type tags: dict[str, str]
    :param additional_info: Gets or sets the the additional info fields.
    :type additional_info: dict[str, str]
    """
    _attribute_map = {'resource_uri': {'key': 'resourceUri', 'type': 'str'}, 'location': {'key': 'location', 'type': 'str'}, 'part_number': {'key': 'partNumber', 'type': 'str'}, 'order_number': {'key': 'orderNumber', 'type': 'str'}, 'tags': {'key': 'tags', 'type': '{str}'}, 'additional_info': {'key': 'additionalInfo', 'type': '{str}'}}

    def __init__(self, resource_uri=None, location=None, part_number=None, order_number=None, tags=None, additional_info=None):
        super(MicrosoftPartnerSdkContractsV1ContractsUtilizationsAzureInstanceData, self).__init__()
        self.resource_uri = resource_uri
        self.location = location
        self.part_number = part_number
        self.order_number = order_number
        self.tags = tags
        self.additional_info = additional_info