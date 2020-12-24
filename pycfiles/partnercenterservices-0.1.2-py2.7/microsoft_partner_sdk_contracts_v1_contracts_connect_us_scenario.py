# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_contracts_connect_us_scenario.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1ContractsConnectUsScenario(Model):
    """Represent the Connect Us Scenario object.

    :param name: Gets or sets the name.
    :type name: str
    :param code: Gets or sets the code.
    :type code: int
    :param consultation_types: Gets or sets the consultation types.
    :type consultation_types:
     list[~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1ContractsConnectUsConsultationType]
    """
    _attribute_map = {'name': {'key': 'name', 'type': 'str'}, 'code': {'key': 'code', 'type': 'int'}, 'consultation_types': {'key': 'consultationTypes', 'type': '[MicrosoftPartnerSdkContractsV1ContractsConnectUsConsultationType]'}}

    def __init__(self, name=None, code=None, consultation_types=None):
        super(MicrosoftPartnerSdkContractsV1ContractsConnectUsScenario, self).__init__()
        self.name = name
        self.code = code
        self.consultation_types = consultation_types