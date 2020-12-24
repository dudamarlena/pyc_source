# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_device_deployment_device_batch.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1DeviceDeploymentDeviceBatch(Model):
    """Represents a collection of devices associated with a customer.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param id: Gets or sets a GUID-formatted string that is associated with
     the batch of devices.
    :type id: str
    :param created_by: Gets or sets the name of the tenant that created the
     collection.
    :type created_by: str
    :param creation_date: Gets or sets the data and time that the collection
     was created.
    :type creation_date: datetime
    :param devices_count: Gets or sets the number of devices in the
     collection.
    :type devices_count: int
    :param devices_link: Gets or sets a link to the devices contained in this
     batch.
    :type devices_link:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonLink
    :param links: Gets or sets the links.
    :type links:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceLinks
    :ivar attributes: Gets the attributes.
    :vartype attributes:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceAttributes
    """
    _validation = {'attributes': {'readonly': True}}
    _attribute_map = {'id': {'key': 'id', 'type': 'str'}, 'created_by': {'key': 'createdBy', 'type': 'str'}, 'creation_date': {'key': 'creationDate', 'type': 'iso-8601'}, 'devices_count': {'key': 'devicesCount', 'type': 'int'}, 'devices_link': {'key': 'devicesLink', 'type': 'MicrosoftPartnerSdkContractsV1CommonLink'}, 'links': {'key': 'links', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceLinks'}, 'attributes': {'key': 'attributes', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceAttributes'}}

    def __init__(self, id=None, created_by=None, creation_date=None, devices_count=None, devices_link=None, links=None):
        super(MicrosoftPartnerSdkContractsV1DeviceDeploymentDeviceBatch, self).__init__()
        self.id = id
        self.created_by = created_by
        self.creation_date = creation_date
        self.devices_count = devices_count
        self.devices_link = devices_link
        self.links = links
        self.attributes = None
        return