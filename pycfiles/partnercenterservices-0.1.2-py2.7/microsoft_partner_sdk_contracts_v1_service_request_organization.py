# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_service_request_organization.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1ServiceRequestOrganization(Model):
    """Describes the organization for which the service request is created.

    :param id: Gets or sets the unique identifier of the organization.
    :type id: str
    :param name: Gets or sets the name of the organization.
    :type name: str
    :param phone_number: Gets or sets the phone number of the organization.
    :type phone_number: str
    """
    _attribute_map = {'id': {'key': 'id', 'type': 'str'}, 'name': {'key': 'name', 'type': 'str'}, 'phone_number': {'key': 'phoneNumber', 'type': 'str'}}

    def __init__(self, id=None, name=None, phone_number=None):
        super(MicrosoftPartnerSdkContractsV1ServiceRequestOrganization, self).__init__()
        self.id = id
        self.name = name
        self.phone_number = phone_number