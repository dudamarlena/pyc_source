# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/system_collections_generic_key_value_pair_microsoft_partner_sdk_contracts_v1_device_deployment_policy_category_system_string.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class SystemCollectionsGenericKeyValuePairMicrosoftPartnerSdkContractsV1DeviceDeploymentPolicyCategorySystemString(Model):
    """SystemCollectionsGenericKeyValuePairMicrosoftPartnerSdkContractsV1DeviceDeploymentPolicyCategorySystemString.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar key: Possible values include: 'none', 'o_o_b_e'
    :vartype key: str or ~microsoft.store.partnercenterservices.models.enum
    :ivar value:
    :vartype value: str
    """
    _validation = {'key': {'readonly': True}, 'value': {'readonly': True}}
    _attribute_map = {'key': {'key': 'key', 'type': 'str'}, 'value': {'key': 'value', 'type': 'str'}}

    def __init__(self):
        super(SystemCollectionsGenericKeyValuePairMicrosoftPartnerSdkContractsV1DeviceDeploymentPolicyCategorySystemString, self).__init__()
        self.key = None
        self.value = None
        return