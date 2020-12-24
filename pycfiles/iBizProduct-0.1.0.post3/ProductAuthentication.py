# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\lrivera\Documents\Visual Studio 2013\Projects\iBizProduct-Python\iBizProduct-Python\src\Contracts\ProductAuthentication.py
# Compiled at: 2016-04-11 18:03:53
from abc import ABCMeta, abstractmethod
from future.utils import with_metaclass

class ProductAuthentication(with_metaclass(ABCMeta)):

    @property
    @abstractmethod
    def Action(self):
        pass

    @Action.setter
    @abstractmethod
    def setAction(self, Action):
        pass

    @property
    @abstractmethod
    def SessionID(self):
        pass

    @SessionID.setter
    @abstractmethod
    def setSetSessionID(self, SessionID):
        pass

    @property
    @abstractmethod
    def Language(self):
        pass

    @Language.setter
    @abstractmethod
    def setLanguage(self, Language):
        pass

    @property
    @abstractmethod
    def MyAccountID(self):
        pass

    @MyAccountID.setter
    @abstractmethod
    def setMyAccountID(self, MyAccountID):
        pass

    @property
    @abstractmethod
    def AccountID(self):
        pass

    @AccountID.setter
    @abstractmethod
    def setAccountID(self, AccountID):
        pass

    @property
    @abstractmethod
    def OfferID(self):
        pass

    @OfferID.setter
    @abstractmethod
    def setOfferID(self, OfferID):
        pass

    @property
    @abstractmethod
    def ProductOrderID(self):
        pass

    @ProductOrderID.setter
    @abstractmethod
    def setProductOrderID(self, ProductOrderID):
        pass