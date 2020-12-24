# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/event/dd/acceptcriteria/contains_data_flavor.py
# Compiled at: 2013-04-04 15:36:37
"""A criterion that checks whether Transferable contains given data
flavor."""
from muntjac.event.dd.acceptcriteria.client_side_criterion import ClientSideCriterion

class ContainsDataFlavor(ClientSideCriterion):
    """A Criterion that checks whether L{Transferable} contains given data
    flavor. The developer might for example accept the incoming data only
    if it contains "Url" or "Text".
    """

    def __init__(self, dataFlavor):
        """Constructs a new instance of L{ContainsDataFlavor}.

        @param dataFlavor:
                   the type of data that will be checked from
                   L{Transferable}
        """
        self._dataFlavorId = dataFlavor

    def paintContent(self, target):
        super(ContainsDataFlavor, self).paintContent(target)
        target.addAttribute('p', self._dataFlavorId)

    def accept(self, dragEvent):
        return self._dataFlavorId in dragEvent.getTransferable().getDataFlavors()

    def getIdentifier(self):
        return 'com.vaadin.event.dd.acceptcriteria.ContainsDataFlavor'