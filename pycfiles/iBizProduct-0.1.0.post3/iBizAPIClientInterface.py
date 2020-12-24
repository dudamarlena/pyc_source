# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\lrivera\Documents\Visual Studio 2013\Projects\iBizProduct-Python\iBizProduct-Python\src\Contracts\iBizAPIClientInterface.py
# Compiled at: 2016-04-11 18:02:10
from abc import ABCMeta, abstractmethod
from future.utils import with_metaclass

class iBizAPIClientInterface(with_metaclass(ABCMeta)):

    @abstractmethod
    def ProductOrderAdd(self, productOrderSpec, productOrderId=None):
        pass

    @abstractmethod
    def ProductOrderEdit(self, productOrderId, productOrderSpec):
        pass

    @abstractmethod
    def ProductOrderView(self, productOrderId, infoToReturn=None):
        pass

    @abstractmethod
    def ProductOrderBillOrderAddOneTime(self, cycleBeginDate, cycleEndDate, oneTimeCost, productOrderId, detailAddon=None, descriptionAddon=None, dueNow=None):
        pass

    @abstractmethod
    def ProductOpenCaseWithOwner(self, productOrderId, caseSpec):
        pass

    @abstractmethod
    def ProductOfferPrice(self, productOrderId, accountHos, accountId=None):
        pass

    @abstractmethod
    def UpdateEvent(self, eventId, status, message):
        pass

    @abstractmethod
    def AuthenticateUser(self, productOrderAuthentication):
        pass

    @abstractmethod
    def IsValidBackendRequest(self, externalKey):
        pass

    @abstractmethod
    def ExternalKeyExists(self):
        pass

    @abstractmethod
    def VerifyExternalKey(self):
        pass