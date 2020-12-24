# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\lrivera\Documents\Visual Studio 2013\Projects\iBizProduct-Python\iBizProduct-Python\src\Contracts\iBizSpec.py
# Compiled at: 2016-04-11 18:03:07
from abc import ABCMeta, abstractmethod
from future.utils import with_metaclass

class iBizSpec(with_metaclass(ABCMeta)):

    @property
    def Spec(self):
        pass

    @Spec.getter
    @abstractmethod
    def getSpec(self):
        pass