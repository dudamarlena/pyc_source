# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_associated_partner_user.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1AssociatedPartnerUser(Model):
    """Represents partner user who has an associated user profile.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param id: Gets or sets the id of the associated user.
    :type id: str
    :param profile_type: Gets or sets partner user profile type. Possible
     values include: 'none', 'certification', 'assessment'
    :type profile_type: str or
     ~microsoft.store.partnercenterservices.models.enum
    :param display_name: Gets or sets the display name.
    :type display_name: str
    :param user_principal_name: Gets or sets the name of the user principal.
    :type user_principal_name: str
    :ivar attributes: Gets the attributes.
    :vartype attributes:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceAttributes
    """
    _validation = {'attributes': {'readonly': True}}
    _attribute_map = {'id': {'key': 'id', 'type': 'str'}, 'profile_type': {'key': 'profileType', 'type': 'str'}, 'display_name': {'key': 'displayName', 'type': 'str'}, 'user_principal_name': {'key': 'userPrincipalName', 'type': 'str'}, 'attributes': {'key': 'attributes', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceAttributes'}}

    def __init__(self, id=None, profile_type=None, display_name=None, user_principal_name=None):
        super(MicrosoftPartnerSdkContractsV1AssociatedPartnerUser, self).__init__()
        self.id = id
        self.profile_type = profile_type
        self.display_name = display_name
        self.user_principal_name = user_principal_name
        self.attributes = None
        return