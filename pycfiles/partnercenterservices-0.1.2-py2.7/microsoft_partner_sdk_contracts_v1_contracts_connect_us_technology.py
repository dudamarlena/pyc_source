# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_contracts_connect_us_technology.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1ContractsConnectUsTechnology(Model):
    """Represent the Connect Us Technology object.

    :param name: Gets or sets the name.
    :type name: str
    :param code: Gets or sets the code.
    :type code: int
    :param scenarios: Gets or sets the scenarios.
    :type scenarios:
     list[~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1ContractsConnectUsScenario]
    """
    _attribute_map = {'name': {'key': 'name', 'type': 'str'}, 'code': {'key': 'code', 'type': 'int'}, 'scenarios': {'key': 'scenarios', 'type': '[MicrosoftPartnerSdkContractsV1ContractsConnectUsScenario]'}}

    def __init__(self, name=None, code=None, scenarios=None):
        super(MicrosoftPartnerSdkContractsV1ContractsConnectUsTechnology, self).__init__()
        self.name = name
        self.code = code
        self.scenarios = scenarios