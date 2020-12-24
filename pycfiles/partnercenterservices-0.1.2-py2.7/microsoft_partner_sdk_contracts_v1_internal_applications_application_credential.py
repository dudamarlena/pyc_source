# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_internal_applications_application_credential.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1InternalApplicationsApplicationCredential(Model):
    """The application credential.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param id: The application credential Id.
    :type id: str
    :param start_date: The start date.
    :type start_date: datetime
    :param end_date: The end date.
    :type end_date: datetime
    :param password: The password.
    :type password:
     ~microsoft.store.partnercenterservices.models.SystemSecuritySecureString
    :ivar attributes: Gets the attributes.
    :vartype attributes:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceAttributes
    """
    _validation = {'attributes': {'readonly': True}}
    _attribute_map = {'id': {'key': 'id', 'type': 'str'}, 'start_date': {'key': 'startDate', 'type': 'iso-8601'}, 'end_date': {'key': 'endDate', 'type': 'iso-8601'}, 'password': {'key': 'password', 'type': 'SystemSecuritySecureString'}, 'attributes': {'key': 'attributes', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceAttributes'}}

    def __init__(self, id=None, start_date=None, end_date=None, password=None):
        super(MicrosoftPartnerSdkContractsV1InternalApplicationsApplicationCredential, self).__init__()
        self.id = id
        self.start_date = start_date
        self.end_date = end_date
        self.password = password
        self.attributes = None
        return