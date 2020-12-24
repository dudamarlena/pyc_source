# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_user_license_management_license_warning.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1UserLicenseManagementLicenseWarning(Model):
    """Contains warning information that occurred during a license update
    operation.

    :param code: Gets or sets the warning code.
    :type code: str
    :param message: Gets or sets the warning message.
    :type message: str
    :param service_plans: Gets or sets the list of service plan names
     associated with the warning.
    :type service_plans: list[str]
    """
    _attribute_map = {'code': {'key': 'code', 'type': 'str'}, 'message': {'key': 'message', 'type': 'str'}, 'service_plans': {'key': 'servicePlans', 'type': '[str]'}}

    def __init__(self, code=None, message=None, service_plans=None):
        super(MicrosoftPartnerSdkContractsV1UserLicenseManagementLicenseWarning, self).__init__()
        self.code = code
        self.message = message
        self.service_plans = service_plans