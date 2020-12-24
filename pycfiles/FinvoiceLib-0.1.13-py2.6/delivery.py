# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/finvoicelib/elements/delivery.py
# Compiled at: 2010-03-24 05:43:08
from finvoicelib.elements import DateElement
from finvoicelib.elements import Element
from finvoicelib.elements.country import CountryName

class ManufacturerCountryCode(Element):
    """
    ManufacturerCountryCode
    """
    tag = 'ManufacturerCountryCode'


class ManufacturerCountryName(Element):
    """
    ManufacturerCountryName
    """
    tag = 'ManufacturerCountryName'


class ManufacturerIdentifier(Element):
    """
    ManufacturerIdentifier
    """
    tag = 'ManufacturerIdentifier'


class ManufacturerName(Element):
    """
    ManufacturerName
    """
    tag = 'ManufacturerName'


class DelivererCountryCode(Element):
    """
    DelivererCountryCode
    """
    tag = 'DelivererCountryCode'


class DelivererCountryName(Element):
    """
    DelivererCountryName
    """
    tag = 'DelivererCountryName'


class DelivererIdentifier(Element):
    """
    DelivererIdentifier
    """
    tag = 'DelivererIdentifier'


class DelivererName(Element):
    """
    DelivererName
    """
    tag = 'DelivererName'


class DeliveryDate(DateElement):
    """
    DeliveryDate
    """
    tag = 'DeliveryDate'


class DeliveryMethodText(Element):
    """
    DeliveryMethodText
    """
    tag = 'DeliveryMethodText'


class DeliveryOrganisationName(Element):
    """
    DeliveryOrganisationName
    """
    tag = 'DeliveryOrganisationName'


class DeliveryPartyIdentifier(Element):
    """
    DeliveryPartyIdentifier
    """
    tag = 'DeliveryPartyIdentifier'


class DeliveryPostCodeIdentifier(Element):
    """
    DeliveryPostCodeIdentifier
    """
    tag = 'DeliveryPostCodeIdentifier'


class DeliveryPostofficeBoxIdentifier(Element):
    """
    DeliveryPostofficeBoxIdentifier
    """
    tag = 'DeliveryPostofficeBoxIdentifier'


class DeliveryStreetName(Element):
    """
    DeliveryStreetName
    """
    tag = 'DeliveryStreetName'


class DeliveryTermsText(Element):
    """
    DeliveryTermsText
    """
    tag = 'DeliveryTermsText'


class TerminalAddressText(Element):
    """
    TerminalAddressText
    """
    tag = 'TerminalAddressText'


class WaybillIdentifier(Element):
    """
    WaybillIdentifier
    """
    tag = 'WaybillIdentifier'


class WaybillTypeCode(Element):
    """
    WaybillTypeCode
    """
    tag = 'WaybillTypeCode'


class DeliveryTownName(Element):
    """
    DeliveryTownName
    """
    tag = 'DeliveryTownName'


class DeliveryEmailaddressIdentifier(Element):
    """
    DeliveryEmailaddressIdentifier
    """
    tag = 'DeliveryEmailaddressIdentifier'


class DeliveryPhoneNumberIdentifier(Element):
    """
    DeliveryPhoneNumberIdentifier
    """
    tag = 'DeliveryPhoneNumberIdentifier'


class DeliveryCommunicationDetails(Element):
    """
    DeliveryCommunicationDetails
    """
    tag = 'DeliveryCommunicationDetails'
    aggregate = [DeliveryEmailaddressIdentifier,
     DeliveryPhoneNumberIdentifier]


class DeliveryContactPersonName(Element):
    """
    DeliveryContactPersonName
    """
    tag = 'DeliveryContactPersonName'


class DeliveryContactPersonEmail(Element):
    """
    DeliveryContactPersonName
    """
    tag = 'DeliveryContactPersonEmail'


class DeliveryPostalAddressDetails(Element):
    """
    DeliveryPostalAddressDetails
    """
    tag = 'DeliveryPostalAddressDetails'
    aggregate = [DeliveryStreetName,
     DeliveryTownName,
     DeliveryPostCodeIdentifier,
     CountryName,
     DeliveryPostofficeBoxIdentifier]


class DeliveryPartyDetails(Element):
    """
    DeliveryPartyDetails
    """
    tag = 'DeliveryPartyDetails'
    aggregate = [DeliveryPartyIdentifier,
     DeliveryOrganisationName,
     DeliveryPostalAddressDetails]


class DeliveryDetails(Element):
    """
    DeliveryDetails
    """
    tag = 'DeliveryDetails'
    aggregate = [DeliveryDate,
     DeliveryMethodText,
     DeliveryTermsText,
     TerminalAddressText,
     WaybillIdentifier,
     WaybillTypeCode,
     DelivererIdentifier,
     DelivererName,
     DelivererName,
     DelivererCountryCode,
     DelivererCountryName,
     ManufacturerIdentifier,
     ManufacturerName,
     ManufacturerCountryCode,
     ManufacturerCountryName]