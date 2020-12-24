# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/finvoicelib/elements/invoice_row.py
# Compiled at: 2010-03-24 05:47:05
from finvoicelib.elements import CurrencyElement
from finvoicelib.elements import DateElement
from finvoicelib.elements import DecimalElement
from finvoicelib.elements import Element

class ArticleIdentifier(Element):
    """
    ArticleIdentifier
    """
    tag = 'ArticleIdentifier'


class ArticleInfoUrlText(Element):
    """
    ArticleInfoUrlText
    """
    tag = 'ArticleInfoUrlText'


class ArticleName(Element):
    """
    ArticleName
    """
    tag = 'ArticleName'


class BuyerArticleIdentifier(Element):
    """
    BuyerArticleIdentifier
    """
    tag = 'BuyerArticleIdentifier'


class DeliveredQuantity(Element):
    """
    DeliveredQuantity
    """
    tag = 'DeliveredQuantity'

    def set_attributes(self):
        self.attributes = {'quantityunitcode': ''}


class OrderedQuantity(Element):
    """
    OrderedQuantity
    """
    tag = 'OrderedQuantity'

    def set_attributes(self):
        self.attributes = {'quantityunitcode': ''}


class ConfirmedQuantity(Element):
    """
    OrderedQuantity
    """
    tag = 'ConfirmedQuantity'

    def set_attributes(self):
        self.attributes = {'quantityunitcode': ''}


class UnitPriceAmount(CurrencyElement):
    """
    UnitPriceAmount
    """
    tag = 'UnitPriceAmount'


class RowAccountDimensionText(Element):
    """
    RowAccountDimensionText
    """
    tag = 'RowAccountDimensionText'


class RowAgreementIdentifier(Element):
    """
    RowAgreementIdentifier
    """
    tag = 'RowAgreementIdentifier'


class RowAmount(CurrencyElement):
    """
    RowAmount
    """
    tag = 'RowAmount'


class RowDelivererCountryCode(Element):
    """
    RowDelivererCountryCode
    """
    tag = 'RowDelivererCountryCode'


class RowDelivererCountryName(Element):
    """
    RowDelivererCountryName
    """
    tag = 'RowDelivererCountryName'


class RowDelivererIdentifier(Element):
    """
    RowDelivererIdentifier
    """
    tag = 'RowDelivererIdentifier'


class RowDelivererName(Element):
    """
    RowDelivererName
    """
    tag = 'RowDelivererName'


class RowDeliveryDate(DateElement):
    """
    RowDeliveryDate
    """
    tag = 'RowDeliveryDate'


class RowDiscountPercent(Element):
    """
    RowDiscountPercent
    """
    tag = 'RowDiscountPercent'


class RowFreeText(Element):
    """
    RowFreeText
    """
    tag = 'RowFreeText'


class RowIdentifier(Element):
    """
    RowIdentifier
    """
    tag = 'RowIdentifier'


class RowIdentifierDate(DateElement):
    """
    RowIdentifierDate
    """
    tag = 'RowIdentifierDate'


class RowManufacturerCountryCode(Element):
    """
    RowManufacturerCountryCode
    """
    tag = 'RowManufacturerCountryCode'


class RowManufacturerCountryName(Element):
    """
    RowManufacturerCountryName
    """
    tag = 'RowManufacturerCountryName'


class RowManufacturerIdentifier(Element):
    """
    RowManufacturerIdentifier
    """
    tag = 'RowManufacturerIdentifier'


class RowManufacturerName(Element):
    """
    RowManufacturerName
    """
    tag = 'RowManufacturerName'


class RowNormalProposedAccountIdentifier(Element):
    """
    RowNormalProposedAccountIdentifier
    """
    tag = 'RowNormalProposedAccountIdentifier'


class RowPriceListIdentifier(Element):
    """
    RowPriceListIdentifier
    """
    tag = 'RowPriceListIdentifier'


class RowRequestOfQuotationIdentifier(Element):
    """
    RowRequestOfQuotationIdentifier
    """
    tag = 'RowRequestOfQuotationIdentifier'


class RowShortProposedAccountIdentifier(Element):
    """
    RowShortProposedAccountIdentifier
    """
    tag = 'RowShortProposedAccountIdentifier'


class RowSubIdentifier(Element):
    """
    RowSubIdentifier
    """
    tag = 'RowSubIdentifier'


class RowVatAmount(CurrencyElement):
    """
    RowVatAmount
    """
    tag = 'RowVatAmount'


class RowVatExcludedAmount(CurrencyElement):
    """
    RowVatExcludedAmount
    """
    tag = 'RowVatExcludedAmount'


class RowVatRatePercent(DecimalElement):
    """
    RowVatRatePercent
    """
    tag = 'RowVatRatePercent'


class RowWaybillIdentifier(Element):
    """
    RowWaybillIdentifier
    """
    tag = 'RowWaybillIdentifier'


class RowDeliveryDetails(Element):
    """
    RowDeliveryDetails
    """
    tag = 'RowDeliveryDetails'
    aggregate = [
     RowWaybillIdentifier,
     RowDelivererIdentifier,
     RowDelivererName,
     RowDelivererName,
     RowDelivererCountryCode,
     RowDelivererCountryName,
     RowManufacturerIdentifier,
     RowManufacturerName,
     RowManufacturerCountryCode,
     RowManufacturerCountryName]


class InvoiceRow(Element):
    """
    InvoiceRow
    """
    tag = 'InvoiceRow'
    aggregate = [
     RowSubIdentifier,
     ArticleIdentifier,
     ArticleName,
     BuyerArticleIdentifier,
     DeliveredQuantity,
     OrderedQuantity,
     ConfirmedQuantity,
     UnitPriceAmount,
     RowAccountDimensionText,
     RowIdentifier,
     RowIdentifierDate,
     RowDeliveryDate,
     RowDiscountPercent,
     RowAgreementIdentifier,
     RowRequestOfQuotationIdentifier,
     RowPriceListIdentifier,
     RowDeliveryDetails,
     RowShortProposedAccountIdentifier,
     RowNormalProposedAccountIdentifier,
     RowFreeText,
     RowVatRatePercent,
     RowVatAmount,
     RowVatExcludedAmount,
     RowAmount]