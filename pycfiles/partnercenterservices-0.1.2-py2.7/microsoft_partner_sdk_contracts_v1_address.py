# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_address.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1Address(Model):
    """Represents an address for a customer or partner.

    :param country: Gets or sets the country/region in ISO country code
     format.
    :type country: str
    :param region: Gets or sets the region.
    :type region: str
    :param city: Gets or sets the city.
    :type city: str
    :param state: Gets or sets the state.
    :type state: str
    :param address_line1: Gets or sets the first line of the address.
    :type address_line1: str
    :param address_line2: Gets or sets the second line of the address. This
     property is optional.
    :type address_line2: str
    :param postal_code: Gets or sets the ZIP code or postal code.
    :type postal_code: str
    :param first_name: Gets or sets the first name of a contact at the
     customer's company/organization.
    :type first_name: str
    :param last_name: Gets or sets the last name of a contact at the
     customer's company/organization.
    :type last_name: str
    :param phone_number: Gets or sets the phone number of a contact at the
     customer's company/organization. This property is optional.
    :type phone_number: str
    """
    _attribute_map = {'country': {'key': 'country', 'type': 'str'}, 'region': {'key': 'region', 'type': 'str'}, 'city': {'key': 'city', 'type': 'str'}, 'state': {'key': 'state', 'type': 'str'}, 'address_line1': {'key': 'addressLine1', 'type': 'str'}, 'address_line2': {'key': 'addressLine2', 'type': 'str'}, 'postal_code': {'key': 'postalCode', 'type': 'str'}, 'first_name': {'key': 'firstName', 'type': 'str'}, 'last_name': {'key': 'lastName', 'type': 'str'}, 'phone_number': {'key': 'phoneNumber', 'type': 'str'}}

    def __init__(self, country=None, region=None, city=None, state=None, address_line1=None, address_line2=None, postal_code=None, first_name=None, last_name=None, phone_number=None):
        super(MicrosoftPartnerSdkContractsV1Address, self).__init__()
        self.country = country
        self.region = region
        self.city = city
        self.state = state
        self.address_line1 = address_line1
        self.address_line2 = address_line2
        self.postal_code = postal_code
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number