# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/finvoicelib/elements/invoice.py
# Compiled at: 2010-03-24 05:43:08
from finvoicelib.elements import CurrencyElement
from finvoicelib.elements import DateElement
from finvoicelib.elements import Element
from finvoicelib.elements.seller import SellerReferenceIdentifier

class InvoiceDate(DateElement):
    """
    InvoiceDate
    """
    tag = 'InvoiceDate'


class InvoiceTypeCode(Element):
    """
    InvoiceTypeCode
    """
    tag = 'InvoiceTypeCode'


class InvoiceTypeText(Element):
    """
    InvoiceTypeText
    """
    tag = 'InvoiceTypeText'


class OriginCode(Element):
    """
    OriginCode
    """
    tag = 'OriginCode'


class InvoiceDueDate(DateElement):
    """
    InvoiceDueDate
    """
    tag = 'InvoiceDueDate'


class InvoiceNumber(Element):
    """
    InvoiceNumber
    """
    tag = 'InvoiceNumber'


class InvoiceSenderOrganisationName(Element):
    """
    InvoiceSenderOrganisationName
    """
    tag = 'InvoiceSenderOrganisationName'


class InvoiceSenderPartyIdentifier(Element):
    """
    InvoiceSenderPartyIdentifier
    """
    tag = 'InvoiceSenderPartyIdentifier'


class InvoiceTotalVatAmount(CurrencyElement):
    """
    InvoiceTotalVatAmount
    """
    tag = 'InvoiceTotalVatAmount'


class InvoiceTotalVatExcludedAmount(CurrencyElement):
    """
    InvoiceTotalVatExcludedAmount
    """
    tag = 'InvoiceTotalVatExcludedAmount'


class InvoiceTotalVatIncludedAmount(CurrencyElement):
    """
    InvoiceTotalVatIncludedAmount
    """
    tag = 'InvoiceTotalVatIncludedAmount'


class InvoiceTypeCode(Element):
    """
    InvoiceTypeCode
    """
    tag = 'InvoiceTypeCode'


class InvoiceTypeText(Element):
    """
    InvoiceTypeText
    """
    tag = 'InvoiceTypeText'


class InvoiceUrlNameText(Element):
    """
    InvoiceUrlNameText
    """
    tag = 'InvoiceUrlNameText'


class InvoiceUrlText(Element):
    """
    InvoiceUrlText
    """
    tag = 'InvoiceUrlText'


class VatBaseAmount(Element):
    """
    VatBaseAmount
    """
    tag = 'VatBaseAmount'


class VatRateAmount(Element):
    """
    VatRateAmount
    """
    tag = 'VatRateAmount'


class VatRatePercent(Element):
    """
    VatRatePercent
    """
    tag = 'VatRatePercent'


class VatSpecificationDetails(Element):
    """
    VatSpecificationDetails
    """
    tag = 'VatSpecificationDetails'
    aggregate = [VatBaseAmount, VatRatePercent, VatRateAmount]


class OrderIdentifier(Element):
    """
    OrderIdentifier
    """
    tag = 'OrderIdentifier'


class BuyerReferenceIdentifier(Element):
    """
    Finvoice 1.3
    BuyerReferenceIdentifier
    """
    tag = 'BuyerReferenceIdentifier'


class OrderIdentifier(Element):
    """
    OrderIdentifier
    """
    tag = 'OrderIdentifier'


class InvoiceSenderPartyDetails(Element):
    """
    InvoiceSenderPartyDetails
    """
    tag = 'InvoiceSenderPartyDetails'
    aggregate = [InvoiceSenderPartyIdentifier,
     InvoiceSenderOrganisationName,
     InvoiceSenderOrganisationName]


class CashDiscountAmount(Element):
    """
    CashDiscountAmount
    """
    tag = 'CashDiscountAmount'


class CashDiscountBaseAmount(Element):
    """
    CashDiscountBaseAmount
    """
    tag = 'CashDiscountBaseAmount'


class CashDiscountDate(DateElement):
    """
    CashDiscountDate
    """
    tag = 'CashDiscountDate'


class CashDiscountPercent(Element):
    """
    CashDiscountPercent
    """
    tag = 'CashDiscountPercent'


class PaymentTermsFreeText(Element):
    """
    PaymentTermsFreeText
    """
    tag = 'PaymentTermsFreeText'


class PaymentOverDueFineFreeText(Element):
    """
    PaymentOverDueFineFreeText
    """
    tag = 'PaymentOverDueFineFreeText'


class PaymentOverDueFinePercent(Element):
    """
    PaymentOverDueFinePercent
    """
    tag = 'PaymentOverDueFinePercent'


class PaymentStatusCode(Element):
    """
    PaymentStatusCode
    """
    tag = 'PaymentStatusCode'


class PaymentStatusDetails(Element):
    """
    PaymentStatusDetails
    """
    tag = 'PaymentStatusDetails'
    aggregate = [PaymentStatusCode]


class PaymentOverDueFineDetails(Element):
    """
    PaymentOverDueFineDetails
    """
    tag = 'PaymentOverDueFineDetails'
    aggregate = [PaymentOverDueFineFreeText, PaymentOverDueFinePercent]


class InvoiceFreeText(Element):
    """
    InvoiceFreeText
    """
    tag = 'InvoiceFreeText'


class PaymentTermsDetails(Element):
    """
    PaymentTermsDetails
    """
    tag = 'PaymentTermsDetails'
    aggregate = [
     PaymentTermsFreeText,
     InvoiceDueDate,
     CashDiscountDate,
     CashDiscountBaseAmount,
     CashDiscountPercent,
     CashDiscountAmount,
     PaymentOverDueFineDetails]


class InvoiceDetails(Element):
    """
    InvoiceDetails
    """
    tag = 'InvoiceDetails'
    aggregate = [
     InvoiceTypeCode,
     InvoiceTypeText,
     OriginCode,
     InvoiceNumber,
     InvoiceDate,
     InvoiceFreeText,
     SellerReferenceIdentifier,
     BuyerReferenceIdentifier,
     OrderIdentifier,
     InvoiceTotalVatExcludedAmount,
     InvoiceTotalVatAmount,
     InvoiceTotalVatIncludedAmount,
     VatSpecificationDetails,
     PaymentTermsDetails]


class VirtualBankBarcode(Element):
    """
    VirtualBankBarcode
    """
    tag = 'VirtualBankBarcode'