# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_contracts_password_profile.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1ContractsPasswordProfile(Model):
    """Describes a specific password and indicates if that password needs to be
    changed.

    :param password: Gets or sets the password.
    :type password:
     ~microsoft.store.partnercenterservices.models.SystemSecuritySecureString
    :param force_change_password: Gets or sets a value indicating whether the
     password must be forcibly changed on the next login.
    :type force_change_password: bool
    """
    _attribute_map = {'password': {'key': 'password', 'type': 'SystemSecuritySecureString'}, 'force_change_password': {'key': 'forceChangePassword', 'type': 'bool'}}

    def __init__(self, password=None, force_change_password=None):
        super(MicrosoftPartnerSdkContractsV1ContractsPasswordProfile, self).__init__()
        self.password = password
        self.force_change_password = force_change_password