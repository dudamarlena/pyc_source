# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_device_deployment_device_policy_update_request.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1DeviceDeploymentDevicePolicyUpdateRequest(Model):
    """Provides the information required to update a list of devices with a
    policy.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param devices: Sets the list of devices to be updated. Each object
     specifies a device.
     The following properties are required:  Id, Policies.
    :type devices:
     list[~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1DeviceDeploymentDevice]
    :ivar attributes: Gets the attributes.
    :vartype attributes:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceAttributes
    """
    _validation = {'attributes': {'readonly': True}}
    _attribute_map = {'devices': {'key': 'devices', 'type': '[MicrosoftPartnerSdkContractsV1DeviceDeploymentDevice]'}, 'attributes': {'key': 'attributes', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceAttributes'}}

    def __init__(self, devices=None):
        super(MicrosoftPartnerSdkContractsV1DeviceDeploymentDevicePolicyUpdateRequest, self).__init__()
        self.devices = devices
        self.attributes = None
        return