# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/event/dd/acceptcriteria/source_is_target.py
# Compiled at: 2013-04-04 15:36:37
"""A criterion that ensures the drag source is the same as drop target."""
from muntjac.event.transferable_impl import TransferableImpl
from muntjac.event.dd.acceptcriteria.client_side_criterion import ClientSideCriterion

class SourceIsTarget(ClientSideCriterion):
    """A criterion that ensures the drag source is the same as drop target.
    Eg. L{Tree} or L{Table} could support only re-ordering of items,
    but no L{Transferable}s coming outside.

    Note! Class is singleton, use L{get} method to get the instance.
    """
    _instance = None

    def __init__(self):
        pass

    def accept(self, dragEvent):
        if isinstance(dragEvent.getTransferable(), TransferableImpl):
            sourceComponent = dragEvent.getTransferable().getSourceComponent()
            target = dragEvent.getTargetDetails().getTarget()
            return sourceComponent == target
        return False

    @classmethod
    def get(cls):
        return cls._instance

    def getIdentifier(self):
        return 'com.vaadin.event.dd.acceptcriteria.SourceIsTarget'


SourceIsTarget._instance = SourceIsTarget()