# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_subscriptions_user_license_error.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1SubscriptionsUserLicenseError(Model):
    """Describes an error arising from a failed user license transfer.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param user_object_id: The unique identifier of the user object.
    :type user_object_id: str
    :param name: The name of the user.
    :type name: str
    :param email: The email of the user.
    :type email: str
    :param errors: A list of exceptions thrown when trying to perform the user
     license transfer.
    :type errors:
     list[~microsoft.store.partnercenterservices.models.MicrosoftMarketplaceServicesCoreServiceFault]
    :ivar attributes: Gets the attributes.
    :vartype attributes:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceAttributes
    """
    _validation = {'attributes': {'readonly': True}}
    _attribute_map = {'user_object_id': {'key': 'userObjectId', 'type': 'str'}, 'name': {'key': 'name', 'type': 'str'}, 'email': {'key': 'email', 'type': 'str'}, 'errors': {'key': 'errors', 'type': '[MicrosoftMarketplaceServicesCoreServiceFault]'}, 'attributes': {'key': 'attributes', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceAttributes'}}

    def __init__(self, user_object_id=None, name=None, email=None, errors=None):
        super(MicrosoftPartnerSdkContractsV1SubscriptionsUserLicenseError, self).__init__()
        self.user_object_id = user_object_id
        self.name = name
        self.email = email
        self.errors = errors
        self.attributes = None
        return