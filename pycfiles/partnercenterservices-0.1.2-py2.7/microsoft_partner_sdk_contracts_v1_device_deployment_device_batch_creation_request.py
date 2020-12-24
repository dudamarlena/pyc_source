# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_device_deployment_device_batch_creation_request.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1DeviceDeploymentDeviceBatchCreationRequest(Model):
    """Provides the information required to create a device batch and populate it
    with devices.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param batch_id: Gets or sets a GUID-formatted string that is associated
     with the batch of devices.
    :type batch_id: str
    :param devices: Sets the list of devices to be uploaded. Each object
     specifies a device.
     The following combinations of fields for identifying a device are
     accepted:
     hardwareHash + productKey, hardwareHash + serialNumber, hardwareHash +
     productKey + serialNumber,
     hardwareHash only, productKey only, serialNumber + oemManufacturerName +
     modelName.
    :type devices:
     list[~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1DeviceDeploymentDevice]
    :ivar attributes: Gets the attributes.
    :vartype attributes:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceAttributes
    """
    _validation = {'attributes': {'readonly': True}}
    _attribute_map = {'batch_id': {'key': 'batchId', 'type': 'str'}, 'devices': {'key': 'devices', 'type': '[MicrosoftPartnerSdkContractsV1DeviceDeploymentDevice]'}, 'attributes': {'key': 'attributes', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceAttributes'}}

    def __init__(self, batch_id=None, devices=None):
        super(MicrosoftPartnerSdkContractsV1DeviceDeploymentDeviceBatchCreationRequest, self).__init__()
        self.batch_id = batch_id
        self.devices = devices
        self.attributes = None
        return