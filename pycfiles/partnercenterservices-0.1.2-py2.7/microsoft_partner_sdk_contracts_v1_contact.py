# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_contact.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1Contact(Model):
    """Describes contact information for a specific individual.

    :param first_name: Gets or sets the contact's first name.
    :type first_name: str
    :param last_name: Gets or sets the contact's last name.
    :type last_name: str
    :param email: Gets or sets the contact's email address.
    :type email: str
    :param phone_number: Gets or sets the contact's phone number.
    :type phone_number: str
    """
    _attribute_map = {'first_name': {'key': 'firstName', 'type': 'str'}, 'last_name': {'key': 'lastName', 'type': 'str'}, 'email': {'key': 'email', 'type': 'str'}, 'phone_number': {'key': 'phoneNumber', 'type': 'str'}}

    def __init__(self, first_name=None, last_name=None, email=None, phone_number=None):
        super(MicrosoftPartnerSdkContractsV1Contact, self).__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number