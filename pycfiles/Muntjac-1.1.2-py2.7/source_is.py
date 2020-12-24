# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/event/dd/acceptcriteria/source_is.py
# Compiled at: 2013-04-04 15:36:37
"""Client side criteria that checks if the drag source is one of the given
components."""
from muntjac.event.transferable_impl import TransferableImpl
from muntjac.event.dd.acceptcriteria.client_side_criterion import ClientSideCriterion

class SourceIs(ClientSideCriterion):
    """Client side criteria that checks if the drag source is one of the given
    components.
    """

    def __init__(self, *component):
        self._component = component

    def paintContent(self, target):
        super(SourceIs, self).paintContent(target)
        target.addAttribute('c', len(self._component))
        for i, c in enumerate(self._component):
            target.addAttribute('component' + i, c)

    def accept(self, dragEvent):
        if isinstance(dragEvent.getTransferable(), TransferableImpl):
            sourceComponent = dragEvent.getTransferable().getSourceComponent()
            for c in self._component:
                if c == sourceComponent:
                    return True

        return False

    def getIdentifier(self):
        return 'com.vaadin.event.dd.acceptcriteria.SourceIs'