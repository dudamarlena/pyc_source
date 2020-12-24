# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/event/transferable_impl.py
# Compiled at: 2013-04-04 15:36:37
from muntjac.event.transferable import ITransferable

class TransferableImpl(ITransferable):

    def __init__(self, sourceComponent, rawVariables):
        self._sourceComponent = sourceComponent
        self._rawVariables = rawVariables

    def getSourceComponent(self):
        return self._sourceComponent

    def getData(self, dataFlavor):
        return self._rawVariables.get(dataFlavor)

    def setData(self, dataFlavor, value):
        self._rawVariables[dataFlavor] = value

    def getDataFlavors(self):
        return self._rawVariables.keys()