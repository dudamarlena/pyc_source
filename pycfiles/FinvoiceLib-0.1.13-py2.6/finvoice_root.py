# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/finvoicelib/elements/finvoice_root.py
# Compiled at: 2010-03-24 05:43:08
from finvoicelib.elements import BuyerCommunicationDetails
from finvoicelib.elements import BuyerContactPersonName
from finvoicelib.elements import BuyerOrganisationUnitNumber
from finvoicelib.elements import BuyerOrganisationTaxCode
from finvoicelib.elements import BuyerPartyDetails
from finvoicelib.elements import DeliveryCommunicationDetails
from finvoicelib.elements import DeliveryContactPersonName
from finvoicelib.elements import DeliveryDetails
from finvoicelib.elements import DeliveryPartyDetails
from finvoicelib.elements import Element
from finvoicelib.elements import EpiDetails
from finvoicelib.elements import InvoiceDetails
from finvoicelib.elements import InvoiceRecipientPartyDetails
from finvoicelib.elements import InvoiceRow
from finvoicelib.elements import InvoiceSenderPartyDetails
from finvoicelib.elements import InvoiceUrlNameText
from finvoicelib.elements import InvoiceUrlText
from finvoicelib.elements import PaymentStatusDetails
from finvoicelib.elements import SellerCommunicationDetails
from finvoicelib.elements import SellerContactPersonName
from finvoicelib.elements import SellerInformationDetails
from finvoicelib.elements import SellerOrganisationUnitNumber
from finvoicelib.elements import SellerOrganisationTaxCode
from finvoicelib.elements import SellerPartyDetails
from finvoicelib.elements import SpecificationDetails
from finvoicelib.elements import VirtualBankBarcode

class FinvoiceRoot(Element):
    """
    FinvoiceRoot wrapper for the <Finvoice> element
    """
    tag = 'finvoice'
    aggregate = [
     BuyerCommunicationDetails,
     BuyerOrganisationUnitNumber,
     BuyerOrganisationTaxCode,
     BuyerContactPersonName,
     BuyerPartyDetails,
     DeliveryDetails,
     DeliveryPartyDetails,
     DeliveryContactPersonName,
     DeliveryCommunicationDetails,
     EpiDetails,
     InvoiceDetails,
     InvoiceRecipientPartyDetails,
     InvoiceRow,
     InvoiceSenderPartyDetails,
     InvoiceUrlNameText,
     InvoiceUrlText,
     PaymentStatusDetails,
     SellerCommunicationDetails,
     SellerContactPersonName,
     SellerInformationDetails,
     SellerPartyDetails,
     SellerOrganisationUnitNumber,
     SellerOrganisationTaxCode,
     SpecificationDetails,
     VirtualBankBarcode]

    def set_attributes(self):
        self.attributes = {'version': None}
        return