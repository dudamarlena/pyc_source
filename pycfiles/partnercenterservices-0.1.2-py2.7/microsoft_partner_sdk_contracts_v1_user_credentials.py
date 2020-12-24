# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_user_credentials.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1UserCredentials(Model):
    """Describes a user's login credentials.

    :param user_name: Gets or sets the name of the user.
    :type user_name: str
    :param password: Gets or sets the user's securely stored password.
    :type password:
     ~microsoft.store.partnercenterservices.models.SystemSecuritySecureString
    """
    _attribute_map = {'user_name': {'key': 'userName', 'type': 'str'}, 'password': {'key': 'password', 'type': 'SystemSecuritySecureString'}}

    def __init__(self, user_name=None, password=None):
        super(MicrosoftPartnerSdkContractsV1UserCredentials, self).__init__()
        self.user_name = user_name
        self.password = password