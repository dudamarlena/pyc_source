# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\Contracts\CaseSpec.py
# Compiled at: 2016-04-11 13:53:52
# Size of source mod 2**32: 1689 bytes
from abc import abstractmethod
from src.Contracts.iBizSpec import iBizSpec

class CaseSpec(iBizSpec):

    @property
    @abstractmethod
    def AutoClose(self):
        pass

    @AutoClose.setter
    @abstractmethod
    def setAutoClose(self, AutoClose):
        pass

    @property
    @abstractmethod
    def Description(self):
        pass

    @Description.setter
    @abstractmethod
    def setDescription(Description):
        pass

    @property
    @abstractmethod
    def Detail(self):
        pass

    @Detail.setter
    @abstractmethod
    def setDetail(self, Detail):
        pass

    @property
    @abstractmethod
    def InternalNotes(self):
        pass

    @InternalNotes.setter
    @abstractmethod
    def setInternalNotes(self, InternalNotes):
        pass

    @property
    @abstractmethod
    def IsResolved(self):
        pass

    @IsResolved.setter
    @abstractmethod
    def setIsResolved(self, IsResolved):
        pass

    @property
    @abstractmethod
    def Priority(self):
        pass

    @Priority.setter
    @abstractmethod
    def setPriority(self, Priority):
        pass

    @property
    @abstractmethod
    def ReturnHours(self):
        pass

    @ReturnHours.setter
    @abstractmethod
    def setReturnHours(self, ReturnHours):
        pass

    @property
    @abstractmethod
    def Status(self):
        pass

    @Status.setter
    @abstractmethod
    def setStatus(self, Status):
        pass

    @property
    @abstractmethod
    def Type(self):
        pass

    @Type.setter
    @abstractmethod
    def setType(self, type):
        pass