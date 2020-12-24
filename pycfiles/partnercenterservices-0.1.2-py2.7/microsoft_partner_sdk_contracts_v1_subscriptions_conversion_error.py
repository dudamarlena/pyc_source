# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_subscriptions_conversion_error.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1SubscriptionsConversionError(Model):
    """Represents an error that occurred during conversion.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param code: The error code associated with the issue. Possible values
     include: 'other', 'conversions_not_found'
    :type code: str or ~microsoft.store.partnercenterservices.models.enum
    :param description: The friendly text describing the issue.
    :type description: str
    :ivar attributes: Gets the attributes.
    :vartype attributes:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceAttributes
    """
    _validation = {'attributes': {'readonly': True}}
    _attribute_map = {'code': {'key': 'code', 'type': 'str'}, 'description': {'key': 'description', 'type': 'str'}, 'attributes': {'key': 'attributes', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceAttributes'}}

    def __init__(self, code=None, description=None):
        super(MicrosoftPartnerSdkContractsV1SubscriptionsConversionError, self).__init__()
        self.code = code
        self.description = description
        self.attributes = None
        return