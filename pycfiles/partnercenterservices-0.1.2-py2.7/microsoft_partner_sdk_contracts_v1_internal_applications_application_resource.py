# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_internal_applications_application_resource.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1InternalApplicationsApplicationResource(Model):
    """Resource for an application to register/unregister.

    :param registration_resource: The registration resource. Possible values
     include: 'none', 'v1', 'v2'
    :type registration_resource: str or
     ~microsoft.store.partnercenterservices.models.enum
    :param status: Registration status of the application. Possible values
     include: 'none', 'active', 'disabled'
    :type status: str or ~microsoft.store.partnercenterservices.models.enum
    """
    _attribute_map = {'registration_resource': {'key': 'registrationResource', 'type': 'str'}, 'status': {'key': 'status', 'type': 'str'}}

    def __init__(self, registration_resource=None, status=None):
        super(MicrosoftPartnerSdkContractsV1InternalApplicationsApplicationResource, self).__init__()
        self.registration_resource = registration_resource
        self.status = status