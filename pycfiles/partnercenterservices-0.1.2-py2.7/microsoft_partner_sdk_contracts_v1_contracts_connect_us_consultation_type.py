# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_contracts_connect_us_consultation_type.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1ContractsConnectUsConsultationType(Model):
    """Represent the Connect Us Consultation Type object.

    :param name: Gets or sets the name of the consultation type.
    :type name: str
    :param code: Gets or sets the code.
    :type code: int
    """
    _attribute_map = {'name': {'key': 'name', 'type': 'str'}, 'code': {'key': 'code', 'type': 'int'}}

    def __init__(self, name=None, code=None):
        super(MicrosoftPartnerSdkContractsV1ContractsConnectUsConsultationType, self).__init__()
        self.name = name
        self.code = code