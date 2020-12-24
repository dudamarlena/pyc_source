# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/finvoicelib/elements/subinvoice_row.py
# Compiled at: 2010-03-24 05:43:08
from finvoice.elements import Element

class SubOriginalInvoiceNumber(Element):
    """
    SubOriginalInvoiceNumber
    """
    tag = 'SubOriginalInvoiceNumber'


class SubRowAccountDimensionText(Element):
    """
    SubRowAccountDimensionText
    """
    tag = 'SubRowAccountDimensionText'


class SubRowAgreementIdentifier(Element):
    """
    SubRowAgreementIdentifier
    """
    tag = 'SubRowAgreementIdentifier'


class SubRowAmount(Element):
    """
    SubRowAmount
    """
    tag = 'SubRowAmount'


class SubRowDelivererCountryCode(Element):
    """
    SubRowDelivererCountryCode
    """
    tag = 'SubRowDelivererCountryCode'


class SubRowDelivererCountryName(Element):
    """
    SubRowDelivererCountryName
    """
    tag = 'SubRowDelivererCountryName'


class SubRowDelivererIdentifier(Element):
    """
    SubRowDelivererIdentifier
    """
    tag = 'SubRowDelivererIdentifier'


class SubRowDelivererName(Element):
    """
    SubRowDelivererName
    """
    tag = 'SubRowDelivererName'


class SubRowDeliveryDate(Element):
    """
    SubRowDeliveryDate
    """
    tag = 'SubRowDeliveryDate'


class SubRowDeliveryIdentifier(Element):
    """
    SubRowDeliveryIdentifier
    """
    tag = 'SubRowDeliveryIdentifier'


class SubRowIdentifier(Element):
    """
    SubRowIdentifier
    """
    tag = 'SubRowIdentifier'


class SubRowIdentifierDate(Element):
    """
    SubRowIdentifierDate
    """
    tag = 'SubRowIdentifierDate'


class SubRowManufacturerCountryCode(Element):
    """
    SubRowManufacturerCountryCode
    """
    tag = 'SubRowManufacturerCountryCode'


class SubRowManufacturerCountryName(Element):
    """
    SubRowManufacturerCountryName
    """
    tag = 'SubRowManufacturerCountryName'


class SubRowManufacturerIdentifier(Element):
    """
    SubRowManufacturerIdentifier
    """
    tag = 'SubRowManufacturerIdentifier'


class SubRowManufacturerName(Element):
    """
    SubRowManufacturerName
    """
    tag = 'SubRowManufacturerName'


class SubRowNormalProposedAccountIdentifier(Element):
    """
    SubRowNormalProposedAccountIdentifier
    """
    tag = 'SubRowNormalProposedAccountIdentifier'


class SubRowPriceListIdentifier(Element):
    """
    SubRowPriceListIdentifier
    """
    tag = 'SubRowPriceListIdentifier'


class SubRowRequestOfQuotationIdentifier(Element):
    """
    SubRowRequestOfQuotationIdentifier
    """
    tag = 'SubRowRequestOfQuotationIdentifier'


class SubRowShortProposedAccountIdentifier(Element):
    """
    SubRowShortProposedAccountIdentifier
    """
    tag = 'SubRowShortProposedAccountIdentifier'


class SubRowVatAmount(Element):
    """
    SubRowVatAmount
    """
    tag = 'SubRowVatAmount'


class SubRowVatExcludedAmount(Element):
    """
    SubRowVatExcludedAmount
    """
    tag = 'SubRowVatExcludedAmount'


class SubRowVatRatePercent(Element):
    """
    SubRowVatRatePercent
    """
    tag = 'SubRowVatRatePercent'


class SubRowWaybillIdentifier(Element):
    """
    SubRowWaybillIdentifier
    """
    tag = 'SubRowWaybillIdentifier'


class SubArticleIdentifier(Element):
    """
    SubArticleIdentifier
    """
    tag = 'SubArticleIdentifier'


class SubArticleName(Element):
    """
    SubArticleName
    """
    tag = 'SubArticleName'


class SubRowDeliveryDetails(Element):
    """
    SubRowDeliveryDetails
    """
    tag = 'SubRowDeliveryDetails'
    aggregate = [
     SubRowWaybillIdentifier,
     SubRowDelivererIdentifier,
     SubRowDelivererName,
     SubRowDelivererName,
     SubRowDelivererCountryCode,
     SubRowDelivererCountryName,
     SubRowManufacturerIdentifier,
     SubRowManufacturerName,
     SubRowManufacturerCountryCode,
     SubRowManufacturerCountryName]


class SubInvoiceRow(Element):
    """
    SubInvoiceRow
    """
    tag = 'SubInvoiceRow'
    aggregate = [
     SubArticleIdentifier,
     SubArticleName,
     SubRowIdentifier,
     SubRowIdentifierDate,
     SubOriginalInvoiceNumber,
     SubRowDeliveryIdentifier,
     SubRowDeliveryDate,
     SubRowAgreementIdentifier,
     SubRowRequestOfQuotationIdentifier,
     SubRowPriceListIdentifier,
     SubRowDeliveryDetails,
     SubRowShortProposedAccountIdentifier,
     SubRowNormalProposedAccountIdentifier,
     SubRowAccountDimensionText,
     SubRowVatRatePercent,
     SubRowVatAmount,
     SubRowVatExcludedAmount,
     SubRowAmount]