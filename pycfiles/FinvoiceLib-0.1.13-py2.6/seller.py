# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/finvoicelib/elements/seller.py
# Compiled at: 2010-03-24 05:43:08
from finvoicelib.elements import BusinessIdElement
from finvoicelib.elements import Element
from finvoicelib.elements.country import CountryCode
from finvoicelib.elements.country import CountryName

class SellerOrganisationUnitNumber(Element):
    """
    SellerOrganisationUnitNumber
    """
    tag = 'SellerOrganisationUnitNumber'


class SellerPhoneNumberIdentifier(Element):
    """
    SellerPhoneNumberIdentifier
    """
    tag = 'SellerPhoneNumberIdentifier'


class SellerVatRegistrationDate(Element):
    """
    SellerVatRegistrationDate
    """
    tag = 'SellerVatRegistrationDate'


class SellerVatRegistrationText(Element):
    """
    SellerVatRegistrationText
    """
    tag = 'SellerVatRegistrationText'


class SellerAccountID(Element):
    """
    SellerAccountID
    """
    tag = 'SellerAccountID'


class SellerBic(Element):
    """
    SellerBic
    """
    tag = 'SellerBic'


class SellerAccountDetails(Element):
    """
    SellerAccountDetails
    """
    tag = 'SellerAccountDetails'
    aggregate = [SellerAccountID, SellerBic]


class SellerCommonEmailaddressIdentifier(Element):
    """
    SellerCommonEmailaddressIdentifier
    """
    tag = 'SellerCommonEmailaddressIdentifier'


class SellerContactPersonName(Element):
    """
    SellerContactPersonName
    """
    tag = 'SellerContactPersonName'


class SellerEmailaddressIdentifier(Element):
    """
    SellerEmailaddressIdentifier
    """
    tag = 'SellerEmailaddressIdentifier'


class SellerCommunicationDetails(Element):
    """
    SellerCommunicationDetails
    """
    tag = 'SellerCommunicationDetails'
    aggregate = [SellerEmailaddressIdentifier,
     SellerPhoneNumberIdentifier]


class SellerFaxNumber(Element):
    """
    SellerFaxNumber
    """
    tag = 'SellerFaxNumber'


class SellerFreeText(Element):
    """
    SellerFreeText
    """
    tag = 'SellerFreeText'


class SellerHomeTownName(Element):
    """
    SellerHomeTownName
    """
    tag = 'SellerHomeTownName'


class SellerOrganisationName(Element):
    """
    SellerOrganisationName
    """
    tag = 'SellerOrganisationName'


class SellerOrganisationTaxCode(Element):
    """
    SellerOrganisationTaxCode
    """
    tag = 'SellerOrganisationTaxCode'


class SellerOrganisationTaxCodeUrlText(Element):
    """
    SellerOrganisationTaxCodeUrlText
    """
    tag = 'SellerOrganisationTaxCodeUrlText'


class SellerPartyIdentifier(BusinessIdElement):
    """
    SellerPartyIdentifier
    """
    tag = 'SellerPartyIdentifier'


class SellerPhoneNumber(Element):
    """
    SellerPhoneNumber
    """
    tag = 'SellerPhoneNumber'


class SellerPostCodeIdentifier(Element):
    """
    SellerPostCodeIdentifier
    """
    tag = 'SellerPostCodeIdentifier'


class SellerReferenceIdentifier(Element):
    """
    SellerReferenceIdentifier
    """
    tag = 'SellerReferenceIdentifier'


class SellerStreetName(Element):
    """
    SellerStreetName
    """
    tag = 'SellerStreetName'


class SellerTownName(Element):
    """
    SellerTownName
    """
    tag = 'SellerTownName'


class SellerWebaddressIdentifier(Element):
    """
    SellerWebaddressIdentifier
    """
    tag = 'SellerWebaddressIdentifier'


class SellerPostalAddressDetails(Element):
    """
    SellerPostalAddressDetails
    """
    tag = 'SellerPostalAddressDetails'
    aggregate = [SellerStreetName,
     SellerTownName,
     SellerPostCodeIdentifier,
     CountryCode,
     CountryName]


class SellerPartyDetails(Element):
    """
    SellerPartyDetails
    """
    tag = 'SellerPartyDetails'
    aggregate = [SellerPartyIdentifier,
     SellerOrganisationName,
     SellerOrganisationTaxCode,
     SellerOrganisationTaxCodeUrlText,
     SellerPostalAddressDetails]


class InvoiceRecipientOrganisationName(Element):
    """
    InvoiceRecipientOrganisationName
    """
    tag = 'InvoiceRecipientOrganisationName'


class InvoiceRecipientPartyIdentifier(Element):
    """
    InvoiceRecipientPartyIdentifier
    """
    tag = 'InvoiceRecipientPartyIdentifier'


class InvoiceRecipientOrganisationTaxCode(Element):
    """
    InvoiceRecipientOrganisationName
    """
    tag = 'InvoiceRecipientOrganisationTaxCode'


class InvoiceRecipientPostCodeIdentifier(Element):
    """
    InvoiceRecipientPostCodeIdentifier
    """
    tag = 'InvoiceRecipientPostCodeIdentifier'


class InvoiceRecipientPostOfficeBoxIdentifier(Element):
    """
    InvoiceRecipientPostOfficeBoxIdentifier
    """
    tag = 'InvoiceRecipientPostOfficeBoxIdentifier'


class InvoiceRecipientStreetName(Element):
    """
    InvoiceRecipientStreetName
    """
    tag = 'InvoiceRecipientStreetName'


class InvoiceRecipientTownName(Element):
    """
    InvoiceRecipientTownName
    """
    tag = 'InvoiceRecipientTownName'


class InvoiceRecipientAddress(Element):
    """
    InvoiceRecipientAddress
    """
    tag = 'InvoiceRecipientAddress'


class InvoiceRecipientIntermediatorAddress(Element):
    """
    InvoiceRecipientIntermediatorAddress
    """
    tag = 'InvoiceRecipientIntermediatorAddress'


class InvoiceRecipientDetails(Element):
    """
    InvoiceRecipientDetails
    """
    tag = 'InvoiceRecipientDetails'
    aggregate = [InvoiceRecipientAddress,
     InvoiceRecipientIntermediatorAddress]


class SellerInformationDetails(Element):
    """
    SellerInformationDetails
    """
    tag = 'SellerInformationDetails'
    aggregate = [SellerHomeTownName,
     SellerPhoneNumber,
     SellerFaxNumber,
     SellerCommonEmailaddressIdentifier,
     SellerWebaddressIdentifier,
     SellerFreeText,
     SellerAccountDetails,
     SellerAccountDetails,
     SellerAccountDetails,
     InvoiceRecipientDetails,
     SellerVatRegistrationText,
     SellerVatRegistrationDate]


class InvoiceRecipientPostalAddressDetails(Element):
    """
    InvoiceRecipientPostalAddressDetails
    """
    tag = 'InvoiceRecipientPostalAddressDetails'
    aggregate = [InvoiceRecipientStreetName,
     InvoiceRecipientTownName,
     InvoiceRecipientPostCodeIdentifier,
     CountryCode,
     CountryName,
     InvoiceRecipientPostOfficeBoxIdentifier]


class InvoiceRecipientPartyDetails(Element):
    """
    InvoiceRecipientPartyDetails
    """
    tag = 'InvoiceRecipientPartyDetails'
    aggregate = [InvoiceRecipientPartyIdentifier,
     InvoiceRecipientOrganisationName,
     InvoiceRecipientOrganisationTaxCode,
     InvoiceRecipientPostalAddressDetails]