# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_contracts_utilizations_azure_resource.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1ContractsUtilizationsAzureResource(Model):
    """Describes the properties of an Azure resource.

    :param id: Gets or sets the unique identifier of the Azure resource. Also
     known as resource ID or resource GUID.
    :type id: str
    :param name: Gets or sets the friendly name of the Azure resource being
     consumed.
    :type name: str
    :param category: Gets or sets the category of the consumed Azure resource.
    :type category: str
    :param subcategory: Gets or sets the sub-category of the consumed Azure
     resource.
    :type subcategory: str
    :param region: Gets or sets the region of the consumed Azure resource.
    :type region: str
    """
    _attribute_map = {'id': {'key': 'id', 'type': 'str'}, 'name': {'key': 'name', 'type': 'str'}, 'category': {'key': 'category', 'type': 'str'}, 'subcategory': {'key': 'subcategory', 'type': 'str'}, 'region': {'key': 'region', 'type': 'str'}}

    def __init__(self, id=None, name=None, category=None, subcategory=None, region=None):
        super(MicrosoftPartnerSdkContractsV1ContractsUtilizationsAzureResource, self).__init__()
        self.id = id
        self.name = name
        self.category = category
        self.subcategory = subcategory
        self.region = region