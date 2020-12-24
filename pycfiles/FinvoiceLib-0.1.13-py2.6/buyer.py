# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/finvoicelib/elements/buyer.py
# Compiled at: 2010-03-24 05:43:08
from finvoicelib.elements import BusinessIdElement
from finvoicelib.elements import Element

class BuyerOrganisationUnitNumber(Element):
    """
    BuyerOrganisationUnitNumber
    """
    tag = 'BuyerOrganisationUnitNumber'


class BuyerContactPersonName(Element):
    """
    BuyerContactPersonName
    """
    tag = 'BuyerContactPersonName'


class BuyerEmailaddressIdentifier(Element):
    """
    BuyerEmailaddressIdentifier
    """
    tag = 'BuyerEmailaddressIdentifier'


class BuyerOrganisationName(Element):
    """
    BuyerOrganisationName
    """
    tag = 'BuyerOrganisationName'


class BuyerOrganisationTaxCode(Element):
    """
    BuyerOrganisationTaxCode
    """
    tag = 'BuyerOrganisationTaxCode'


class BuyerPartyIdentifier(Element):
    """
    BuyerPartyIdentifier
    """
    tag = 'BuyerPartyIdentifier'


class BuyerPhoneNumberIdentifier(Element):
    """
    BuyerPhoneNumberIdentifier
    """
    tag = 'BuyerPhoneNumberIdentifier'


class BuyerPostCodeIdentifier(Element):
    """
    BuyerPostCodeIdentifier
    """
    tag = 'BuyerPostCodeIdentifier'


class BuyerStreetName(Element):
    """
    BuyerStreetName
    """
    tag = 'BuyerStreetName'


class BuyerTownName(Element):
    """
    BuyerTownName
    """
    tag = 'BuyerTownName'


class BuyerPostalAddressDetails(Element):
    """
    BuyerPostalAddressDetails
    """
    tag = 'BuyerPostalAddressDetails'
    aggregate = [BuyerStreetName,
     BuyerTownName,
     BuyerPostCodeIdentifier]


class BuyerPartyDetails(Element):
    """
    BuyerPartyDetails
    """
    tag = 'BuyerPartyDetails'
    aggregate = [BuyerPartyIdentifier,
     BuyerOrganisationName,
     BuyerOrganisationTaxCode,
     BuyerPostalAddressDetails]


class BuyerCommunicationDetails(Element):
    """
    BuyerCommunicationDetails
    """
    tag = 'BuyerCommunicationDetails'
    aggregate = [
     BuyerPhoneNumberIdentifier,
     BuyerEmailaddressIdentifier]