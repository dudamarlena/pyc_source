# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\lrivera\Documents\Visual Studio 2013\Projects\iBizProduct-Python\iBizProduct-Python\src\Contracts\ProductOrderSpec.py
# Compiled at: 2016-04-11 13:55:48
from abc import abstractmethod
from src.Contracts.iBizSpec import iBizSpec

class ProductOrderSpec(iBizSpec):

    @property
    @abstractmethod
    def ProductOrderId(self):
        pass

    @ProductOrderId.setter
    @abstractmethod
    def setProductOrderId(ProductOrderId):
        pass

    @property
    @abstractmethod
    def ProductOrderName(self):
        pass

    @ProductOrderName.setter
    @abstractmethod
    def setProductOrderName(self, ProductOrderName):
        pass

    @property
    @abstractmethod
    def Cost(self):
        pass

    @Cost.setter
    @abstractmethod
    def setCost(self, Cost):
        pass

    @property
    @abstractmethod
    def Setup(self):
        pass

    @Setup.setter
    @abstractmethod
    def setSetup(self, Setup):
        pass

    @property
    @abstractmethod
    def ProductOrderStatus(self):
        pass

    @ProductOrderStatus.setter
    @abstractmethod
    def setProductOrderStatus(self, ProductOrderStatus):
        pass

    @property
    @abstractmethod
    def Notes(self):
        pass

    @Notes.setter
    @abstractmethod
    def setNotes(self, Notes):
        pass