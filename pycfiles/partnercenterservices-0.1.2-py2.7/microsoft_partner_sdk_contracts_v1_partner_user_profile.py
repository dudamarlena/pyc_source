# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_partner_user_profile.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1PartnerUserProfile(Model):
    """Base partner user profile.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar profile_type: Gets the profile type. Possible values include:
     'none', 'certification', 'assessment'
    :vartype profile_type: str or
     ~microsoft.store.partnercenterservices.models.enum
    :ivar attributes: Gets the attributes.
    :vartype attributes:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceAttributes
    """
    _validation = {'profile_type': {'readonly': True}, 'attributes': {'readonly': True}}
    _attribute_map = {'profile_type': {'key': 'profileType', 'type': 'str'}, 'attributes': {'key': 'attributes', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceAttributes'}}

    def __init__(self):
        super(MicrosoftPartnerSdkContractsV1PartnerUserProfile, self).__init__()
        self.profile_type = None
        self.attributes = None
        return