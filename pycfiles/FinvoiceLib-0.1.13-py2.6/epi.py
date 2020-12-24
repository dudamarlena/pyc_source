# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/finvoicelib/elements/epi.py
# Compiled at: 2010-03-24 05:43:08
from finvoicelib.elements import AccountElement
from finvoicelib.elements import Element
from finvoicelib.elements import ReferenceNumberElement

class EpiAccountID(AccountElement):
    """
    EpiAccountID
    """
    tag = 'EpiAccountID'


class EpiBei(Element):
    """
    EpiBei
    """
    tag = 'EpiBei'


class EpiBfiIdentifier(Element):
    """
    EpiBfiIdentifier
    """
    tag = 'EpiBfiIdentifier'


class EpiBfiPartyDetails(Element):
    """
    EpiBfiPartyDetails
    """
    tag = 'EpiBfiPartyDetails'
    aggregate = [EpiBfiIdentifier]


class EpiCharge(Element):
    """
    EpiCharge
    """
    tag = 'EpiCharge'


class EpiDate(Element):
    """
    EpiDate
    """
    tag = 'EpiDate'


class EpiDateOptionDate(Element):
    """
    EpiDateOptionDate
    """
    tag = 'EpiDateOptionDate'


class EpiInstructedAmount(Element):
    """
    EpiInstructedAmount
    """
    tag = 'EpiInstructedAmount'


class EpiReference(Element):
    """
    EpiReference
    """
    tag = 'EpiReference'


class EpiRemittanceInfoIdentifier(ReferenceNumberElement):
    """
    EpiRemittanceInfoIdentifier
    """
    tag = 'EpiRemittanceInfoIdentifier'
    required = True


class EpiNameAddressDetails(Element):
    """
    EpiNameAddressDetails
    """
    tag = 'EpiNameAddressDetails'


class EpiBeneficiaryPartyDetails(Element):
    """
    EpiBeneficiaryPartyDetails
    """
    tag = 'EpiBeneficiaryPartyDetails'
    aggregate = [EpiNameAddressDetails, EpiBei, EpiAccountID]


class EpiIdentificationDetails(Element):
    """
    EpiIdentificationDetails
    """
    tag = 'EpiIdentificationDetails'
    aggregate = [EpiDate, EpiReference]


class EpiPartyDetails(Element):
    """
    EpiPartyDetails
    """
    tag = 'EpiPartyDetails'
    aggregate = [EpiBfiPartyDetails,
     EpiBeneficiaryPartyDetails]


class EpiPaymentInstructionDetails(Element):
    """
    EpiPaymentInstructionDetails
    """
    tag = 'EpiPaymentInstructionDetails'
    aggregate = [
     EpiRemittanceInfoIdentifier,
     EpiInstructedAmount,
     EpiCharge,
     EpiDateOptionDate]


class EpiDetails(Element):
    """
    EpiDetails
    """
    tag = 'EpiDetails'
    aggregate = [
     EpiIdentificationDetails,
     EpiPartyDetails,
     EpiPaymentInstructionDetails]